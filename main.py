import hashlib
from tkinter import filedialog

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

AES_BLOCK_SIZE = AES.block_size
AES_KEY_LEN = 32
IV = b"0123456701234567"
MODE = AES.MODE_CBC
RSA_KEY_LEN = 4096


def generate_rsa_key_pair():
    key = RSA.generate(RSA_KEY_LEN)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_private_key(private_key, pin):
    aes_key = hashlib.sha256(pin.encode()).digest()[:AES_KEY_LEN]
    cipher = AES.new(aes_key, MODE, IV)
    padded_private_key = pad(private_key, AES_BLOCK_SIZE)
    encrypted_private_key = cipher.encrypt(padded_private_key)
    return encrypted_private_key


# def decrypt_private_key(encrypted_private_key, pin):
#     aes_key = hashlib.sha256(pin.encode()).digest()[:AES_KEY_LEN]
#     cipher = AES.new(aes_key, MODE, IV)
#     decrypted_private_key = cipher.decrypt(encrypted_private_key)
#     return unpad(decrypted_private_key, AES_BLOCK_SIZE)


def save_to_file(key, is_private_key):
    if is_private_key:
        title = "Select directory to save private key"
        file_name = "private_key.txt"
    else:
        title = "Select directory to save public key"
        file_name = "public_key.txt"

    directory = filedialog.askdirectory(title=title)

    if directory:
        file_path = directory + "/" + file_name

        with open(file_path, "wb") as file:
            file.write(key)

        print("Key saved successfully")


def main():
    private_key, public_key = generate_rsa_key_pair()
    pin = input("Enter PIN for encryption: ")
    encrypted_private_key = encrypt_private_key(private_key, pin)
    # decrypted_private_key = decrypt_private_key(encrypted_private_key, pin)
    save_to_file(encrypted_private_key, True)
    save_to_file(public_key, False)


if __name__ == "__main__":
    main()
