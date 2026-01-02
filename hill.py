from math import gcd
import numpy as np
import re

def hill_encrypt(key_matrix, digrams):
    cipher = ""

    base = ord('a')

    for digram in digrams:
        temp = np.array([ord(digram[0]) - base, ord(digram[1]) - base])
        mul = np.matmul(temp, key_matrix)
        mul = mul % 26
        cipher += (chr(mul[0] + base) + chr(mul[1] + base))

    cipher = cipher.upper()

    return cipher

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


def hill_decrypt(key_matrix, digrams):
    plaintext = ""
    base = ord('a')
    inverse_key = hill_inverse_2x2(key_matrix)

    for digram in digrams:
        temp = np.array([ord(digram[0]) - base, ord(digram[1]) - base])
        mul = np.matmul(temp, inverse_key)
        mul = mul % 26
        plaintext += (chr(mul[0] + base) + chr(mul[1] + base))
    
    plaintext = plaintext.upper()

    return plaintext


def hill_cipher(operation, key, text):
    key_matrix = np.array([[key[0], key[1]], [key[2], key[3]]])
    print(key_matrix)

    text = text.replace(" ", "")
    text = text.lower()
    text = re.sub(r'[^a-z]', '', text)
    if(len(text) % 2 == 1):
        text = text + 'x'

    digrams = []

    for i in range(0, len(text), 2):
        digrams.append(text[i] + text[i+1])

    if(operation == "Encrypt"):
        return hill_encrypt(key_matrix, digrams)
    else:
        return hill_decrypt(key_matrix, digrams)
