from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def rc5_encrypt(message):
    key = os.urandom(16)  # 128-бітний ключ
    iv = os.urandom(16)   # IV для режиму CBC
    cipher = Cipher(algorithms.ARC4(key), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message) + encryptor.finalize()
    return encrypted_message, key

def rc5_decrypt(encrypted_message, key):
    cipher = Cipher(algorithms.ARC4(key), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    return decrypted_message
