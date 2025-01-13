class RC5:
    def __init__(self, w, r, b, key):
        self.w = w  # Розмір слова (наприклад, 16, 32 або 64 біти)
        self.r = r  # Кількість раундів
        self.b = b  # Довжина ключа в байтах
        self.key = key
        self.T = []  # Розширений ключ
        self.modulus = 2 ** self.w
        self._key_expansion()

    def _rotate_left(self, x, y):
        return ((x << y) & (self.modulus - 1)) | (x >> (self.w - y))

    def _rotate_right(self, x, y):
        return (x >> y) | ((x << (self.w - y)) & (self.modulus - 1))

    def _key_expansion(self):
        # Константи згідно специфікації RC5
        P = 0xb7e15163 if self.w == 32 else 0x9e3779b9 if self.w == 16 else 0x171a3b68
        Q = 0x9e3779b9 if self.w == 32 else 0xb7e15163 if self.w == 16 else 0x1320f57f

        L = [0] * (self.b // 4)
        for i in range(self.b - 1, -1, -1):
            L[i // 4] = (L[i // 4] << 8) + self.key[i]

        self.T = [0] * (2 * (self.r + 1))
        self.T[0] = P
        for i in range(1, 2 * (self.r + 1)):
            self.T[i] = (self.T[i - 1] + Q) % self.modulus

        A = B = i = j = 0
        for k in range(3 * max(len(L), len(self.T))):
            A = self.T[i] = self._rotate_left((self.T[i] + A + B) % self.modulus, 3)
            B = L[j] = self._rotate_left((L[j] + A + B) % self.modulus, (A + B) % self.w)
            i = (i + 1) % len(self.T)
            j = (j + 1) % len(L)

    def encrypt_block(self, plaintext):
        A = int.from_bytes(plaintext[:self.w // 8], 'big')
        B = int.from_bytes(plaintext[self.w // 8:], 'big')

        A = (A + self.T[0]) % self.modulus
        B = (B + self.T[1]) % self.modulus

        for i in range(1, self.r + 1):
            A = (self._rotate_left(A ^ B, B % self.w) + self.T[2 * i]) % self.modulus
            B = (self._rotate_left(B ^ A, A % self.w) + self.T[2 * i + 1]) % self.modulus

        return A.to_bytes(self.w // 8, 'big') + B.to_bytes(self.w // 8, 'big')

    def decrypt_block(self, ciphertext):
        A = int.from_bytes(ciphertext[:self.w // 8], 'big')
        B = int.from_bytes(ciphertext[self.w // 8:], 'big')

        for i in range(self.r, 0, -1):
            B = self._rotate_right((B - self.T[2 * i + 1]) % self.modulus, A % self.w) ^ A
            A = self._rotate_right((A - self.T[2 * i]) % self.modulus, B % self.w) ^ B

        B = (B - self.T[1]) % self.modulus
        A = (A - self.T[0]) % self.modulus

        return A.to_bytes(self.w // 8, 'big') + B.to_bytes(self.w // 8, 'big')

    def encrypt(self, plaintext, iv):
        block_size = self.w // 8
        ciphertext = bytearray()
        previous_block = iv.to_bytes(block_size, 'big')

        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i + block_size]
            if len(block) < block_size:
                block += b'\x00' * (block_size - len(block))

            xored_block = bytes(a ^ b for a, b in zip(block, previous_block))
            encrypted_block = self.encrypt_block(xored_block)
            ciphertext.extend(encrypted_block)
            previous_block = encrypted_block

        return bytes(ciphertext)

    def decrypt(self, ciphertext, iv):
        block_size = self.w // 8
        plaintext = bytearray()
        previous_block = iv.to_bytes(block_size, 'big')

        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            decrypted_block = self.decrypt_block(block)
            xored_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
            plaintext.extend(xored_block)
            previous_block = block

        return bytes(plaintext).rstrip(b'\x00')
