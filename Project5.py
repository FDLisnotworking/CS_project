
import mysql.connector as msc
import random
import datetime

db=msc.connect(host ="localhost",user="root",password="root",database="bookshop")       #Fadil: Establishing connection
cursor=db.cursor()      #Fadil: Creating cursor

def Books():

    def AddRecord():
        #Adding books
        book_id = input("Enter book ID: ")
        book_name = input("Enter book name: ")
        author = input("Enter author: ")
        cost = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        # Secure SQL query using parameterized statements
        cursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s, %s)",(book_id, book_name, stock, cost, author))
        db.commit()
        print("Book record added successfully.")
    
    def UpdateRecord():
    
        def BooksUpdateName():
            new_name = input("Enter the new book name: ")
            cursor.execute("UPDATE books SET book_name = %s WHERE book_id = %s", (new_name, book_id))
        def BooksUpdateAuthor():
            new_author = input("Enter the new author: ")
            cursor.execute("UPDATE books SET book_author = %s WHERE book_id = %s", (new_author, book_id))
        def BooksUpdatePrice():
            new_price = float(input("Enter the new price: "))
            cursor.execute("UPDATE books SET cost = %s WHERE book_id = %s", (new_price, book_id))
        def BooksUpdateStock():
            new_stock = int(input("Enter the new stock quantity: "))
            cursor.execute("UPDATE books SET stock = %s WHERE book_id = %s", (new_stock, book_id))
        
        ch_updateb={1: BooksUpdateName, 2: BooksUpdateAuthor, 3: BooksUpdatePrice, 4: BooksUpdateStock}
        #updating books
        book_id = input("Enter the book ID to update: ")
        print("\nWhat would you like to update?")
        print("1. Book Name")
        print("2. Author")
        print("3. Price")
        print("4. Stock")
        c = input("Enter your choice: ")
        try:
            c=int(c)
        except ValueError:
            pass
        try:
            ch_updateb[c]()
        except KeyError:
            print("Invalid choice.")
        db.commit()
        print("Book record updated successfully.")

    def DeleteBooksRecord():
        #deleting books
        book_id = input("Enter the book ID to delete: ")
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        db.commit()
        print("Book record deleted successfully.")

    def DisplayStock():
        #displaying stock
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        if books:
            for book in books:
                print(f"\nBook ID: {book[0]}")
                print(f"Book Name: {book[1]}")
                print(f"Author: {book[2]}")
                print(f"Price: {book[3]}")
                print(f"Stock: {book[4]}")
            else:
                print("No books found.")

    ch_books={1: AddRecord, 2: UpdateRecord, 3: DeleteBooksRecord, 4: DisplayStock}

    print("\nChoose an action:")
    print("1. Add records")
    print("2. Update records")
    print("3. Delete records")
    print("4. Display stock")
    print("5. Back")
    c2=input("Enter your choice: ")
    try:
        c2=int(c2)
    except ValueError:
        pass
    try:
        ch_books[c2]()
    except KeyError:
        print("Invalid choice")

