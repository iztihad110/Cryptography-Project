import numpy as np
from math import gcd


def mod_inverse(a, m):
    for x in range(1, m):
        if ((a * x) % m == 1):
            return x
    raise ValueError("No modular inverse exists")

def hill_inverse_2x2(key_matrix, mod=26):
    a, b = key_matrix[0]
    c, d = key_matrix[1]

    det = (a*d - b*c) % mod

    if (gcd(det, mod) != 1):
        raise ValueError("Matrix is not invertible mod 26")

    det_inv = mod_inverse(det, mod)

    adj = np.array([[ d, -b],
                    [-c,  a]])

    key_matrix_inv = (det_inv * adj) % mod
    return key_matrix_inv

def hill_attack(plaintext, ciphertext):
    a = ord(plaintext[0]) - ord('a')
    b = ord(plaintext[1]) - ord('a')
    c = ord(plaintext[2]) - ord('a')
    d = ord(plaintext[3]) - ord('a')
    a1 = ord(ciphertext[0]) - ord('a')
    b1 = ord(ciphertext[1]) - ord('a')
    c1 = ord(ciphertext[2]) - ord('a')
    d1 = ord(ciphertext[3]) - ord('a')

    plain_matrix = np.array([[a, b], [c, d]])
    cipher_matrix = np.array([[a1, b1], [c1, d1]])

    inv_plain_matrix = hill_inverse_2x2(plain_matrix)

    key = np.matmul(inv_plain_matrix, cipher_matrix)
    key = key % 26

    return key