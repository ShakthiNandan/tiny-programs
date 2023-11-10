from tkinter import *
import tkinter as tk
import SqliteHelper as sq
def start():
    data=sq.read_table()
    root=Tk()
    root.geometry("950x250")
    root.title("EISENHOWER MATRIX")
    headers = ['Task Name', 'Description', 'Urgency', 'Target Date', 'Due Date']
    for j, header in enumerate(headers):
        label = tk.Label(root, text=header)
        label.grid(row=0, column=j)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            label = tk.Label(root, text=value)
            label.grid(row=i+1, column=j)
    root.mainloop()