def Sales():
    
    def AddPurchase():
        cursor.execute("select customer_id from sales")
        L=cursor.fetchall()
        c_exid=[]
        s_id=1000000
        if L:
            for i in L:
                c_exid.append(i[0])
            cursor.execute("select max(sale_id) from books")
            s_id=cursor.fetchone()[0]+1

        while True:
            try:
                c_id=input("Enter customer ID: ")
                c_id=int(c_id)
                break
            except ValueError:
                if c_id.lower()=='r':
                    while True:
                        c_id=random.randint(10000,99999)
                        if c_id not in c_exid:
                            break
                else:
                    print("Error. Please enter a valid value")
            try:
                if c_id not in c_exid:
                    c_fn=input("Enter First name of customer: ")
                    c_ln=input("Enter Last name of customer: ")
                    c_p=int(input("Enter customer phone number: "))
                    n=int(input("Enter number of books purchased: "))
                break
            except ValueError:
                print("Error. Please enter a valid value")
        for i in range(n):
            while True:
                try:
                    print(i+1, ". ", sep='',end='')                 # This statement for neatness
                    b_id=int(input("Enter book ID: "))
                    break
                except ValueError:
                    print("Enter a valid number")
            cursor.execute(f"select book_name from books where book_id={b_id}")       # Fetching name of book using ID
            b_n=cursor.fetchone()[0]        # Saving book name to a variable
            dt = str(datetime.datetime.now())[:-7]
            cursor.execute(f'insert into sales values({b_id},"{b_n}",{c_id},{c_p},{s_id},"{c_fn}","{c_ln}","{dt}")')
            db.commit()
            print("record added sucessfully")

    def EditSales():
        b_id=input("\nEnter Book ID: ")
        c_id=input("Enter Customer ID: ")
        print("\nWhat would you like to edit?")
        print("1. Book ID/name")
        print("2. Customer ID")
        print("3. Customer phone")
        print("4. Customer name")
        c3=input("Enter your choice: ")
        if c3=='1':
            nb_id=input("Enter new Book ID: ")
            cursor.execute("select book_name from books where book_id="+nb_id)
            nb_n=cursor.fetchone()[0]
            cursor.execute('update sales set book_id='+nb_id+', book_name="'+nb_n+'" where book_id='+b_id+' and customer_id='+c_id)
            db.commit()
            print("Record added sucessfully")
        elif c3=='2':
            nc_id=input("Enter new Customer ID: ")
            cursor.execute('update sales set customer_id='+nc_id+' where book_id='+b_id+' and customer_id='+c_id)
            db.commit()
            print("Record added sucessfully")
        elif c3=='3':
            nc_p=input("Enter new Customer phone: ")
            cursor.execute('update sales set customer_phone='+nc_p+' where book_id='+b_id+' and customer_id='+c_id)
            db.commit()
            print("Record added sucessfully")
        elif c3=='4':
            nc_n=input("Enter new Customer name: ")
            cursor.execute('update sales set customer_name="'+nc_n+'" where book_id='+b_id+' and customer_id='+c_id)
            db.commit()
            print("Record added sucessfully")

    def DeleteSalesRecord():
        print("\n1. Choose and delete")
        print("2. Delete all records")
        c3=input("Enter your choice: ")
        if c3=='1':
            b_id=input("\nEnter Book ID: ")
            c_id=input("Enter Customer ID: ")
            cursor.execute('select * from sales where book_id='+b_id+' and customer_id='+c_id)
            L=cursor.fetchone()
            print("\nBook ID:", L[0])
            print("Book Name:", L[1])
            print("Customer ID:", L[2])
            print("Customer phone:", L[3])
            print("Customer name:", L[4])
            c4=input("Are you sure you want to delete this record? (y/n): ")
            if c4=='y':
                cursor.execute('delete from sales where book_id='+b_id+' and customer_id='+c_id)
                db.commit()
                print("Record deleted sucessfully")
            else:
                print("Record not deleted")
        elif c3=='2':
            c4=input("Are you sure you want to delete all records? (y/n): ")
            if c4=='y':
                cursor.execute('delete from sales')
                db.commit()
                print("Record(s) deleted sucessfully")
            else:
                print("Record(s) not deleted")

    def DisplaySales():
        print("\n1. Search for record")
        print("2. Show all records")
        c3=input("Enter your choice: ")
        if c3=='1':
            print("\nSearch using:")
            print("1. Book ID")
            print("2. Book name")
            print("3. Customer ID")
            print("4.Customer phone")
            print("5. Customer name")
            c4=input("Enter your choice: ")
            if c4=='1':
                c5=input("Enter Book ID: ")
                cursor.execute(f'select * from sales where book_id like "%{c5}%"')
            elif c4=='2':
                c5=input("Enter Book name: ")
                cursor.execute(f'select * from sales where book_name like "%{c5}%"')
            elif c4=='3':
                c5=input("Enter Customer ID: ")
                cursor.execute(f'select * from sales where customer_id like "%{c5}%"')
            elif c4=='4':
                c5=input("Enter Customer phone: ")
                cursor.execute(f'select * from sales where customer_phone like "%{c5}%"')
            elif c4=='5':
                c5=input("Enter Customer name: ")
                cursor.execute(f'select * from sales where customer_name like "%{c5}%"')
            L=cursor.fetchall()
            if not L:
                print("No records found")
            else:
                for i in L:
                    print(f"""\nBook ID: {i[0]}
Book Name: {i[1]}
Customer ID: {i[2]}
Customer phone: {i[3]}
Sale ID: {i[4]}
Customer First name: {i[5]}
Customer Last name: {i[6]}
Date & Time: {i[7]}""")
        elif c3=='2':
            cursor.execute("select * from sales")
            L=cursor.fetchall()
            if not L:
                print("No records found")
            else:
                for i in L:
                    print(f"""\nBook ID: {i[0]}
Book Name: {i[1]}
Customer ID: {i[2]}
Customer phone: {i[3]}
Sale ID: {i[4]}
Customer First name: {i[5]}
Customer Last name: {i[6]}
Date & Time: {i[7]}""")
                
    ch_sales={1: AddPurchase, 2: EditSales, 3: DeleteSalesRecord, 4: DisplaySales}
    
    print("\nChoose an action:")
    print("1. Add new purchase")
    print("2. Edit sales")
    print("3. Delete records")
    print("4. Display sales")
    print("5. Back")
    c2=input("Enter your choice: ")
    try:
        c2=int(c2)
    except ValueError:
        pass
    try:
        ch_sales[c2]()
    except KeyError:
        print("Invalid choice")

ch_main={1: Books, 2: Sales}

print(db)
print("[Insert Welcome text]")


while True:
    #Fadil: while loop for the user to do things
    print("""\n--------------------------------------------
MAIN MENU
--------------------------------------------
Choose table:
1. Books
2. Sales
3. Exit""")
    c=input("Enter your choice: ")
    try:
        c=int(c)
    except ValueError:
        pass
    try:
        ch_main[c]()
    except KeyError:
        if c==3:
            print("Thank you for using the Application")
            break
        else:
            print("Invalid choice")
