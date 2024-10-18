import mysql.connector as msc
import random
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

try:
    db=msc.connect(host ="localhost",user="root",password="root",database="bookshop")
    cursor=db.cursor()
except:
    db=msc.connect(host ="localhost",user="root",password="root")
    cursor=db.cursor()
    cursor.execute('create database bookshop')
    cursor.execute('use bookshop')
    cursor.execute('create table books (book_id int, book_name varchar(30), book_author varchar(30), supplier varchar(30), cost decimal(8,2), stock int)')
    cursor.execute('create table sales (sale_id int, customer_firstname varchar(30), customer_lastname varchar(30), customer_phone int, book_id int, book_name varchar(30), datetime datetime)')
    db.commit()

print(db)

def Erase():
    j=0
    for i in w.winfo_children():
        if j<2:
            j+=1
        else:
            i.destroy()

def AddSales():
    Erase()
    
    def Output():
        if ec_fn.get() and ec_ln.get():
            try:
                b_id = int(eb_id.get())
                cursor.execute(f'select book_name from books where book_id={b_id}')
                b_n=cursor.fetchone()[0]
                try:
                    s_id=random.randint(1000000,9999999)
                    dt=str(datetime.datetime.now())[:-7]
                    c_p = int(ec_p.get())
                    c_fn = ec_fn.get()
                    c_ln = ec_ln.get()
                    cursor.execute('select sale_id from sales')
                    L=cursor.fetchall()
                    while True:
                        if (s_id,) in L:
                            s_id=random.randint(1000000,9999999)
                        else:
                            break
                    cursor.execute(f'insert into sales values ({s_id},"{c_fn}","{c_ln}",{c_p},{b_id},"{b_n}","{dt}")')
                    db.commit()

                    messagebox.showinfo("Info", "Record added successfully")
                    eb_id.delete(0,tk.END)
                    ec_p.delete(0,tk.END)
                    ec_fn.delete(0,tk.END)
                    ec_ln.delete(0,tk.END)
                except ValueError:
                    messagebox.showerror("Error", "Invalid value found. Please try again")
                    eb_id.delete(0,tk.END)
                    ec_p.delete(0,tk.END)
                    ec_fn.delete(0,tk.END)
                    ec_ln.delete(0,tk.END)
            except TypeError:
                messagebox.showerror("Error", "No Book found with that ID. Please try again")
                eb_id.delete(0,tk.END)
                ec_p.delete(0,tk.END)
                ec_fn.delete(0,tk.END)
                ec_ln.delete(0,tk.END)
        else:
            messagebox.showerror("Error", "Please enter the data")
            eb_id.delete(0,tk.END)
            ec_p.delete(0,tk.END)
            ec_fn.delete(0,tk.END)
            ec_ln.delete(0,tk.END)

    tb_id=tk.Label(w,relief=tk.FLAT,text='Enter Book ID :')
    tb_id.grid(row=2,column=0)
    tc_p=tk.Label(w,relief=tk.FLAT,text="Enter Customer's phone number :")
    tc_p.grid(row=3,column=0)
    tc_fn=tk.Label(w,relief=tk.FLAT,text="Enter Customer's First name :")
    tc_fn.grid(row=4,column=0)
    tc_ln=tk.Label(w,relief=tk.FLAT,text="Enter Customer's Last name :")
    tc_ln.grid(row=5,column=0)
    eb_id=tk.Entry(w,relief=tk.SUNKEN)
    eb_id.grid(row=2,column=1)
    ec_p=tk.Entry(w,relief=tk.SUNKEN)
    ec_p.grid(row=3,column=1)
    ec_fn=tk.Entry(w,relief=tk.SUNKEN)
    ec_fn.grid(row=4,column=1)
    ec_ln=tk.Entry(w,relief=tk.SUNKEN)
    ec_ln.grid(row=5,column=1)
    but=tk.Button(w,text="Enter",command=Output)
    but.grid(row=7,column=0,sticky="nsew")

