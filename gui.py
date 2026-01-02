import tkinter as tk
from tkinter import ttk, messagebox
import caesar
import affine
import playfair
import hill
import math
import re
import hill_attack
import tkinter.font as tkfont

def run_cipher():
    cipher = cipher_var.get()
    operation = op_var.get()
    text = input_text.get("1.0", tk.END).strip()

    if cipher == "Caesar":
        try:
            shift = int(key_entry.get("1.0", tk.END))
            if(shift > 25):
                key_entry.delete("1.0", tk.END)
                messagebox.showerror("Error", "Invalid key! Please insert a valid integer")
            else:
                result = f"Processed text: {caesar.caesar_cipher(operation, shift, text)}"
        except ValueError:
            key_entry.delete("1.0", tk.END)
            messagebox.showerror("Error", "Invalid key! Please insert a valid integer")           

    elif cipher == "Affine":
        Key = key_entry.get("1.0", tk.END).split()
        try:
            Key = list(map(int, Key))
            if(math.gcd(Key[0], 26) != 1 or len(Key) != 2):
                key_entry.delete("1.0", tk.END)
                messagebox.showerror("Error", "Invalid key! Please insert valid integers")    
            else: 
                result = f"Processed text: {affine.affine_cipher(operation, Key, text)}"
        except ValueError:
            key_entry.delete("1.0", tk.END)
            messagebox.showerror("Error", "Invalid key! Please insert valid integers")
        
    elif cipher == "Playfair":
        Key = key_entry.get("1.0", tk.END)
        # print(len(Key))
        # print(Key)

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        cnt = 0

        Key = Key.lower()
        
        
        for ch in alphabet:
                for ch2 in Key:
                    if(ch == ch2):
                        cnt = cnt + 1
        if(cnt != 25):
            key_entry.delete("1.0", tk.END)
            messagebox.showerror("Error", "Invalid key! Please insert a valid key")
        else:
            result = f"Processed text: {playfair.playfair_cipher(operation, Key, text)}"
            

    elif cipher == "Hill":
        Key = key_entry.get("1.0", tk.END).split()
        try:
            Key = list(map(int, Key))
            if(len(Key) != 4):
                key_entry.delete("1.0", tk.END)
                messagebox.showerror("Error", "Invalid key! Please insert a valid number of integers")
            else:
                det = (Key[0] * Key[3]) - (Key[1] * Key[2])
                if(math.gcd(det, 26) != 1):
                    key_entry.delete("1.0", tk.END)
                    messagebox.showerror("Error", "Invalid key! Please insert valid integers")
                else:
                    result = f"Processed text: {hill.hill_cipher(operation, Key, text)}"
        except ValueError:
            key_entry.delete("1.0", tk.END)
            messagebox.showerror("Error", "Invalid key! Please insert valid integers")

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def run_attack():
    plaintext = plaintext_entry.get("1.0", tk.END)
    ciphertext = ciphertext_entry.get("1.0", tk.END)

    if (not plaintext or not ciphertext):
        messagebox.showerror("Input error!", "Both fields are required")
        return
    if(len(plaintext) < 4 or len(ciphertext) < 4):
        messagebox.showerror("Invalid input!", "Please provide valid inputs")
        return
    
    plaintext = plaintext.lower()
    plaintext = plaintext.replace(" ", "")
    ciphertext = ciphertext.lower()
    plaintext = re.sub(r'[^a-z]', '', plaintext)
    ciphertext = re.sub(r'[^a-z]', '', ciphertext)

    found = 0
    valid_plain = ""
    valid_cipher = ""

    for i in range(0, len(plaintext)):
        if(found == 1):
            break
        else:
            for j in range(i+1, len(plaintext)):
                if(found == 1):
                    break
                else:
                    for k in range(j+1, len(plaintext)):
                        if(found == 1):
                            break
                        else:
                            for l in range(k+1, len(plaintext)):
                                base = ord('a')
                                a = ord(plaintext[i]) - base
                                b = ord(plaintext[j]) - base
                                c = ord(plaintext[k]) - base
                                d = ord(plaintext[l]) - base
                                a1 = ciphertext[i]
                                b1 = ciphertext[j]
                                c1 = ciphertext[k]
                                d1 = ciphertext[l]

                                det = ((a*d) - (b*c))

                                if(math.gcd(det, 26) == 1):
                                    
                                    valid_plain = plaintext[i] + plaintext[j] + plaintext[k] + plaintext[l]
                                    valid_cipher = a1 + b1 + c1 + d1

                                    key = hill_attack.hill_attack(valid_plain, valid_cipher)
                                    print(valid_plain)
                                    print(valid_cipher)

                                    det_key = ((key[0][0] * key[1][1]) - (key[0][1] * key[1][0]))
                                    if(math.gcd(det_key, 26) == 1):
                                        key_arr = [key[0][0], key[0][1], key[1][0], key[1][1]]
                                        cipher = hill.hill_cipher("Encrypt", key_arr, plaintext)
                                        cipher = cipher.lower()
                                        print(cipher)
                                        print(plaintext)
                                        if(cipher == ciphertext):
                                            found = 1
                                            break
                                        
                                    

    

    if(found == 0):
        plaintext_entry.delete("1.0", tk.END)
        ciphertext_entry.delete("1.0", tk.END)
        messagebox.showerror("Invalid input!", "A valid key cannot be generated with these inputs")
        return

    
    

    result_label.config(
        text=f"Recovered Key Matrix:\n[  {key[0][0]}    {key[0][1]}  ]\n[  {key[1][0]}    {key[1][1]}  ]"
    )


root = tk.Tk()
root.title("Cryptography Project")

title_font = tkfont.Font(size=14, weight="bold")

ttk.Label(
    root,
    text="Classical Cipher Tool",
    font=title_font
).pack(pady=12)
root.geometry("1920x1080")

cipher_var = tk.StringVar()
op_var = tk.StringVar()

ttk.Label(root, text="Cipher").pack()
ttk.Combobox(root, textvariable=cipher_var,
             values=["Caesar", "Affine", "Playfair", "Hill"]).pack()

ttk.Label(root, text="Operation").pack()
ttk.Combobox(root, textvariable=op_var,
             values=["Encrypt", "Decrypt"]).pack()

ttk.Label(root, text="Key").pack()
key_entry = tk.Text(root, height=2, width=100)
key_entry.pack()

ttk.Label(root, text="Input Text").pack()
input_text = tk.Text(root, height=5, width=100)
input_text.pack()

ttk.Button(root, text="Run", command=run_cipher).pack(pady=10)

ttk.Label(root, text="Output").pack()
output_text = tk.Text(root, height=5, width=100)
output_text.pack(pady = (0, 48))

ttk.Label(
    root,
    text="Plaintext Attack on Hill Cipher:",
    font=("TkDefaultFont", 14, "bold")
).pack()


# ---------- Plaintext ----------
ttk.Label(root, text="Plaintext:").pack()
plaintext_entry = tk.Text(root, height=5, width=100)
plaintext_entry.pack()



# ---------- Ciphertext ----------
ttk.Label(root, text="Ciphertext:").pack()
ciphertext_entry = tk.Text(root, height=5, width=100)
ciphertext_entry.pack()

# ---------- Button ----------
ttk.Button(
    root,
    text="Recover Key",
    command=run_attack,
    width=20
).pack(pady=10)

# ---------- Result ----------
result_label = ttk.Label(
    
    root,
    text="Recovered Key Matrix:\n",
    font=("Courier", 11),
    justify="left"
)
result_label.pack(pady=5)


root.mainloop()
