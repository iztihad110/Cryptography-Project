import tkinter as tk
from tkinter import ttk, messagebox
import caesar
import affine
import playfair
import hill
import math

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

root = tk.Tk()
root.title("Classic Crypto Tool")
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
input_text = tk.Text(root, height=20, width=100)
input_text.pack()

ttk.Button(root, text="Run", command=run_cipher).pack(pady=10)

ttk.Label(root, text="Output").pack()
output_text = tk.Text(root, height=20, width=100)
output_text.pack()

root.mainloop()
