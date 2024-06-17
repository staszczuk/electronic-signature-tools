from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from common import decrypt_private_key
import os

def load_public_key(file_path):
    with open(file_path, "rb") as file:
        public_key = RSA.import_key(file.read())
    return public_key


def load_private_key(file_path, pin):
    with open(file_path, "rb") as file:
        encrypted_private_key = file.read()
    private_key = decrypt_private_key(encrypted_private_key, pin)
    return RSA.import_key(private_key)


def encrypt_file_with_rsa(input_file_path, public_key_path):
    public_key = load_public_key(public_key_path)
    rsa_cipher = PKCS1_OAEP.new(public_key)

    with open(input_file_path, "rb") as file:
        plaintext = file.read()

    ciphertext = rsa_cipher.encrypt(plaintext)

    encrypted_file_path = input_file_path + ".enc"
    with open(encrypted_file_path, "wb") as file:
        file.write(ciphertext)

    print(f"File encrypted successfully and saved as {encrypted_file_path}")


def decrypt_file_with_rsa(encrypted_file_path, private_key_path, pin):
    private_key = load_private_key(private_key_path, pin)
    rsa_cipher = PKCS1_OAEP.new(private_key)

    with open(encrypted_file_path, "rb") as file:
        ciphertext = file.read()

    plaintext = rsa_cipher.decrypt(ciphertext)

    base, ext = os.path.splitext(encrypted_file_path)
    if base.endswith(".enc"):
        base = base[:-4]
    decrypted_file_path = base + "_decrypted" + ext
    with open(decrypted_file_path, "wb") as file:
        file.write(plaintext)

    print(f"File decrypted successfully and saved as {decrypted_file_path}")
