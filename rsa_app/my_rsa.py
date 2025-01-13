from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys(public_key_path, private_key_path):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def encrypt_message(message, public_key_path):
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(encrypted_message, private_key_path):
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

def encrypt_file(file_path, public_key_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted_data = encrypt_message(data.decode(), public_key_path)
    with open(file_path + '.enc', 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(encrypted_file_path, private_key_path, output_path):
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_message(encrypted_data, private_key_path)
    with open(output_path, 'w') as f:
        f.write(decrypted_data)
