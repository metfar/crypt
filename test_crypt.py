import subprocess;
import os;

def run(command):
    return subprocess.check_output(command, shell=True, text=True).strip();

def test_fernet_roundtrip(tmp_path):
    key_file = tmp_path / "key.txt";
    enc_file = tmp_path / "encoded.txt";
    dec_file = tmp_path / "decoded.txt";

    key = run(f"python3 crypt.py --generateKey");
    key_file.write_text(key);

    encoded = run(f"python3 crypt.py --key {key_file} --encode 'mensaje fernet'");
    enc_file.write_text(encoded);

    decoded = run(f"python3 crypt.py --key {key_file} --decode {enc_file}");
    dec_file.write_text(decoded);

    assert decoded == "mensaje fernet";

def test_rsa_roundtrip(tmp_path):
    priv = tmp_path / "id_rsa";
    pub = tmp_path / "id_rsa.pub";
    enc_file = tmp_path / "rsa_encoded.txt";
    dec_file = tmp_path / "rsa_decoded.txt";

    run(f"python3 crypt.py --algo RSA --generateKeyPair {priv} {pub}");

    encoded = run(f"python3 crypt.py --algo RSA --key {pub} --encode 'mensaje rsa'");
    enc_file.write_text(encoded);

    decoded = run(f"python3 crypt.py --algo RSA --key {priv} --decode {enc_file}");
    dec_file.write_text(decoded);

    assert decoded == "mensaje rsa";

