import shower as show
from tkinter import *
from tkinter import ttk
import Checklist as c
import adder as adder
win= Tk()
win.geometry("950x400")
win.title('tasks')
def open_add():
    show.start()
def open_pen():
     adder.add_task()
def open_imp():
     c.h()
     
Label(win, text= "ALL TASKS", font= ('Helvetica 17 bold')).pack(pady=10)
ttk.Button(win, text="Open all task", command=open_add).pack(pady=5)
Label(win, text= "ADD TASKS", font= ('Helvetica 17 bold')).pack(pady=10)
ttk.Button(win, text="Open task adder", command=open_pen).pack(pady=5)
Label(win, text= "Checklist", font= ('Helvetica 17 bold')).pack(pady=10)
ttk.Button(win, text="View checklist", command=open_imp).pack(pady=5)
win.mainloop()
