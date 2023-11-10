from tkinter import *
import tkinter
def newcheck(ba):
	global m
	global a
	global b
	global to
	global changeval
	m+=1
	to=Frame(top)
	done=IntVar()
	txt=ba.get()
	ba.delete(0,END)
	a=Label(to,text=txt,bg="#fff")
	ha=Checkbutton(to,variable=done,onvalue=3,offvalue=1,height=5,width=5)
	ha.grid(row=0,column=0)
	b=Button(to,text="x",command=lambda: [a.destroy(),b.destroy(),to.destroy(),globals().update(m=m-1)])
	a.grid(row=0,column =1)
	b.grid(row=0,column=2)
	to.grid(row=m,column=columnval)
def ch(to):
	global n
	col=to.grid_info().get("column")
	col=2 if col==1 else 1
	to.grid(column=col)
	n+=1
def h():
        global top
        global ti
        global m
        global n
        global columnval
        top = tkinter.Tk()
        top.title("Checklist of Tasks")
        top.geometry("950x250")
        ti=Label(top,text="Checklist of tasks",font=("Arial 7"))
        ti.grid(row=0,column=1)
        i=Label(top,text="                ")
        n=IntVar()
        m=2
        columnval=1
        n=1
        task=["task1",n]
        entry=Entry(top)
        add=Button(top,text="+",font=("Arial",10),command=lambda: newcheck(entry))
        i.grid(row=1,column=0)
        entry.grid(row=1,column=0)
        add.grid(row=1,column=2)
        tc=Label(top,text="Completed",font=("Arial 7"))
        tc.grid(row=0,column=3)
        top.mainloop()
