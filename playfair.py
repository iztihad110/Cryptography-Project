import re

def process_digrams(text):
    
    

    digrams = []
    i = 0

    
    while i < len(text):
        a = text[i]

        if i + 1 < len(text):
            b = text[i + 1]

            
            if a == b:
                digrams.append(a + 'x')
                i += 1
            else:
                digrams.append(a + b)
                i += 2
        else:
            
            digrams.append(a + 'x')
            i += 1

    return digrams


def playfair_encrypt(key_matrix, text, index):
    digrams = process_digrams(text)

    cipher = ""

    for digram in digrams:
        if(index[digram[0]][0] == index[digram[1]][0]):
            cipher += key_matrix[index[digram[0]][0]][(index[digram[0]][1] + 1) % 5]
            cipher += key_matrix[index[digram[0]][0]][(index[digram[1]][1] + 1) % 5]
        elif(index[digram[0]][1] == index[digram[1]][1]):
            cipher += key_matrix[(index[digram[0]][0] + 1) % 5][index[digram[0]][1]]
            cipher += key_matrix[(index[digram[1]][0] + 1) % 5][index[digram[0]][1]]
        else:
            cipher += key_matrix[(index[digram[0]][0])][index[digram[1]][1]]
            cipher += key_matrix[(index[digram[1]][0])][index[digram[0]][1]]
        cipher +=" "

    cipher = cipher.upper()

    return cipher


def playfair_decrypt(key_matrix, text, index):
    text = text.lower()
    digrams = []
    text = text.replace(" ", "")

    for i in range(0, len(text), 2):
        
        digrams.append(text[i] + text[i+1]) 

    plaintext = ""
    # print(digrams)
    # print(index)

    for digram in digrams:
        if(index[digram[0]][0] == index[digram[1]][0]):
            plaintext += key_matrix[index[digram[0]][0]][(index[digram[0]][1] - 1 + 5) % 5]
            plaintext += key_matrix[index[digram[0]][0]][(index[digram[1]][1] - 1 + 5) % 5]
        elif(index[digram[0]][1] == index[digram[1]][1]):
            plaintext += key_matrix[(index[digram[0]][0] - 1 + 5) % 5][index[digram[0]][1]]
            plaintext += key_matrix[(index[digram[1]][0] - 1 + 5) % 5][index[digram[0]][1]]
        else:
            plaintext += key_matrix[(index[digram[0]][0])][index[digram[1]][1]]
            plaintext += key_matrix[(index[digram[1]][0])][index[digram[0]][1]]
        plaintext +=" "

    plaintext = plaintext.upper()

    return plaintext

def playfair_cipher(operation, key, text):

    text = text.lower()
    text = re.sub(r'[^a-z]', '', text)  
    key = re.sub(r'[^a-z]', '', key)

    i = 0

    for ch in key:
        if(ch == 'i'):
            i = 1
            break
    if(i == 1):
        text = text.replace('j', 'i')
    else:
        text = text.replace('i', 'j')
    print(text)
    
    key_matrix = []
    key_matrix = [list(key[i:i+5]) for i in range(0, 25, 5)]
        
        

    print(key_matrix)

    index = {}

    for i in range(0,5):
        for j in range(0,5):
            index[key_matrix[i][j]] = [i, j]

    print(index)
    if(operation == "Encrypt"):
        return playfair_encrypt(key_matrix, text, index)
    else:
        return playfair_decrypt(key_matrix, text, index)