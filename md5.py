import struct
import math
def F(B, C, D):
    return (B & C) | (~B & D)

def G(B, C, D):
    return (B & D) | (C & ~D)

def H(B, C, D):
    return B ^ C ^ D

def I(B, C, D):
    return C ^ (B | ~D)

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def to_little_endian(x):
    return struct.pack('<I', x)

def generate_T():
    T = []
    for i in range(1, 65):
        T.append(int((2 ** 32) * abs(math.sin(i))))
    return T

def md5_initialize():
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    return A, B, C, D

def md5_padding(message):
    original_length_bits = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', original_length_bits)
    return message

def process_block(block, A, B, C, D, T):
    X = [int.from_bytes(block[i:i + 4], byteorder='little') for i in range(0, 64, 4)]
    AA, BB, CC, DD = A, B, C, D
    for i in range(64):
        if i < 16:
            f = F(B, C, D)
            g = i
        elif i < 32:
            f = G(B, C, D)
            g = (5 * i + 1) % 16
        elif i < 48:
            f = H(B, C, D)
            g = (3 * i + 5) % 16
        else:
            f = I(B, C, D)
            g = (7 * i) % 16

        temp = (A + f + X[g] + T[i]) & 0xFFFFFFFF
        A = D
        D = C
        C = B
        B = (B + left_rotate(temp, shifts[i])) & 0xFFFFFFFF

    A = (A + AA) & 0xFFFFFFFF
    B = (B + BB) & 0xFFFFFFFF
    C = (C + CC) & 0xFFFFFFFF
    D = (D + DD) & 0xFFFFFFFF

    return A, B, C, D

shifts = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

def md5(message):
    A, B, C, D = md5_initialize()
    T = generate_T()
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        A, B, C, D = process_block(block, A, B, C, D, T)
    return (to_little_endian(A) + to_little_endian(B) + to_little_endian(C) + to_little_endian(D)).hex()

