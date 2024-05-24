import sqlite3

con1 = sqlite3.connect("university.db")
cur1 = con1.cursor()
cur1.execute("SELECT * FROM Student_List")
rows = cur1.fetchall()
print(rows)
con1.close()
