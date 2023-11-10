import sqlite3 as sq
connection=sq.connect("Task.db")
cursor=connection.cursor()
'''cursor.execute("""CREATE TABLE task (
    task_name VARCHAR(255),
    description VARCHAR(255),
    urgency INT,
    target_date DATE,
    due_date DATE
)""")'''
def read_table():
    cursor.execute('SELECT * FROM task')
    rows = cursor.fetchall()
    list_of_lists = []
    for row in rows:
        list_of_lists.append(list(row))
    return list_of_lists
def write_to_table(list_of_lists):
    for inner_list in list_of_lists:
        task_name = inner_list[0]
        description = inner_list[1]
        urgency = inner_list[2]
        target_date = inner_list[3]
        due_date = inner_list[4]
        cursor.execute("INSERT INTO task (task_name, description, urgency, target_date, due_date) VALUES (?, ?, ?, ?, ?)", (task_name, description, urgency, target_date, due_date))
        connection.commit()
a=read_table()
print(a)
