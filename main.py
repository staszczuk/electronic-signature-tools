import hashlib
from tkinter import filedialog

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from en_decrypt import encrypt_file_with_rsa, decrypt_file_with_rsa
from common import RSA_KEY_LEN, AES_KEY_LEN, AES_BLOCK_SIZE, MODE, IV

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
    # private_key, public_key = generate_rsa_key_pair()
    # pin = input("Enter PIN for encryption: ")
    # encrypted_private_key = encrypt_private_key(private_key, pin)
    # # decrypted_private_key = decrypt_private_key(encrypted_private_key, pin)
    # save_to_file(encrypted_private_key, True)
    # save_to_file(public_key, False)

    input_file_path = filedialog.askopenfilename(title="Select file to encrypt")
    public_key_path = filedialog.askopenfilename(title="Select public key file")
    if input_file_path and public_key_path:
       encrypt_file_with_rsa(input_file_path, public_key_path)

    encrypted_file_path = filedialog.askopenfilename(title="Select file to decrypt")
    private_key_path = filedialog.askopenfilename(title="Select private key file")

    if encrypted_file_path and private_key_path:
        pin = input("Enter PIN for decryption: ")
        decrypt_file_with_rsa(encrypted_file_path, private_key_path, pin)


if __name__ == "__main__":
    main()
