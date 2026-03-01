import tkinter as tk
from tkinter import ttk
import csv
from data_model import*
import threading
import random

#Last ten
def view1():
    v1=tk.Toplevel(win)
    v1.title("Last Twenty Days")
    v1.geometry("1220x450")
    v1.configure(bg="#282c34")
    lable=tk.Label(v1,text="LAST TWENTY DAYS",font=("Helventica",18,"bold"),fg="#61dafb",bg="#282c34",)
    lable.pack(pady=20)
    data=[]
    r_d=[["No","Yes"],["No priority","Moderate priority","High priority"]]
    o=open("STD10.csv",'r')
    reader=csv.reader(o)
    for i in reader:
        l=[]
        if float(i[0])>=0.85:
            l.append("Heavy Rain")
        elif float(i[0])>=0.60:
            l.append("Moderate Rain")
        elif float(i[0])>=0.40:
            l.append("Light Rain")
        else:
            l.append("No Rain")
        l.append(r_d[0][int(i[1])])
        l.append(r_d[1][int(i[2])])
        l.append(r_d[0][int(i[3])])
        if float(i[4])<=0.2:
            l.append("Friday")
        elif float(i[4])<=0.4:
            l.append("Thursday")
        elif float(i[4])<=0.6:
            l.append("Monday")
        elif float(i[4])<=0.8:
            l.append("Tuesday")
        else:
            l.append("Wednesday")
        l.append(f"{(float(i[5])*100):.2f}%")
        data.append(l)
    o.close()
    tree=ttk.Treeview(v1,columns=("Precipitation","Exam","Priority","Practical","Week","PresentPercent"),show="headings")
    tree.heading("Precipitation",text="Precipitation")
    tree.heading("Exam",text="Exam")
    tree.heading("Priority",text="Priority")
    tree.heading("Practical",text="Practical")
    tree.heading("Week",text="Week")
    tree.heading("PresentPercent",text="Present Percent")

    style=ttk.Style()
    style.configure("Treeview",font=("Arial",10),rowheight=25,foreground="white",background="#282c34",)
    style.configure("Treeview.Heading",font=("Arial",12,"bold"),foreground="#282c34",background="#61dafb",)
    tree.column("Precipitation",anchor="center")
    tree.column("Exam",anchor="center")
    tree.column("Priority",anchor="center")
    tree.column("Practical",anchor="center")
    tree.column( "Week",anchor="center")
    tree.column( "PresentPercent",anchor="center")

    for i in data:
        tree.insert("","end",values=i)
    tree.pack(fill=tk.BOTH,padx=10,pady=10)

    ttk.Button(v1,text="Exit",style="Custom.TButton",command=v1.destroy,).place(x=80,y=400)

