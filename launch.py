import os
from tkinter import *  # type: ignore
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

main_window = Tk()
main_window.title("Application")
main_window.geometry("600x400")
# Create a database connection object and cursor to interact with the database
main_window.iconbitmap("images.ico")
ico = Image.open("images.ico")
photo = ImageTk.PhotoImage(ico)
main_window.iconphoto(False, photo)


def open_Student_List():
    subprocess.Popen(["python", "main.py"])


def open_Student_Mark_System():
    subprocess.Popen(["python", "main2.py"])


def check_database():
    database_path = "university.db"
    # Check if the database file exists
    if os.path.exists(database_path):
        try:
            connection = sqlite3.connect(database_path)
            messagebox.showinfo("Database Status", "The database is connected!")
            return connection
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to connect database: {e}")
            return None
    else:
        messagebox.showerror("Error", "Database file does not exist!")
        return None


text = Label(text="Choose on option:")
text.pack(side=TOP)
Button1 = Button(main_window, text="Student List", command=open_Student_List)
Button1.pack(pady=10, side="top", padx=10, expand=False)
Button2 = Button(
    main_window, text="Student Mark System", command=open_Student_Mark_System
)
Button2.pack(pady=10, side="top", padx=10, expand=False)
Text = Label(text="Check Database").pack(pady=5)
Button3 = Button(main_window, text="Check Database", command=check_database)
Button3.pack(pady=10, side="top", padx=10, expand=False)
Text = Label(text="Kill App!")
Text.pack()
Button4 = Button(main_window, text="Kill app!", command=quit)
Button4.pack(pady=10, side="top", padx=10, expand=False)
main_window.mainloop()
# EOF
