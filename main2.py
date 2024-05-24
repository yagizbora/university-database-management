from tkinter import *  # type: ignore
from tkinter import ttk
import sqlite3
from tkinter import Button
from tkinter import messagebox
from PIL import Image, ImageTk

main_window = Tk()
main_window.title("Ders giriş ekranı")
main_window.geometry("1000x720")
main_window.iconbitmap("images.ico")
ico = Image.open("images.ico")
photo = ImageTk.PhotoImage(ico)
main_window.iconphoto(False, photo)


def connect():
    try:
        connection = sqlite3.connect("university.db")
        return connection
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        return None


def fetch_and_insert_data(table_name, Tree):
    connection = connect()
    cursor = connection.cursor()  # type: ignore
    sql_query = f"SELECT * FROM {table_name};"
    cursor.execute(sql_query)

    rows = cursor.fetchall()

    Tree.delete(*Tree.get_children())

    for row in rows:
        Tree.insert("", "end", values=row)

    connection.close()  # type: ignore


def fetch_table_names():
    connection = connect()
    cursor = connection.cursor()  # type: ignore

    try:
        # Exclude sqlite_sequence table
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        )
        table_names = [row[0] for row in cursor.fetchall()]
        return table_names
    except sqlite3.Error as e:
        print("Error fetching table names:", e)
        return []
    finally:
        connection.close()  # type: ignore


def combobox_fetch_tables(*args):
    selected_table = combobox.get()
    if selected_table:
        fetch_and_insert_data(selected_table, Tree)


current_var = StringVar()
current_var.trace_add("write", combobox_fetch_tables)

combobox = ttk.Combobox(main_window, textvariable=current_var)
combobox.pack()


# Front End
def AddDataForStudents_window():
    top = Toplevel()
    top.title("Add Students")
    top.geometry("300x300")

    Student_Number_Label = Label(top, text="Enter the number of student")
    Student_Number_Label.pack()
    Student_Number_var = IntVar()
    Student_Number = Entry(top, textvariable=Student_Number_var)
    Student_Number.insert(0, "")
    Student_Number.pack()

    name_surname_label = Label(top, text="Enter the name and surname of the student")
    name_surname_label.pack()
    name_surname_var = StringVar()
    name_surname_entry = Entry(top, textvariable=name_surname_var)
    name_surname_entry.insert(0, "")
    name_surname_entry.pack()

    MidTerm_Label = Label(top, text="Enter the MidTerm grade")
    MidTerm_Label.pack()
    MidTerm_var = IntVar()
    MidTerm_Entry = Entry(top, textvariable=MidTerm_var)
    MidTerm_Entry.insert(0, "")
    MidTerm_Entry.pack()

    Final_Exam_Label = Label(top, text="Enter the Final Exam grade")
    Final_Exam_Label.pack()
    Final_Exam_var = IntVar()
    Final_Exam_Entry = Entry(top, textvariable=Final_Exam_var)
    Final_Exam_Entry.insert(0, "")
    Final_Exam_Entry.pack()

    Project_Label = Label(top, text="Enter the Project grade")
    Project_Label.pack()
    Project_var = IntVar()
    Project_Entry = Entry(top, textvariable=Project_var)
    Project_Entry.insert(0, "")
    Project_Entry.pack()

    submit_button = Button(
        top,
        text="Submit",
        command=lambda: AddDataForStudents(
            Student_Number_var.get(),
            name_surname_entry.get(),
            MidTerm_Entry.get(),
            Final_Exam_Entry.get(),
            Project_Entry.get(),
        ),
    )
    submit_button.pack()  # Add this line to pack the submit_button

    top.mainloop()


def EditDataofstudentsmark_window():
    top = Toplevel()
    top.title("Edit Students")
    top.geometry("300x300")

    Student_Number_Label = Label(top, text="Enter the number of student")
    Student_Number_Label.pack()
    Student_Number_var = IntVar()
    Student_Number = Entry(top, textvariable=Student_Number_var)
    Student_Number.insert(0, "")
    Student_Number.pack()

    name_surname_label = Label(top, text="Enter the name and surname of the student")
    name_surname_label.pack()
    name_surname_var = StringVar()
    name_surname_entry = Entry(top, textvariable=name_surname_var)
    name_surname_entry.insert(0, "")
    name_surname_entry.pack()

    MidTerm_Label = Label(top, text="Enter the MidTerm grade")
    MidTerm_Label.pack()
    MidTerm_var = IntVar()
    MidTerm_Entry = Entry(top, textvariable=MidTerm_var)
    MidTerm_Entry.insert(0, "")
    MidTerm_Entry.pack()

    Final_Exam_Label = Label(top, text="Enter the Final Exam grade")
    Final_Exam_Label.pack()
    Final_Exam_var = IntVar()
    Final_Exam_Entry = Entry(top, textvariable=Final_Exam_var)
    Final_Exam_Entry.insert(0, "")
    Final_Exam_Entry.pack()

    Project_Label = Label(top, text="Enter the Project grade")
    Project_Label.pack()
    Project_var = IntVar()
    Project_Entry = Entry(top, textvariable=Project_var)
    Project_Entry.insert(0, "")
    Project_Entry.pack()

    submit_button = Button(
        top,
        text="Submit",
        command=lambda: UpdateMarks(
            Student_Number_var.get(),
            name_surname_entry.get(),
            MidTerm_Entry.get(),
            Final_Exam_Entry.get(),
            Project_Entry.get(),
        ),
    )
    submit_button.pack()

    top.mainloop()


