import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.configure("Treeview", background="lightblue")

table = ttk.Treeview(root)
table.pack()

# Добавление данных в таблицу
table.insert("", "end", values=("1", "John Doe", "Engineer"))
table.insert("", "end", values=("2", "Jane Smith", "Designer"))

root.mainloop()
