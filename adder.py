from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import SqliteHelper as sq
values = []
def add_to_list():
    global task_name_entry
    global description_entry
    global urgency_entry
    global due_date_entry
    global target_date_entry
    global add_button
    global values
    task_name = task_name_entry.get()
    task_name_entry.delete(0,END)
    description = description_entry.get()
    description_entry.delete(0,END)
    urgency = urgency_entry.get()
    urgency_entry.delete(0,END)
    target_date = target_date_entry.get()
    target_date_entry.delete(0,END)
    due_date = due_date_entry.get()
    due_date_entry.delete(0,END)
    values.append([task_name, description, urgency, target_date, due_date])
    sq.write_to_table(values)
    values=[]
def add_task():
    MyFrame= Tk()
    MyFrame.geometry("550x350")
    global task_name_entry
    global description_entry
    global urgency_entry
    global due_date_entry
    global target_date_entry
    global add_button
    ttk.Label(MyFrame,font=("Arial 20"), text="Introduction", background="#ffffff").grid(row=1, column=2, sticky="w")
    Canvas(MyFrame, height=1, background="#a0a0a0", highlightthickness=0, highlightbackground="white").grid(row=1, column=3, columnspan=3, sticky="we")
    task_name_l=ttk.Label(MyFrame,text="Enter task name:",width=30)
    task_name_l.grid(row=3,column=2)
    task_name_entry = ttk.Entry(MyFrame, width=20)
    task_name_entry.grid(row=3, column=3)
    description_l=ttk.Label(MyFrame,text="Enter task description:",width=30)
    description_l.grid(row=4,column=2)
    description_entry = ttk.Entry(MyFrame, width=20)
    description_entry.grid(row=4, column=3)
    urgency_l=ttk.Label(MyFrame,text="Enter task urgency:",width=30)
    urgency_l.grid(row=5,column=2)
    urgency_entry = ttk.Entry(MyFrame,width=20)
    urgency_entry.grid(row=5,column=3)
    target_l=ttk.Label(MyFrame,text="Enter target date:",width=30)
    target_l.grid(row=6,column=2)
    target_date_entry = DateEntry(MyFrame,width=20,date_pattern='yyyy-mm-dd')
    target_date_entry.grid(row=6,column=3)
    due_l=ttk.Label(MyFrame,text="Enter due date:",width=30)
    due_l.grid(row=7,column=2)
    due_date_entry = DateEntry(MyFrame,width=20,date_pattern='yyyy-mm-dd')
    due_date_entry.grid(row=7,column=3)
    add_button = ttk.Button(MyFrame,text="Add Task",command=add_to_list)
    add_button.grid(row=8,columnspan=2,pady=(10))
    MyFrame.mainloop()
