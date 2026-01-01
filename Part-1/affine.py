import math

def affine_encrypt(key, text):
    a = key[0]
    b = key[1]
    text = text.upper()
    result = ""

    for ch in text:
        if(ch.isalpha()):
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((a * (ord(ch) - base) + b) % 26 + base)
        else:
            result += ch
        
    return result

def affine_decrypt(key, text):
    a = key[0]
    b = key[1]
    inv_a = 0
    result = ""

    for i in range(0, 25):
        if((i * a) % 26 == 1):
            inv_a = i
            break

    for ch in text:
        if(ch.isalpha()):
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((inv_a * ((ord(ch) - base) - b)) % 26 + base)
        else:
            result += ch

    return result
        

def affine_cipher(operation, key, text):

    if(operation == "Encrypt"):
        return affine_encrypt(key, text)
    
    else:
        return affine_decrypt(key, text)