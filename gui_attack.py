import tkinter as tk
from tkinter import messagebox
import math
import hill_attack
import hill
import re

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
root.title("Hill Cipher Plaintext–Ciphertext Attack")
root.geometry("500x500")

# ---------- Plaintext ----------
tk.Label(root, text="Plaintext:").grid(
    row=0, column=0, padx=10, pady=5, sticky="e"
)

plaintext_entry = tk.Text(root, height=1, width=40)
plaintext_entry.grid(row=0, column=1, padx=10, pady=5)

# ---------- Ciphertext ----------
tk.Label(root, text="Ciphertext:").grid(
    row=1, column=0, padx=10, pady=5, sticky="e"
)

ciphertext_entry = tk.Text(root, height=1, width=40)
ciphertext_entry.grid(row=1, column=1, padx=10, pady=5)

# ---------- Button ----------
tk.Button(
    root,
    text="Recover Key",
    command=run_attack,
    width=20
).grid(row=2, column=0, columnspan=2, pady=10)

# ---------- Result ----------
result_label = tk.Label(
    root,
    text="Recovered Key Matrix:\n",
    font=("Courier", 11),
    justify="left"
)
result_label.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