#train
def view2():
    v2=tk.Toplevel(win)
    v2.title("Training Model")
    v2.geometry("800x400")
    v2.configure(bg="#282c34")
    lable=tk.Label(v2,text="TRAINING",font=("Helventica",18,"bold"),fg="#61dafb",bg="#282c34")
    lable.pack(pady=10)
    def loading():
        global t_out
        t_out=train(select_t.get())
        v2.after(0,stop_loading)
    def stop_loading():
        loading_label.config(text="Training Completed!")
        extv2.config(text="Exit",command=v2.destroy)
        start_training.config(state=tk.NORMAL)
        tk.Label(v2,text="Weights",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=80,y=245,width=200,height=25)
        tk.Label(v2,text=f"{t_out[0][0]:.2f}  {t_out[0][1]:.2f}  {t_out[0][2]:.2f} ",font=("Arial",12,"bold"),fg="#282c34",bg="white").place(x=300,y=245,width=200,height=25)
        tk.Label(v2,text="Bias",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=80,y=295,width=200,height=25)
        tk.Label(v2,text=f"{t_out[1]:.2f}",font=("Arial",12,"bold"),fg="#282c34",bg="white").place(x=300,y=295,width=200,height=25)
        ttk.Button(win,text="Predict Today's",style="Custom.TButton",command=view3).place(x=80,y=230)
    def update_loading_text():
        current_text=loading_label["text"]
        if current_text.endswith("..."):
            loading_label.config(text="Training")
        else:
            loading_label.config(text=current_text+".")
        if task_thread.is_alive():
            v2.after(500,update_loading_text)
    def show_loading_screen():
        start_training.config(state=tk.DISABLED)
        loading_label.config(text="Training")
        extv2.config(text="Can't Exit",command=unset)
        global task_thread
        task_thread=threading.Thread(target=loading)
        task_thread.start()
        update_loading_text()
    def unset():
        extv2.config(command=None)
    loading_label=tk.Label(v2,text='',font=("Arial",16),fg="white",bg="#282c34")
    loading_label.place(x=80,y=200)
    style=ttk.Style()
    style.configure("Custom.TRadiobutton",foreground="white",background="#282c34",font=("Arial",12))
    style.map("Custom.TRadiobutton",background=[('selected',"#282c34")])
    select_t=tk.StringVar(value="STD10.csv")
    radio_t1 = ttk.Radiobutton(v2, text="Partial Training", variable=select_t,value="STD10.csv",style="Custom.TRadiobutton")
    radio_t1.place(x=95, y=100)
    radio_t2 = ttk.Radiobutton(v2, text="Full Training", variable=select_t, value="STD.csv",style="Custom.TRadiobutton" )
    radio_t2.place(x=235, y=100)
    start_training=ttk.Button(v2,text="Start Training",style="Custom.TButton",command=show_loading_screen)
    start_training.place(x=150,y=150)
    extv2=ttk.Button(v2,text="Exit",style="Custom.TButton",command=v2.destroy,)
    extv2.place(x=80,y=350)