# BackEnd
def AddDataForStudents(
    Student_Number, name_surname, MidTerm_Entry, Final_exam, Project_Entry
):
    try:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()

        # Get the selected table name from the combobox
        selected_table = combobox.get()

        # Construct and execute the SQL INSERT query
        query = f"INSERT INTO {selected_table} (Student_Number, Name_Surname, MidTerm, Final_Exam, Project) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(
            query,
            (Student_Number, name_surname, MidTerm_Entry, Final_exam, Project_Entry),
        )
        conn.commit()
        messagebox.showinfo("Message", "Operation is successful")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()  # type: ignore


def delete_student():
    connection = sqlite3.connect("university.db")
    cursor = connection.cursor()

    try:
        selected_item = Tree.selection()[0]
        table_names = fetch_table_names()

        if not table_names:
            messagebox.showerror("Error", "No tables found in the database.")
            return

        selected_table = (
            combobox.get()
        )  # Assuming you want to delete from the first table
        print(f"Selected Table: {selected_table}")

        selected_student = Tree.item(selected_item)["values"]

        if messagebox.askokcancel(
            "Confirm Deletion",
            f"Are you sure you want to delete the student '{selected_student[1]}' from the database?",
        ):
            Tree.delete(selected_item)
            student_id = selected_student[0]
            # Assuming the student ID is in the first position
            cursor.execute(
                f"DELETE FROM {selected_table} WHERE Student_Number = ?", (student_id,)
            )
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
    finally:
        connection.close()


def UpdateMarks(Student_Number, Name_Surname, MidTerm, Final_Exam, Project):
    con = sqlite3.connect("university.db")
    cursor = con.cursor()
    try:
        selected_table = combobox.get()
        # Use placeholders in the UPDATE statement and provide the values in the execute method
        cursor.execute(
            f"UPDATE {selected_table} SET Name_Surname=?, MidTerm=?, Final_Exam=?, Project=? WHERE Student_Number=?",
            (Name_Surname, MidTerm, Final_Exam, Project, Student_Number),
        )
        con.commit()
        messagebox.showinfo("Success", "Marks have been updated.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        con.close()


def Updatetreeview():
    con = sqlite3.connect("university.db")
    cursor = con.cursor()

    Tree.delete(*Tree.get_children())  # Clear existing data

    selected_table = combobox.get()

    if selected_table:
        try:
            sql_query = f"SELECT * FROM {selected_table}"
            cursor.execute(
                sql_query,
            )
            rows = cursor.fetchall()

            for row in rows:
                Tree.insert("", "end", value=row)  # type: ignore
        except sqlite3.Error as e:
            messagebox.showerror(
                "Failed to fetch data from table: " + selected_table, "\n" + str(e)
            )
    else:
        messagebox.showinfo("Don't Forget!", "Select the table")

    con.close()


# Create a Tkinter window
# Functions for displaying and managing tree views
Tree = ttk.Treeview(
    main_window, columns=("c1", "c2", "c3", "c4", "c5"), show="headings"
)
Tree.column("#1", anchor="center")
Tree.heading("#1", text="Student Number")
Tree.column("#2", anchor="center")
Tree.heading("#2", text="Name_Surname")
Tree.column("#3", anchor="center")
Tree.heading("#3", text="MidTerm")
Tree.column("#4", anchor="center")
Tree.heading("#4", text="Final Exam")
Tree.column("#5", anchor="center")
Tree.heading("#5", text="Project")
verscrlbar = ttk.Scrollbar(main_window, orient="vertical", command=Tree.yview)
verscrlbar.pack(side="left", fill="y", expand=False)
Tree.pack()
Button1 = Button(main_window, text="Add Students", command=AddDataForStudents_window)
Button1.pack(pady=10, side="top", padx=10, expand=False)
EditButton = Button(
    main_window, text="Edit Data", command=EditDataofstudentsmark_window
)
EditButton.pack(pady=10, side="top", padx=10, expand=False)
DeleteButton = Button(main_window, text="Delete Students", command=delete_student)
DeleteButton.pack(pady=10, side="top", padx=10, expand=False)
Updatetree = Button(main_window, text="Refresh data", command=Updatetreeview)
Updatetree.pack(pady=10, side="top", padx=10, expand=False)
# Populate combobox with table names
table_names = fetch_table_names()
combobox["values"] = table_names
main_window.mainloop()
# EOF
