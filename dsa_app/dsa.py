# dsa.py
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
import os

def generate_keys():
    private_key = dsa.generate_private_key(key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename, is_private=True):
    encoding = serialization.Encoding.PEM
    if is_private:
        data = key.private_bytes(
            encoding=encoding,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    else:
        data = key.public_bytes(
            encoding=encoding,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    with open(filename, 'wb') as f:
        f.write(data)

def load_private_key(filename):
    with open(filename, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(filename):
    with open(filename, 'rb') as f:
        return serialization.load_pem_public_key(f.read())

def sign_message(private_key, message):
    return private_key.sign(message.encode(), hashes.SHA256())

def sign_file(private_key, file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return private_key.sign(file_data, hashes.SHA256())

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(signature, message.encode(), hashes.SHA256())
        return True
    except Exception:
        return False

def verify_file_signature(public_key, file_path, signature):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    try:
        public_key.verify(signature, file_data, hashes.SHA256())
        return True
    except Exception:
        return False
