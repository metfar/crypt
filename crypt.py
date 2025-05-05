#!/usr/bin/env python3
#
#  crypt.py
#  
#  Copyright 2025 William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys;
import argparse;
from datetime import datetime;
from cryptography.fernet import Fernet;
from cryptography.hazmat.primitives import serialization;
from cryptography.hazmat.primitives.asymmetric import rsa, padding;
from cryptography.hazmat.primitives import hashes;
import base64;
import os;
from cryptography.exceptions import UnsupportedAlgorithm;

def generate_key_with_time(iso_time=None):
    if iso_time:
        try:
            timestamp = datetime.fromisoformat(iso_time);
        except ValueError:
            print("Invalid time format. Use ISO 8601: YYYY-MM-DDTHH:MM:SS or with .ffffff");
            return 1;
    else:
        timestamp = datetime.now();

    key = Fernet.generate_key();
    print(f"{timestamp.isoformat()} {key.decode()}");
    return 0;

def load_fernet_key(filepath):
    with open(filepath, 'rb') as f:
        content = f.read().decode().strip();
        if ' ' in content:
            return content.split(' ', 1)[1].encode();
        else:
            return content.encode();

def fernet_encode_text(keyfile, plaintext):
    key = load_fernet_key(keyfile);
    cipher = Fernet(key);
    token = cipher.encrypt(plaintext.encode());
    print(token.decode());
    return 0;

def fernet_decode_file(keyfile, ciphertext_file):
    key = load_fernet_key(keyfile);
    with open(ciphertext_file, 'rb') as f:
        ciphertext = f.read().strip();
    cipher = Fernet(key);
    plaintext = cipher.decrypt(ciphertext).decode();
    print(plaintext);
    return 0;

def rsa_generate_keypair(private_path, public_path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    );

    public_key = private_key.public_key();

    # Guardar clave privada (PEM tradicional)
    with open(private_path, "wb") as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        );

    # Guardar clave pública en formato PEM
    with open(public_path, "wb") as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.OpenSSH,
                format=serialization.PublicFormat.OpenSSH
            )
        );

    print("RSA key pair (OpenSSH-compatible) generated.");
    return 0;

def rsa_generate_keypair_ssh_paths(private_path, public_path):
    return rsa_generate_keypair(private_path, public_path);

def rsa_encode_text_from_private(private_path, plaintext):
    try:
        with open(private_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None);
            public_key = private_key.public_key();

        ciphertext = public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        );
        #print("Using RSA private key (deriving public key).\nEncrypted:");
        print(base64.b64encode(ciphertext).decode());
        return 0;
    except (ValueError, UnsupportedAlgorithm):
        #print("Using RSA public key directly.\nEncrypted:");
        return rsa_encode_text(private_path, plaintext);

def rsa_encode_text(public_path, plaintext):
    with open(public_path, 'rb') as f:
        public_key = serialization.load_ssh_public_key(f.read());

    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    );
    print(base64.b64encode(ciphertext).decode());
    return 0;

def rsa_decode_file_from_public(public_path, ciphertext_file):
    print("Error: Cannot decode with a public key. Please use the corresponding private key.");
    
    return 1;

def rsa_decode_file(private_path, ciphertext_file):
    try:
        with open(private_path, 'rb') as f:
            private_bytes = f.read()
            if not private_bytes.startswith(b"-----BEGIN RSA PRIVATE KEY-----"):
                raise ValueError("Not a valid PEM key")
            private_key = serialization.load_pem_private_key(private_bytes, password=None);

        with open(ciphertext_file, 'rb') as f:
            ciphertext = base64.b64decode(f.read().strip());

        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        );
        #print("Using RSA private key.\nDecrypted:");
        print(plaintext.decode());
        return 0;
    except (ValueError, UnsupportedAlgorithm) as e:
        print("Error: Provided key is not a valid RSA private key or not in PEM format.");
        print("Details:", e);
        return 1;

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt text using Fernet or RSA');
    parser.add_argument('--algo', type=str, default='Fernet', choices=['Fernet', 'RSA'], help='Encryption algorithm to use');
    parser.add_argument('--generateKey', action='store_true', help='Generate a Fernet key with timestamp');
    parser.add_argument('--generateKeyWithTime', type=str, help='Generate Fernet key using ISO 8601 timestamp');
    parser.add_argument('--generateKeyPair', nargs=2, metavar=('PRIVATE', 'PUBLIC'), help='Generate RSA key pair with OpenSSH public format');
    parser.add_argument('--key', type=str, help='Path to the Fernet key file or RSA key file');
    parser.add_argument('--encode', type=str, help='Text to encrypt');
    parser.add_argument('--decode', type=str, help='Path to file with encrypted text');
    parser.add_argument('--publicKey', type=str, help='RSA public key file');
    parser.add_argument('--privateKey', type=str, help='RSA private key file');

    args = parser.parse_args();

    if args.algo == 'Fernet':
        if args.generateKey:
            return generate_key_with_time();
        elif args.generateKeyWithTime:
            return generate_key_with_time(args.generateKeyWithTime);
        elif args.key and args.encode:
            return fernet_encode_text(args.key, args.encode);
        elif args.key and args.decode:
            return fernet_decode_file(args.key, args.decode);
    elif args.algo == 'RSA':
        if args.generateKeyPair:
            return rsa_generate_keypair_ssh_paths(args.generateKeyPair[0], args.generateKeyPair[1]);
        elif args.publicKey and args.encode:
            return rsa_encode_text(args.publicKey, args.encode);
        elif args.key and args.encode:
            return rsa_encode_text_from_private(args.key, args.encode);
        elif args.privateKey and args.decode:
            return rsa_decode_file(args.privateKey, args.decode);
        elif args.key and args.decode:
            if args.key.endswith(".pub"):
                return rsa_decode_file_from_public(args.key, args.decode);
            else:
                return rsa_decode_file(args.key, args.decode);
        elif args.publicKey and args.decode:
            return rsa_decode_file_from_public(args.publicKey, args.decode);
        elif args.privateKey and args.decode:
            return rsa_decode_file(args.privateKey, args.decode);

    print("Invalid combination of arguments. Use --help for options.");
    return 1;

if __name__ == '__main__':
    sys.exit(main());
