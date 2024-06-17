import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_BLOCK_SIZE = AES.block_size
AES_KEY_LEN = 32
IV = b"0123456701234567"
MODE = AES.MODE_CBC
RSA_KEY_LEN = 4096

def decrypt_private_key(encrypted_private_key, pin):
    aes_key = hashlib.sha256(pin.encode()).digest()[:AES_KEY_LEN]
    cipher = AES.new(aes_key, MODE, IV)
    decrypted_private_key = cipher.decrypt(encrypted_private_key)
    return unpad(decrypted_private_key, AES_BLOCK_SIZE)