#Predict
def view3():
    v3=tk.Toplevel(win)
    v3.title("Predict Today's")
    v3.geometry("800x400")
    v3.configure(bg="#282c34")
    lable=tk.Label(v3,text="TODAY'S PREDICTION",font=("Helventica",18,"bold"),fg="#61dafb",bg="#282c34")
    lable.pack(pady=10)
    tk.Label(v3,text="Precipitation Chance",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=30,y=90,width=200,height=25)
    tk.Label(v3,text="Exam",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=30,y=125,width=200,height=25)
    tk.Label(v3,text="Priority",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=30,y=160,width=200,height=25)
    tk.Label(v3,text="Practical",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=30,y=195,width=200,height=25)
    tk.Label(v3,text="Day of the week",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=30,y=230,width=200,height=25)
    entry1=tk.Entry(v3,font=("Arial",12),fg="#282c34")
    entry1.place(x=250,y=90,width=200,height=25)
    style=ttk.Style()
    style.configure("Custom.TRadiobutton",foreground="white",background="#282c34",font=("Arial",12))
    style.map("Custom.TRadiobutton",background=[('selected',"#282c34")])
    select1 = tk.IntVar(value=0)
    radio1 = ttk.Radiobutton(v3, text="Yes", variable=select1,value=1,style="Custom.TRadiobutton")
    radio1.place(x=295, y=125)
    radio2 = ttk.Radiobutton(v3, text="No", variable=select1, value=0,style="Custom.TRadiobutton" )
    radio2.place(x=345, y=125)
    select2 = tk.IntVar(value=1)
    radio3 = ttk.Radiobutton(v3, text="Low", variable=select2,value=0,style="Custom.TRadiobutton")
    radio3.place(x=255, y=160)
    radio4 = ttk.Radiobutton(v3, text="Moderate", variable=select2, value=1,style="Custom.TRadiobutton" )
    radio4.place(x=305, y=160)
    radio5 = ttk.Radiobutton(v3, text="High", variable=select2, value=2,style="Custom.TRadiobutton" )
    radio5.place(x=395, y=160)
    select3 = tk.IntVar(value=0)
    radio6 = ttk.Radiobutton(v3, text="Yes", variable=select3,value=1,style="Custom.TRadiobutton")
    radio6.place(x=295, y=195)
    radio7 = ttk.Radiobutton(v3, text="No", variable=select3, value=0,style="Custom.TRadiobutton" )
    radio7.place(x=345, y=195)
    days=["Monday","Tuesday","Wednesday","Thursday","Friday"]
    entry2=ttk.Combobox(v3,values=days,state='readonly',font=("Arial",12))
    entry2.set("Choose a Day")
    entry2.place(x=250,y=230)
    def get_data():
        def update_file():
            full.pop()
            full.append(float(entrya.get())/100)
            o=open("STD.csv",'a',newline="")
            writers=csv.writer(o)
            writers.writerow(full)
            o.close()
            d=[]
            o=open("STD.csv",'r')
            reader=csv.reader(o)
            for i in reader:
                d.append(i)
            o.close()
            o=open("STD10.csv","w",newline="")
            writer=csv.writer(o)
            for i in d[-1:-21:-1]:
                writer.writerow(i)
            o.close()
            tk.Label(v3,text='Updated',font=("Arial",14),fg="white",bg="#282c34").place(x=565,y=350)
        pre=float(entry1.get())/100
        ex=int(select1.get())
        pri=int(select2.get())
        pra=int(select3.get())
        w=entry2.get().lower()
        if w=="friday":
            wv=random.uniform(0,0.2)
        elif w=="thursday":
            wv=random.uniform(0.2,0.4)
        elif w=="monday":
            wv=random.uniform(0.4,0.6)
        elif w=="tuesday":
            wv=random.uninform(0.6,0.8)
        else:
            wv=random.uniform(0.8,1)
        full=[pre,ex,pri,pra,wv]
        f_out=f_predict(full,t_out)
        tk.Label(v3,text="Student Coming",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=500,y=110,width=200,height=25)
        tk.Label(v3,text="Accuracy",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=500,y=160,width=200,height=25)
        tk.Label(v3,text=f"{f_out[0]*100:.2f}%",font=("Arial",12,"bold"),fg="#282c34",bg="white").place(x=720,y=110,width=70,height=25)
        tk.Label(v3,text=f"{f_out[1]*100:.2f}%",font=("Arial",12,"bold"),fg="#282c34",bg="white").place(x=720,y=160,width=70,height=25)
        tk.Label(v3,text="Actual",font=("Arial",12,"bold"),fg="#282c34",bg="#61dafb").place(x=500,y=210,width=70,height=25)
        entrya=tk.Entry(v3,font=("Arial",12),fg="#282c34")
        entrya.place(x=590,y=210,width=100,height=25)
        ttk.Button(v3,text="Update",style="Custom.TButton",command=update_file).place(x=550,y=300)
    ttk.Button(v3,text="Predict",style="Custom.TButton",command=get_data).place(x=80,y=300)
    ttk.Button(v3,text="Exit",style="Custom.TButton",command=v3.destroy,).place(x=80,y=350)
#main window
win=tk.Tk()
win.title("Student Attendence AI")
win.geometry("800x400")
win.configure(bg="#282c34")

lable=tk.Label(win,text="MAIN MENU",font=("Helventica",18,"bold"),fg="#61dafb",bg="#282c34",)
lable.pack(pady=20)

style=ttk.Style()
style.theme_use("clam")
style.configure("Custom.TButton",font=("Arial",11,"bold"),foreground="#282c34",background="#61dafb",borderwidth=2,relief='solid',highlightthickness=2,highlightbackground="black",highlightcolor="black",)

view1=ttk.Button(win,text="View Last Twenty Days",style="Custom.TButton",command=view1).place(x=80,y=130)
view2=ttk.Button(win,text="Train The Model",style="Custom.TButton",command=view2).place(x=80,y=180)

ext=ttk.Button(win,text="Exit",style="Custom.TButton",command=win.destroy,).place(x=80,y=280)

win.mainloop()
