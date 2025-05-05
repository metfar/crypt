# 🔐 crypt.py — Fernet and RSA Encryption Tool

This Python script allows you to encrypt and decrypt text using two algorithms:

- **Fernet**: Symmetric encryption, ideal for temporary data.
- **RSA**: Asymmetric encryption, compatible with OpenSSH keys.

---

## ⚙️ Requirements

- Python 3.7+
- `cryptography` library

Installation:

```bash
pip install cryptography
```

---

## 📌 General Use

```bash
python crypt.py [--something Fernet|RSA] [options]
```

---

## 🔐 Fernet (symmetric)

### Generate key with timestamp:

```bash
python crypt.py --generateKey > key.txt
```

### Generate key with custom timestamp:

```bash
python crypt.py --generateKeyWithTime "2025-05-05T08:06:16.049001" > key.txt
```

### Encrypt text:

```bash
python crypt.py --key key.txt --encode "Secret text" > encoded.txt
```

### Decrypt text:

```bash
python crypt.py --key key.txt --decode encoded.txt
```

---

## 🔐 RSA (asymmetric)

### Generate RSA key pair (PEM private + OpenSSH public):

```bash
python crypt.py --algo RSA --generateKeyPair id_rsa id_rsa.pub
```

### Encrypt text with a public or private key:

```bash
# With a public key
python crypt.py --algo RSA --key id_rsa.pub --encode "Secret message"

# Or with a private key (extract public key internally)
python crypt.py --algo RSA --key id_rsa --encode "Secret Message"
```

### Decrypt with private key:

```bash
python crypt.py --algo RSA --key id_rsa --decode encoded.txt
```

### ❌ Attempt to decrypt with public key (not allowed):

```bash
python crypt.py --algo RSA --key id_rsa.pub --decode encoded.txt
```

Result:
```
Error: Cannot decode with a public key. Please use the corresponding private key.
```

---

## 🧪 RSA Key Format

- `id_rsa`: Private key in PEM format
- `id_rsa.pub`: Public key in `ssh-rsa ...` format, compatible with OpenSSH (`~/.ssh/authorized_keys`)

---

## 🛡️ Security Notes

- Do not share your private key (`id_rsa`)
- RSA encryption supports limited blocks of text. This script works well for short texts. For files or long texts, use a hybrid combination (RSA+AES).

---

## 🧑‍💻 Author

Script developed for educational use, adaptable to simple console encryption automation.