def UpdateSaleData():
    Erase()
    
    def Output():
        
        def Update():
            if eb_id.get() or ec_p.get() or ec_fn.get() or ec_ln.get():
                if eb_id.get():
                    try:
                        b_id=int(eb_id.get())
                        cursor.execute(f'select book_name from books where book_id={b_id}')
                        b_n=cursor.fetchone()[0]
                        cursor.execute(f'update sales set book_id={b_id}, book_name="{b_n}"where sale_id={s_id}')
                    except:
                        messagebox.showerror("Error", "Error. Book ID not updated. Enter a valid value")
                        eb_id.delete(0,tk.END)
                        ec_p.delete(0,tk.END)
                        ec_fn.delete(0,tk.END)
                        ec_ln.delete(0,tk.END)
                if ec_p.get():
                    try:
                        c_p=int(ec_p.get())
                        cursor.execute(f'update sales set customer_phone="{c_p}" where sale_id={s_id}')
                    except ValueError:
                        messagebox.showerror("Error", "Error. Customer phone number not updated. Enter a valid value")
                        eb_id.delete(0,tk.END)
                        ec_p.delete(0,tk.END)
                        ec_fn.delete(0,tk.END)
                        ec_ln.delete(0,tk.END)
                if ec_fn.get():
                    c_fn=ec_fn.get()
                    cursor.execute(f'update sales set customer_firstname={c_fn} where sale_id={s_id}')
                if ec_ln.get():
                    c_ln=ec_ln.get()
                    cursor.execute(f'update sales set customer_lastname={c_ln} where sale_id={s_id}')
                    
                db.commit()
                messagebox.showinfo("Info", "Record(s) updated successfully")
                menubooks.menu.invoke(2)
            else:
                messagebox.showerror("Error", "Please enter the data to update")
                eb_id.delete(0,tk.END)
                ec_p.delete(0,tk.END)
                ec_fn.delete(0,tk.END)
                ec_ln.delete(0,tk.END)
        try:
            s_id=int(es_id.get())
            cursor.execute(f'select * from sales where sale_id={s_id}')
            L=cursor.fetchone()
            if L:
                Erase()
                tb_id=tk.Label(w,relief=tk.FLAT,text='Sale ID')
                tb_id.grid(row=2,column=0)
                tc_fn=tk.Label(w,relief=tk.FLAT,text='Customer First name')
                tc_fn.grid(row=2,column=1)
                tc_ln=tk.Label(w,relief=tk.FLAT,text='Customer Last name')
                tc_ln.grid(row=2,column=2)
                tc_p=tk.Label(w,relief=tk.FLAT,text='Customer phone')
                tc_p.grid(row=2,column=3)
                tb_id=tk.Label(w,relief=tk.FLAT,text='Book ID')
                tb_id.grid(row=2,column=4)
                tb_n=tk.Label(w,relief=tk.FLAT,text='Book Name')
                tb_n.grid(row=2,column=5)
                tdt=tk.Label(w,relief=tk.FLAT,text='Date & Time')
                tdt.grid(row=2,column=6)
                for i in range(len(L)):
                    info=tk.Label(w,relief=tk.FLAT,text=L[i])
                    info.grid(row=3,column=i)
                
                tb_id=tk.Label(w,relief=tk.FLAT,text='Enter Book ID :')
                tb_id.grid(row=6,column=0)
                tc_p=tk.Label(w,relief=tk.FLAT,text="Enter Customer's phone :")
                tc_p.grid(row=7,column=0)
                tc_fn=tk.Label(w,relief=tk.FLAT,text="Enter Customer's First name :")
                tc_fn.grid(row=8,column=0)
                tc_ln=tk.Label(w,relief=tk.FLAT,text="Enter Customer's Last name :")
                tc_ln.grid(row=9,column=0)
                eb_id=tk.Entry(w,relief=tk.SUNKEN)
                eb_id.grid(row=6,column=1)
                ec_p=tk.Entry(w,relief=tk.SUNKEN)
                ec_p.grid(row=7,column=1)
                ec_fn=tk.Entry(w,relief=tk.SUNKEN)
                ec_fn.grid(row=8,column=1)
                ec_ln=tk.Entry(w,relief=tk.SUNKEN)
                ec_ln.grid(row=9,column=1)
                text=tk.Label(w,relief=tk.FLAT,text='Choose what to update (Leave empty to not update)')
                text.grid(row=5,column=1)
                but=tk.Button(w,text='Update',command=Update)
                but.grid(row=10,column=1)
            else:
                messagebox.showerror("Error", "Record not found")
                es_id.delete(0,tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid value. Please try again")
            es_id.delete(0,tk.END)
        

    es_id=tk.Entry(w,relief=tk.SUNKEN)
    es_id.grid(row=2,column=1)
    ts_id=tk.Label(w,relief=tk.FLAT,text='Enter Sale ID :')
    ts_id.grid(row=2,column=0)
    but=tk.Button(w,text='Enter',command=Output)
    but.grid(row=2,column=2,sticky="nsew")

def DeleteSaleRecord():
    Erase()
    
    def Output():
        
        def Delete():
            cursor.execute(f'delete from sales where sale_id={s_id}')
            db.commit()
            messagebox.showinfo("Info", "Record deleted successfully")
            menubooks.menu.invoke(3)
        def DontDelete():
            messagebox.showinfo("Info", "Record was not deleted")
            menubooks.menu.invoke(3)
        try:
            s_id=int(es_id.get())
            cursor.execute(f'select * from sales where sale_id={s_id}')
            L=cursor.fetchone()
            if L:
                Erase()
                tb_id=tk.Label(w,relief=tk.FLAT,text='Sale ID')
                tb_id.grid(row=2,column=0)
                tc_fn=tk.Label(w,relief=tk.FLAT,text='Customer First name')
                tc_fn.grid(row=2,column=1)
                tc_ln=tk.Label(w,relief=tk.FLAT,text='Customer Last name')
                tc_ln.grid(row=2,column=2)
                tc_p=tk.Label(w,relief=tk.FLAT,text='Customer phone')
                tc_p.grid(row=2,column=3)
                tb_id=tk.Label(w,relief=tk.FLAT,text='Book ID')
                tb_id.grid(row=2,column=4)
                tb_n=tk.Label(w,relief=tk.FLAT,text='Book Name')
                tb_n.grid(row=2,column=5)
                tdt=tk.Label(w,relief=tk.FLAT,text='Date & Time')
                tdt.grid(row=2,column=6)
                for i in range(len(L)):
                    info=tk.Label(w,relief=tk.FLAT,text=L[i])
                    info.grid(row=3,column=i)

                text=tk.Label(w,relief=tk.FLAT,text='Are you sure you want to delete this record?')
                text.grid(row=5,column=0)
                but1=tk.Button(w,text='Yes',command=Delete)
                but1.grid(row=5, column=1)
                but2=tk.Button(w,text='No',command=DontDelete)
                but2.grid(row=5, column=2)
            else:
                messagebox.showerror("Error", "Record not found")
                ebook_id.delete(0,tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid value. Please try again")
            ebook_id.delete(0,tk.END)
    
    es_id=tk.Entry(w,relief=tk.SUNKEN)
    es_id.grid(row=2,column=1)
    ts_id=tk.Label(w,relief=tk.FLAT,text='Enter Sale ID :')
    ts_id.grid(row=2,column=0)
    but=tk.Button(w,text='Enter',command=Output)
    but.grid(row=2,column=2,sticky="nsew")

def DisplaySales():
    Erase()
    def Output():
        def ssaleid():
            nonlocal found
            try:
                found=False
                s_id=int(evalue.get())
                cursor.execute(f'select * from sales where sale_id like "%{s_id}%"')
                nonlocal S
                S=cursor.fetchall()
                if S:
                    found=True
            except ValueError:
                messagebox.showerror("Error", "Invalid value. Please try again")
                evalue.delete(0,tk.END)
                found=False
        def scustomerfname():
            nonlocal found
            found=False
            c_fn=evalue.get()
            cursor.execute(f'select * from sales where customer_firstname like "%{c_fn}%"')
            nonlocal S
            S=cursor.fetchall()
            if S:
                found=True
        def scustomerlname():
            nonlocal found
            found=False
            c_ln=evalue.get()
            cursor.execute(f'select * from sales where customer_lastname like "%{c_ln}%"')
            nonlocal S
            S=cursor.fetchall()
            if S:
                found=True
        def scustomerphone():
            nonlocal found
            try:
                found=False
                c_p=int(evalue.get())
                cursor.execute(f'select * from sales where customer_phone like "%{c_p}%"')
                nonlocal S
                S=cursor.fetchall()
                if S:
                    found=True
            except ValueError:
                messagebox.showerror("Error", "Invalid value. Please try again")
                evalue.delete(0,tk.END)
                found=False
        def sbookid():
            nonlocal found
            try:
                found=False
                b_id=int(evalue.get())
                cursor.execute(f'select * from sales where book_id like "%{b_id}%"')
                nonlocal S
                S=cursor.fetchall()
                if S:
                    found=True
            except ValueError:
                messagebox.showerror("Error", "Invalid value. Please try again")
                evalue.delete(0,tk.END)
                found=False
        choice={1:ssaleid,2:scustomerfname,3:scustomerlname,4:scustomerphone,5:sbookid}
        print(rval.get())
        try:
            choice[rval.get()]()
        except KeyError:
            cursor.execute('select * from sales')
            S=cursor.fetchall()
            found=True
        evalue.delete(0,tk.END)
        
        if found:
            T=tk.Toplevel()
            T.title('Records')
            scroll= tk.Scrollbar(T)
            scroll.pack(side=tk.RIGHT,fill=tk.Y)
            columns=('customerfname','customerlname','customerphone','bookid','bookname','date')
            tree=ttk.Treeview(T,columns=columns,yscrollcommand=scroll.set)
            tree.pack()
            scroll.config( command = tree.yview )

            tree.heading('#0',text='Sale ID')
            tree.heading('customerfname',text='Customer First name')
            tree.heading('customerlname',text='Customer Last name')
            tree.heading('customerphone',text='Customer phone')
            tree.heading('bookid',text='Book ID')
            tree.heading('bookname',text='Book name')
            tree.heading('date',text='Date & time')

            for i in S:
                tree.insert('',tk.END,text=f"{i[0]}",values=i[1:])
        else:
            messagebox.showerror("Error", "No records found")
    rval= tk.IntVar()
    tvalue=tk.Label(w,relief=tk.FLAT,text='Enter value to search :')
    tvalue.grid(row=2,column=0)
    evalue=tk.Entry(w,relief=tk.SUNKEN)
    evalue.grid(row=2,column=1)
    r1=tk.Radiobutton(w, text='Sale ID',variable=rval,value=1)
    r1.grid(row=3,column=0)
    r2=tk.Radiobutton(w, text='Customer first name',variable=rval,value=2)
    r2.grid(row=3,column=1)
    r3=tk.Radiobutton(w, text='Customer last name',variable=rval,value=3)
    r3.grid(row=3,column=2)
    r4=tk.Radiobutton(w, text='Customer phone',variable=rval,value=4)
    r4.grid(row=3,column=3)
    r5=tk.Radiobutton(w, text='Book ID',variable=rval,value=5)
    r5.grid(row=3,column=3)
    but=tk.Button(w,text='Search',command=Output)
    but.grid(row=2,column=2)


def AddRecord():
    Erase()
    
    def Output():
        if eb_n.get() and eb_a.get():
            try:
                b_id=random.randint(1000,9999)
                b_n = eb_n.get()
                b_a = eb_a.get()
                b_c = float(eb_c.get())
                b_s = int(eb_s.get())
                sup = esup.get()
                cursor.execute('select book_id from books')
                L=cursor.fetchall()
                while True:
                    if (b_id,) in L:
                        b_id=random.randint(1000,9999)
                    else:
                        break
                cursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s)",(b_id, b_n, b_a, sup, b_c, b_s))
                db.commit()
                messagebox.showinfo("Info", "Record added successfully")
                eb_n.delete(0,tk.END)
                eb_a.delete(0,tk.END)
                eb_c.delete(0,tk.END)
                eb_s.delete(0,tk.END)
                esup.delete(0,tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid value found. Please try again")
                eb_n.delete(0,tk.END)
                eb_a.delete(0,tk.END)
                eb_c.delete(0,tk.END)
                eb_s.delete(0,tk.END)
                esup.delete(0,tk.END)
        else:
            messagebox.showerror("Error", "Please enter the data")
            eb_n.delete(0,tk.END)
            eb_a.delete(0,tk.END)
            eb_c.delete(0,tk.END)
            eb_s.delete(0,tk.END)
            esup.delete(0,tk.END)

    tb_n=tk.Label(w,relief=tk.FLAT,text='Enter Book Name :')
    tb_n.grid(row=2,column=0)
    tb_a=tk.Label(w,relief=tk.FLAT,text='Enter Author Name :')
    tb_a.grid(row=3,column=0)
    tb_c=tk.Label(w,relief=tk.FLAT,text='Enter Cost :')
    tb_c.grid(row=4,column=0)
    tb_s=tk.Label(w,relief=tk.FLAT,text='Enter Stock :')
    tb_s.grid(row=5,column=0)
    tsup=tk.Label(w,relief=tk.FLAT,text='Enter Supplier :')
    tsup.grid(row=6,column=0)
    eb_n=tk.Entry(w,relief=tk.SUNKEN)
    eb_n.grid(row=2,column=1)
    eb_a=tk.Entry(w,relief=tk.SUNKEN)
    eb_a.grid(row=3,column=1)
    eb_c=tk.Entry(w,relief=tk.SUNKEN)
    eb_c.grid(row=4,column=1)
    eb_s=tk.Entry(w,relief=tk.SUNKEN)
    eb_s.grid(row=5,column=1)
    esup=tk.Entry(w,relief=tk.SUNKEN)
    esup.grid(row=6,column=1)
    but=tk.Button(w,text="Enter",command=Output)
    but.grid(row=8,column=0,sticky="nsew")

def UpdateBookData():
    Erase()
    
    def Output():
        
        def Update():
            if eb_n.get() or eb_a.get() or eb_c.get() or eb_s.get() or esup.get():
                if eb_n.get():
                    b_n=eb_n.get()
                    cursor.execute(f'update books set book_name="{b_n}" where book_id={b_id}')
                if eb_a.get():
                    b_a=eb_a.get()
                    cursor.execute(f'update books set book_author="{b_a}" where book_id={b_id}')
                if eb_c.get():
                    try:
                        b_c=float(eb_c.get())
                        cursor.execute(f'update books set cost={b_c} where book_id={b_id}')
                    except:
                        messagebox.showerror("Error", "Error. Enter a valid value")
                        eb_n.delete(0,tk.END)
                        eb_a.delete(0,tk.END)
                        eb_c.delete(0,tk.END)
                        eb_s.delete(0,tk.END)
                if eb_s.get():
                    try:
                        b_s=int(eb_s.get())
                        cursor.execute(f'update books set stock={b_s} where book_id={b_id}')
                    except:
                        messagebox.showerror("Error", "Error. Enter a valid value")
                        eb_n.delete(0,tk.END)
                        eb_a.delete(0,tk.END)
                        eb_c.delete(0,tk.END)
                        eb_s.delete(0,tk.END)
                
                db.commit()
                messagebox.showinfo("Info", "Record updated successfully")
                menubooks.menu.invoke(2)
            else:
                messagebox.showerror("Error", "Please enter the data to update")
                eb_n.delete(0,tk.END)
                eb_a.delete(0,tk.END)
                eb_c.delete(0,tk.END)
                eb_s.delete(0,tk.END)
        try:
            b_id=int(eb_id.get())
            cursor.execute(f'select * from books where book_id={b_id}')
            L=cursor.fetchone()
            if L:
                Erase()
                tb_id=tk.Label(w,relief=tk.FLAT,text='Book ID')
                tb_id.grid(row=2,column=0)
                tb_n=tk.Label(w,relief=tk.FLAT,text='Book Name')
                tb_n.grid(row=2,column=1)
                tb_a=tk.Label(w,relief=tk.FLAT,text='Author')
                tb_a.grid(row=2,column=2)
                tsup=tk.Label(w,relief=tk.FLAT,text='Supplier')
                tsup.grid(row=2,column=3)
                tb_c=tk.Label(w,relief=tk.FLAT,text='Cost')
                tb_c.grid(row=2,column=4)
                tb_s=tk.Label(w,relief=tk.FLAT,text='Stock')
                tb_s.grid(row=2,column=5)
                for i in range(len(L)):
                    info=tk.Label(w,relief=tk.FLAT,text=L[i])
                    info.grid(row=3,column=i)
                
                tbook_name=tk.Label(w,relief=tk.FLAT,text='Enter Book Name :')
                tbook_name.grid(row=6,column=0)
                tauthor=tk.Label(w,relief=tk.FLAT,text='Enter Author Name :')
                tauthor.grid(row=7,column=0)
                tcost=tk.Label(w,relief=tk.FLAT,text='Enter Cost :')
                tcost.grid(row=8,column=0)
                tstock=tk.Label(w,relief=tk.FLAT,text='Enter Stock :')
                tstock.grid(row=9,column=0)
                tsupplier=tk.Label(w,relief=tk.FLAT,text='Enter Supplier :')
                tsupplier.grid(row=10,column=0)
                eb_n=tk.Entry(w,relief=tk.SUNKEN)
                eb_n.grid(row=6,column=1)
                eb_a=tk.Entry(w,relief=tk.SUNKEN)
                eb_a.grid(row=7,column=1)
                eb_c=tk.Entry(w,relief=tk.SUNKEN)
                eb_c.grid(row=8,column=1)
                eb_s=tk.Entry(w,relief=tk.SUNKEN)
                eb_s.grid(row=9,column=1)
                esup=tk.Entry(w,relief=tk.SUNKEN)
                esup.grid(row=10,column=1)
                text=tk.Label(w,relief=tk.FLAT,text='Choose what to update (Leave empty to not update)')
                text.grid(row=5,column=1)
                but=tk.Button(w,text='Update',command=Update)
                but.grid(row=12,column=1)
            else:
                messagebox.showerror("Error", "Record not found")
                eb_id.delete(0,tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid value. Please try again")
            eb_id.delete(0,tk.END)
        

    eb_id=tk.Entry(w,relief=tk.SUNKEN)
    eb_id.grid(row=2,column=1)
    tb_id=tk.Label(w,relief=tk.FLAT,text='Enter Book ID :')
    tb_id.grid(row=2,column=0)
    but=tk.Button(w,text='Enter',command=Output)
    but.grid(row=2,column=2,sticky="nsew")

def DeleteBookRecord():
    Erase()
    def Output():
        def Delete():
            cursor.execute(f'delete from books where book_id={b_id}')
            db.commit()
            messagebox.showinfo("Info", "Record deleted successfully")
            menubooks.menu.invoke(3)
        def DontDelete():
            messagebox.showinfo("Info", "Record was not deleted")
            menubooks.menu.invoke(3)
        try:
            book_id=int(ebook_id.get())
            cursor.execute(f'select * from books where book_id={b_id}')
            L=cursor.fetchone()
            if L:
                Erase()
                tb_id=tk.Label(w,relief=tk.FLAT,text='Book ID')
                tb_id.grid(row=2,column=0)
                tb_n=tk.Label(w,relief=tk.FLAT,text='Book Name')
                tb_n.grid(row=2,column=1)
                tb_a=tk.Label(w,relief=tk.FLAT,text='Author')
                tb_a.grid(row=2,column=2)
                tsup=tk.Label(w,relief=tk.FLAT,text='Supplier')
                tsup.grid(row=2,column=3)
                tb_c=tk.Label(w,relief=tk.FLAT,text='Cost')
                tb_c.grid(row=2,column=4)
                tb_s=tk.Label(w,relief=tk.FLAT,text='Stock')
                tb_s.grid(row=2,column=5)
                for i in range(len(L)):
                    info=tk.Label(w,relief=tk.FLAT,text=L[i])
                    info.grid(row=3,column=i)

                text=tk.Label(w,relief=tk.FLAT,text='Are you sure you want to delete this record?')
                text.grid(row=5,column=0)
                but1=tk.Button(w,text='Yes',command=Delete)
                but1.grid(row=5, column=1)
                but2=tk.Button(w,text='No',command=DontDelete)
                but2.grid(row=5, column=2)
            else:
                messagebox.showerror("Error", "Record not found")
                ebook_id.delete(0,tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid value. Please try again")
            ebook_id.delete(0,tk.END)
    
    eb_id=tk.Entry(w,relief=tk.SUNKEN)
    eb_id.grid(row=2,column=1)
    tb_id=tk.Label(w,relief=tk.FLAT,text='Enter Book ID :')
    tb_id.grid(row=2,column=0)
    but=tk.Button(w,text='Enter',command=Output)
    but.grid(row=2,column=2,sticky="nsew")

def DisplayStock():
    Erase()
    def Output():
        def sbookid():
            nonlocal found
            try:
                found=False
                b_id=int(evalue.get())
                cursor.execute(f'select * from books where book_id like "%{b_id}%"')
                nonlocal S
                S=cursor.fetchall()
                if S:
                    found=True
            except ValueError:
                messagebox.showerror("Error", "Invalid value. Please try again")
                evalue.delete(0,tk.END)
                found=False
        def sbookname():
            nonlocal found
            found=False
            b_n=evalue.get()
            cursor.execute(f'select * from books where book_name like "%{b_n}%"')
            nonlocal S
            S=cursor.fetchall()
            if S:
                found=True
        def sbookauthor():
            nonlocal found
            found=False
            b_a=evalue.get()
            cursor.execute(f'select * from books where book_author like "%{b_a}%"')
            nonlocal S
            S=cursor.fetchall()
            if S:
                found=True
        def ssupplier():
            nonlocal found
            found=False
            sup=evalue.get()
            cursor.execute(f'select * from books where supplier like "%{sup}%"')
            nonlocal S
            S=cursor.fetchall()
            if S:
                found=True
        choice={1:sbookid,2:sbookname,3:sbookauthor,4:ssupplier}
        print(rval.get())
        try:
            choice[rval.get()]()
        except KeyError:
            cursor.execute('select * from books')
            S=cursor.fetchall()
            found=True
        evalue.delete(0,tk.END)
        
        if found:
            T=tk.Toplevel()
            T.title('Records')
            scroll= tk.Scrollbar(T)
            scroll.pack(side=tk.RIGHT,fill=tk.Y)
            columns=('bookname','bookauthor','supplier','cost','stock')
            tree=ttk.Treeview(T,columns=columns,yscrollcommand=scroll.set)
            tree.pack()
            scroll.config( command = tree.yview )

            tree.heading('#0',text='Book ID')
            tree.heading('bookname',text='Book name')
            tree.heading('bookauthor',text='Author')
            tree.heading('supplier',text='Supplier')
            tree.heading('cost',text='Cost')
            tree.heading('stock',text='Stock')

            for i in S:
                tree.insert('',tk.END,text=f"{i[0]}",values=i[1:])
        else:
            messagebox.showerror("Error", "No records found")
    rval= tk.IntVar()
    tvalue=tk.Label(w,relief=tk.FLAT,text='Enter value to search :')
    tvalue.grid(row=2,column=0)
    evalue=tk.Entry(w,relief=tk.SUNKEN)
    evalue.grid(row=2,column=1)
    r1=tk.Radiobutton(w, text='Book ID',variable=rval,value=1)
    r1.grid(row=3,column=0)
    r2=tk.Radiobutton(w, text='Book name',variable=rval,value=2)
    r2.grid(row=3,column=1)
    r3=tk.Radiobutton(w, text='Book author',variable=rval,value=3)
    r3.grid(row=3,column=2)
    r4=tk.Radiobutton(w, text='Supplier',variable=rval,value=4)
    r4.grid(row=3,column=3)
    but=tk.Button(w,text='Search',command=Output)
    but.grid(row=2,column=2)


w=tk.Tk(className='Application')
#w.geometry("500x350")
w.rowconfigure([0,1,2,3,4,5,6,7,8,9,10,11,12],minsize=25,)
w.columnconfigure([0,1,2,3,4,5,6,7],minsize=50,)

bframe = tk.Frame(w, relief = tk.RAISED,borderwidth=2)
menubooks = tk.Menubutton(bframe, text = "Books")
bframe.grid(row=0, column=0,sticky="nsew")
menubooks.pack()
menubooks.menu = tk.Menu(menubooks)
menubooks["menu"]=menubooks.menu
menubooks.menu.add_radiobutton(label = "Add Record",command=AddRecord)
menubooks.menu.add_radiobutton(label = "Update Record",command=UpdateBookData)
menubooks.menu.add_radiobutton(label = "Delete Book Record",command=DeleteBookRecord)
menubooks.menu.add_radiobutton(label = "Display Stock",command=DisplayStock)

sframe= tk.Frame(w, relief = tk.RAISED,borderwidth=2)
menusales = tk.Menubutton(sframe, text = "Sales")
sframe.grid(row=0, column=1,sticky="nsew")
menusales.pack()
menusales.menu = tk.Menu(menusales)
menusales["menu"]=menusales.menu
menusales.menu.add_radiobutton(label = "Add new purchase",command=AddSales)
menusales.menu.add_radiobutton(label = "Edit sales",command=UpdateSaleData)
menusales.menu.add_radiobutton(label = "Delete Sales Record",command=DeleteSaleRecord)
menusales.menu.add_radiobutton(label = "Display Sales",command=DisplaySales)


w.mainloop()
