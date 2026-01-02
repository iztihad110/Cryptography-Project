def caesar_encrypt(shift, text):

    result = ""    
    text = text.upper()
    
    

    for ch in text:
        if(ch.isalpha()):
            base = ord('A')
            result += chr((ord(ch) - base + shift + 26) % 26 + base)
        else:
            result += ch
    return result

def caesar_decrypt(shift, text):
    return caesar_encrypt(-shift, text)

def caesar_cipher(operation, key, text):

    if(operation == "Encrypt"):

        return caesar_encrypt(key, text)
    
    else:
        return caesar_decrypt(key, text)