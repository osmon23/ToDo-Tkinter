import sqlite3

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY,
        task TEXT
    )
''')
conn.commit()


def add_task():
    task = task_entry.get()
    if task:
        cursor.execute('INSERT INTO todo (task) VALUES (?)', (task,))
        conn.commit()
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning('Пустая задача', 'Пожалуйста, введите задачу.')


def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        selected_task = task_listbox.get(selected_index)
        cursor.execute('DELETE FROM todo WHERE task = ?', (selected_task,))
        conn.commit()
        task_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning('Ничего не выбрано', 'Пожалуйста, выберите задачу для удаления.')


root = ctk.CTk()
root.title('ToDo List')
root.geometry('700x400+350+100')
root.config(bg='#202020')
root.resizable(width=False, height=False)

task_label = ctk.CTkLabel(root, text='Daily Tasks', font=("Arial Bold", 30), bg_color='#202020', text_color='#ffffff')
task_label.pack(padx=20, pady=20)

frame = ctk.CTkScrollableFrame(root, width=500)
frame.pack(padx=20)

task_entry = ctk.CTkEntry(frame, width=500)
task_entry.pack()

task_listbox = tk.Listbox(frame, width=62)
task_listbox.pack()

add_button = ctk.CTkButton(root, text='Add', command=add_task, width=500)
add_button.pack(padx=20, pady=20)

delete_button = ctk.CTkButton(root, text='Delete', command=delete_task, width=500)
delete_button.pack(padx=20)

for row in cursor.execute('SELECT task FROM todo'):
    task_listbox.insert(tk.END, row[0])

root.mainloop()

conn.close()
