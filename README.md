# 🔐 crypt.py — Herramienta de cifrado Fernet y RSA

Este script en Python permite cifrar y descifrar textos mediante dos algoritmos:

- **Fernet**: cifrado simétrico, ideal para datos temporales.
- **RSA**: cifrado asimétrico, compatible con claves OpenSSH.

---

## ⚙️ Requisitos

- Python 3.7+
- Biblioteca `cryptography`

Instalación:

```bash
pip install cryptography
```

---

## 📌 Uso general

```bash
python crypt.py [--algo Fernet|RSA] [opciones]
```

---

## 🔐 Fernet (simétrico)

### Generar clave con timestamp:

```bash
python crypt.py --generateKey > key.txt
```

### Generar clave con timestamp personalizado:

```bash
python crypt.py --generateKeyWithTime "2025-05-05T08:06:16.049001" > key.txt
```

### Cifrar texto:

```bash
python crypt.py --key key.txt --encode "Texto secreto" > encoded.txt
```

### Descifrar texto:

```bash
python crypt.py --key key.txt --decode encoded.txt
```

---

## 🔐 RSA (asimétrico)

### Generar par de claves RSA (privada PEM + pública OpenSSH):

```bash
python crypt.py --algo RSA --generateKeyPair id_rsa id_rsa.pub
```

### Cifrar texto con clave pública o privada:

```bash
# Con clave pública
python crypt.py --algo RSA --key id_rsa.pub --encode "Mensaje secreto"

# O con clave privada (extrae clave pública internamente)
python crypt.py --algo RSA --key id_rsa --encode "Mensaje secreto"
```

### Descifrar con clave privada:

```bash
python crypt.py --algo RSA --key id_rsa --decode encoded.txt
```

### ❌ Intentar descifrar con clave pública (no permitido):

```bash
python crypt.py --algo RSA --key id_rsa.pub --decode encoded.txt
```

Resultado:
```
Error: Cannot decode with a public key. Please use the corresponding private key.
```

---

## 🧪 Formato de claves RSA

- `id_rsa`: clave privada en formato PEM
- `id_rsa.pub`: clave pública en formato `ssh-rsa ...`, compatible con OpenSSH (`~/.ssh/authorized_keys`)

---

## 🛡️ Notas de seguridad

- No compartas tu clave privada (`id_rsa`)
- El cifrado RSA soporta bloques limitados de texto. Este script funciona bien para textos breves. Para archivos o textos largos, usá una combinación híbrida (RSA+AES).

---

## 🧑‍💻 Autor

Script desarrollado para uso educativo, adaptable a automatizaciones de cifrado simples en consola.
