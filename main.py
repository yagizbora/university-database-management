from os import name
import select
from tkinter import *  # type: ignore
from tkinter import ttk
import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox


main_window = Tk()
main_window.title("Öğrencilerin listesinin ekranı")
main_window.geometry("1000x720")
#ico = Image.open("images.ico")
#photo = ImageTk.PhotoImage(ico)
#main_window.iconphoto(False, photo)
#

def connect():
    con = sqlite3.connect("university.db")
    cursor = con.cursor()
    con.commit()
    con.close()


def View():
    try:
     Tree.delete(*Tree.get_children())
     con1 = sqlite3.connect("university.db")
     cur1 = con1.cursor()
     cur1.execute("SELECT * FROM Student_List")
     rows = cur1.fetchall()
     for row in rows:
         # print(row)  # Sadece veri göremez isen yorum satırından çıkar #
         Tree.insert("", tk.END, values=row)
    except sqlite3.DatabaseError as f: 
     messagebox.showerror("Error", f"Database error: {f}")
     con1.close()
     connect()


# Front End
def add_students_window():
    top = Toplevel()
    top.title("Add Students")
    top.geometry("300x200")

    name_surname_label = Label(top, text="Enter the name and surname of the student")
    name_surname_label.pack()

    name_surname_var = StringVar()
    name_surname_entry = Entry(top, textvariable=name_surname_var)
    name_surname_entry.insert(0, "")
    name_surname_entry.pack()

    grade_label = Label(top, text="Enter the grade of student")
    grade_label.pack()

    grade_var = StringVar()
    grade_entry = Entry(top, textvariable=grade_var)
    grade_entry.insert(0, "")
    grade_entry.pack()

    date_label = Label(top, text="Enter the student's university entrance date")
    date_label.pack()

    date_var = StringVar()
    date_entry = Entry(top, textvariable=date_var)
    date_entry.insert(0, "")
    date_entry.pack()

    submit_button = Button(
        top,
        text="Submit",
        command=lambda: add_students(
            name_surname_var.get(), grade_var.get(), date_var.get()
        ),
    )
    submit_button.pack()


def EditStudents():
    top = Toplevel()
    top.title("Edit Students")
    top.geometry("300x200")

    id_label = Label(top, text="Enter the ID of the student you want to edit:")
    id_label.pack()
    id_entry = Entry(top)
    id_entry.pack()

    name_label = Label(top, text="Enter the new student's name:")
    name_label.pack()
    name_entry = Entry(top)
    name_entry.pack()

    grade_label = Label(top, text="Enter the new grade")
    grade_label.pack()
    grade_entry = Entry(top)
    grade_entry.pack()

    date_label = Label(top, text="Enter the new entrance date")
    date_label.pack()
    date_entry = Entry(top)
    date_entry.pack()

    submit_button = Button(
        top,
        text="Submit",
        command=lambda: edit_student(
            id_entry.get(), name_entry.get(), grade_entry.get(), date_entry.get()
        ),
    )
    submit_button.pack()


# Back End
def add_students(name_surname, grade_entry, date_entry):
    try:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Student_List (Name_Surname,Grade,Date) VALUES(?,?,?)",
            (
                name_surname,
                grade_entry,
                date_entry,
            ),
        )
        conn.commit()
        messagebox.showinfo("Success!", "Operation is successful!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")

        # Assuming you have a View() function to refresh the Treeview
    View()


def edit_student(id, name_entry, grade_entry, date_entry):
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    sql_query = (
        "UPDATE Student_List SET Name_Surname = ?, Grade = ?, Date = ? WHERE id = ?"
    )

    try:
        cursor.execute(sql_query, (name_entry, grade_entry, date_entry, id))
        conn.commit()
        View()
        messagebox.showinfo("Success", "Student updated successfully!")
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {sql_query}")
        print(f"Error details: {e}")
    finally:
        conn.close()


def delete_student():
    connection = sqlite3.connect("university.db")
    cursor = connection.cursor()

    try:
        selected_item = Tree.selection()[0]
        selected_student = Tree.item(selected_item)["values"]

        if messagebox.askokcancel(
            "Confirm Deletion",
            f"Are you sure you want to delete the student '{selected_student[1]}' from the database?",
        ):
            Tree.delete(selected_item)
            student_id = selected_student[
                0
            ]  # Assuming the student ID is in the first position
            cursor.execute("DELETE FROM Student_List WHERE ID = ?", (student_id,))
            connection.commit()
            messagebox.showinfo(
                "Success", "Student has been deleted from the database."
            )
        else:
            messagebox.showinfo("Cancelled", "The deletion was cancelled.")
    except IndexError as e:
        messagebox.showerror("Error", "Please select a student to delete.")
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An unexpected error occurred. Please try again.\nError details: {e}",
        )


Tree = ttk.Treeview(main_window, columns=("c1", "c2", "c3", "c4"), show="headings")
Tree.column("#1", anchor="center")
Tree.heading("#1", text="id")
Tree.column("#2", anchor="center")
Tree.heading("#2", text="NameSurname")
Tree.column("#3", anchor="center")
Tree.heading("#3", text="Grade")
Tree.column("#4", anchor="center")
Tree.heading("#4", text="Date")
verscrlbar = ttk.Scrollbar(main_window, orient="vertical", command=Tree.yview)
verscrlbar.pack(side="left", fill="y", expand=False)
Tree.pack(side="left", fill=BOTH, expand=True)
Button1 = tk.Button(main_window, text="Display Students", command=View)
Button1.pack(pady=10, side="top", padx=10, expand=False)
Button2 = tk.Button(main_window, text="Edit Students", command=EditStudents)
Button2.pack(pady=10, side="top", padx=10, expand=False)
Button3 = tk.Button(main_window, text="Add Students", command=add_students_window)
Button3.pack(pady=10, side="top", padx=10, expand=False)
Button4 = tk.Button(main_window, text="Delete Students", command=delete_student)
Button4.pack(pady=10, side="top", padx=10, expand=False)
Button5 = tk.Button(main_window, text="Kill App", command=quit)
Button5.pack(side="right", pady=10, padx=10, expand=True)
main_window.mainloop()
# EOF
