import hashlib
import tkinter as tk
from tkinter import filedialog

def md5_with_salt(data, salt):
    hashed_data = []
    for item in data:
        item_with_salt = item + salt
        hashed = hashlib.md5(item_with_salt.encode()).hexdigest()
        hashed_data.append(hashed)
    return hashed_data

def sha_no_salt(data):
    hashed_data = []
    for item in data:
        hashed = hashlib.sha1(item.encode()).hexdigest()
        hashed_data.append(hashed)
    return hashed_data

def sha_with_dig_salt(data, salt):
    hashed_data = []
    for item in data:
        item_with_salt = item + str(salt)
        hashed = hashlib.sha1(item_with_salt.encode()).hexdigest()
        hashed_data.append(hashed)
    return hashed_data

def sha_with_alphabet_salt(data, salt):
    hashed_data = []
    for item in data:
        item_with_salt = item + salt
        hashed = hashlib.sha1(item_with_salt.encode()).hexdigest()
        hashed_data.append(hashed)
    return hashed_data

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        data = [line.strip() for line in data]
    return data

def write_data_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(item + '\n')

def encrypt_data():
    selected_algorithm = algorithm_choice.get()
    input_file = filedialog.askopenfilename()
    output_file = filedialog.asksaveasfilename(defaultextension=".txt")

    data = read_data_from_file(input_file)

    if selected_algorithm == "MD5 with Salt":
        salt = salt_entry.get()
        hashed_data = md5_with_salt(data, salt)
    elif selected_algorithm == "SHA1 No Salt":
        hashed_data = sha_no_salt(data)
    elif selected_algorithm == "SHA1 with Numeric Salt":
        salt = int(salt_entry.get())
        hashed_data = sha_with_dig_salt(data, salt)
    elif selected_algorithm == "SHA1 with Alphabet Salt":
        salt = salt_entry.get()
        hashed_data = sha_with_alphabet_salt(data, salt)
    else:
        hashed_data = []

    write_data_to_file(output_file, hashed_data)
    result_label.config(text="Encryption completed.")

# Создание GUI
root = tk.Tk()
root.title("Data Encryption")

algorithm_label = tk.Label(root, text="Choose Encryption Algorithm:")
algorithm_label.pack()

algorithms = [
    "MD5 with Salt",
    "SHA1 No Salt",
    "SHA1 with Numeric Salt",
    "SHA1 with Alphabet Salt"
]
algorithm_choice = tk.StringVar(root)
algorithm_choice.set(algorithms[0])

algorithm_menu = tk.OptionMenu(root, algorithm_choice, *algorithms)
algorithm_menu.pack()

salt_label = tk.Label(root, text="Enter Salt (if applicable):")
salt_label.pack()

salt_entry = tk.Entry(root)
salt_entry.pack()

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_data)
encrypt_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()