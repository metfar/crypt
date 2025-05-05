#!/bin/bash
f=0;
echo "🔐 Fernet test..." ;
python3 crypt.py --generateKey > test_key.txt ;
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;

python3 crypt.py --key test_key.txt --encode "secret message" > test_encoded.txt ;
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;

python3 crypt.py --key test_key.txt --decode test_encoded.txt > test_decoded.txt ;
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;

echo "✔️ Fernet decoded:";
cat test_decoded.txt;
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;
echo;

echo "🔐 RSA test..."
python3 crypt.py --algo RSA --generateKeyPair test_id_rsa test_id_rsa.pub
f=$((1+f)); if [ $? -gt 0 ]; then echo "Error $f"; exit $f; fi;

python3 crypt.py --algo RSA --key test_id_rsa.pub --encode "mensaje cifrado" > test_encoded_rsa.txt
f=$((1+f)); if [ $? -gt 0 ]; then echo "Error $f"; exit $f; fi;

python3 crypt.py --algo RSA --key test_id_rsa --decode test_encoded_rsa.txt > test_decoded_rsa.txt
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;

echo "✔️ RSA decoded:"
cat test_decoded_rsa.txt
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;
echo
echo "🧹 Temporary files clean-up..."
rm -f test_key.txt test_encoded.txt test_decoded.txt test_id_rsa test_id_rsa.pub test_encoded_rsa.txt test_decoded_rsa.txt
e=$?; f=$((1+f)); if [ $e -gt 0 ]; then echo "Error $f"; exit $f; fi;

echo "✅ End of test."
