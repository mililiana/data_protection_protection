from docx import Document
import struct
from md5_rc5 import md5
from linear_comparison_rc5 import linear_congruential_generator

w = 16
r = 16
b = 32

def read_file_content(filename):
    if filename.endswith('.txt'):
        with open(filename, 'rb') as f:
            return f.read()
    elif filename.endswith('.docx'):
        doc = Document(filename)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text).encode('utf-8')
    else:
        raise ValueError("Unsupported file type. Only .txt and .docx files are supported.")

def generate_key_from_passphrase(passphrase, key_size_bits):
    hash1 = md5(passphrase.encode())
    if key_size_bits == 64:
        return hash1[:8]  # молодші 64 біти
    elif key_size_bits == 256:
        hash2 = md5(hash1)  # H(H(P))
        return hash2 + hash1  # K=H(H(P))||H(P)
    else:
        raise ValueError("Invalid key size.")

def rc5_key_schedule(K):
    S = [0xB7E1]
    for i in range(1, 2 * (r + 1)):
        S.append((S[i - 1] + 0x9E37) % (2 ** w))
    return S

def rc5_encrypt_block(plain_block, S):
    A = struct.unpack('<H', plain_block[:2])[0]
    B = struct.unpack('<H', plain_block[2:])[0]
    A = (A + S[0]) % (2 ** w)
    B = (B + S[1]) % (2 ** w)
    for i in range(1, r + 1):
        A = (A ^ B) % (2 ** w)
        A = ((A << (B % w)) | (A >> (w - (B % w)))) % (2 ** w)
        A = (A + S[2 * i]) % (2 ** w)

        B = (B ^ A) % (2 ** w)
        B = ((B << (A % w)) | (B >> (w - (A % w)))) % (2 ** w)
        B = (B + S[2 * i + 1]) % (2 ** w)
    return struct.pack('<H', A) + struct.pack('<H', B)

def rc5_cbc_encrypt(plaintext, key, iv):
    S = rc5_key_schedule(key)
    blocks = [plaintext[i:i + 4] for i in range(0, len(plaintext), 4)]
    cipher_blocks = []
    prev_cipher = iv
    for block in blocks:
        padded_block = bytes([x ^ y for x, y in zip(block, prev_cipher)])
        encrypted_block = rc5_encrypt_block(padded_block, S)
        cipher_blocks.append(encrypted_block)
        prev_cipher = encrypted_block
    return b''.join(cipher_blocks)

def pad_message(message, block_size):
    padding_len = block_size - (len(message) % block_size)
    return message + bytes([padding_len] * padding_len)

def encrypt_file(filename, passphrase):
    plaintext = read_file_content(filename)

    key = generate_key_from_passphrase(passphrase, 64)

    def generate_iv(length):
        a = 1664525
        c = 1013904223
        m = 2 ** 32
        seed = 123456789
        random_sequence = linear_congruential_generator(a, c, m, seed, length)
        iv = bytes([x % 256 for x in random_sequence])
        return iv

    iv = generate_iv(4)  # w = 16 біт / 4 байти

    padded_plaintext = pad_message(plaintext, 4)  # Падінг блоку до 4 байтів

    encrypted_iv = rc5_encrypt_block(iv, rc5_key_schedule(key))
    ciphertext = rc5_cbc_encrypt(padded_plaintext, key, iv)

    with open(filename + '.enc', 'wb') as f_enc:
        f_enc.write(encrypted_iv + ciphertext)

def rc5_decrypt_block(cipher_block, S):

    A = struct.unpack('<H', cipher_block[:2])[0]
    B = struct.unpack('<H', cipher_block[2:])[0]

    for i in range(r, 0, -1):
        B = (B - S[2 * i + 1]) % (2 ** w)
        B = ((B >> (A % w)) | (B << (w - (A % w)))) % (2 ** w)
        B = B ^ A

        A = (A - S[2 * i]) % (2 ** w)
        A = ((A >> (B % w)) | (A << (w - (B % w)))) % (2 ** w)
        A = A ^ B

    A = (A - S[0]) % (2 ** w)
    B = (B - S[1]) % (2 ** w)

    return struct.pack('<H', A) + struct.pack('<H', B)

def rc5_cbc_decrypt(ciphertext, key, iv):
    S = rc5_key_schedule(key)
    blocks = [ciphertext[i:i + 4] for i in range(0, len(ciphertext), 4)]
    decrypted_blocks = []
    prev_cipher = iv

    for block in blocks:
        decrypted_block = rc5_decrypt_block(block, S)
        plain_block = bytes([x ^ y for x, y in zip(decrypted_block, prev_cipher)])
        decrypted_blocks.append(plain_block)
        prev_cipher = block

    return b''.join(decrypted_blocks)

def unpad_message(padded_message):
    padding_len = padded_message[-1]
    return padded_message[:-padding_len]

def decrypt_file(filename, passphrase):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()

    key = generate_key_from_passphrase(passphrase, 64)

    encrypted_iv = encrypted_data[:4]
    ciphertext = encrypted_data[4:]

    iv = rc5_decrypt_block(encrypted_iv, rc5_key_schedule(key))
    decrypted_padded_text = rc5_cbc_decrypt(ciphertext, key, iv)
    plaintext = unpad_message(decrypted_padded_text)

    with open(filename.replace('.enc', '.dec'), 'wb') as f_dec:
        f_dec.write(plaintext)
