#Fadil: Tarun if you're reading this, try to understand what is happening here. Ok bye
import mysql.connector as msc

db=msc.connect(host ="localhost",user="root",password="root",database="bookshop")       #Fadil: Establishing connection
cursor=db.cursor()      #Fadil: Creating cursor

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
    #updating books
    book_id = input("Enter the book ID to update: ")
    print("\nWhat would you like to update?")
    print("1. Book Name")
    print("2. Author")
    print("3. Price")
    print("4. Stock")
    choice = input("Enter your choice: ")
    if choice == '1':
        new_name = input("Enter the new book name: ")
        cursor.execute("UPDATE books SET book_name = %s WHERE book_id = %s", (new_name, book_id))
    elif choice == '2':
        new_author = input("Enter the new author: ")
        cursor.execute("UPDATE books SET book_author = %s WHERE book_id = %s", (new_author, book_id))
    elif choice == '3':
        new_price = float(input("Enter the new price: "))
        cursor.execute("UPDATE books SET cost = %s WHERE book_id = %s", (new_price, book_id))
    elif choice == '4':
        new_stock = int(input("Enter the new stock quantity: "))
        cursor.execute("UPDATE books SET stock = %s WHERE book_id = %s", (new_stock, book_id))
    else:
        print("Invalid choice. Try again.")
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

def AddPurchase():
    c_id=input("\nEnter customer ID: ")
    c_n=input("Enter name of customer: ")
    c_p=input("Enter customer phone number: ")
    n=int(input("Enter number of books purchased: "))
    for i in range(n):
        print(i+1, ". ", sep='',end='')         #Fadil: This statement for neatness
        b_id=input("Enter book ID: ")
        cursor.execute("select book_name from books where book_id="+b_id)       #Fadil: Fetching name of book using ID
        b_n=cursor.fetchone()[0]        #Fadil: Saving book name to a variable
        cursor.execute('insert into sales values('+b_id+',"'+b_n+'",'+c_id+','+c_p+',"'+c_n+'")')
        db.commit()         #Fadil: Committing (Saving) the values
        print("record added sucessfully")

def EditSales():
    b_id=input("\nEnter Book ID: ")
    c_id=input("Enter Customer ID: ")
    print("\nWhat would you like to edit?")
    print("1. Book ID")
    print("2. Customer ID")
    print("3.Customer phone")
    print("4. Customer name")
    c3=input("Enter your choice: ")
    if c3=='1':
        nb_id=input("Enter new Book ID: ")
        cursor.execute("select book_name from books where book_id="+nb_id)
        nb_n=cursor.fetchone()[0]           #Fadil: Getting the name of book using book id. Same thing I did for adding record
        cursor.execute('update sales set book_id='+nb_id+', book_name="'+nb_n+'" where book_id='+b_id+' and customer_id='+c_id)         #Fadil: Updating Values. Here I'm doing for both book ID and book name using only book ID
        db.commit()
        print("Record added sucessfully")
    elif c3=='2':
        nc_id=input("Enter new Customer ID: ")
        cursor.execute('update sales set customer_id='+nc_id+' where book_id='+b_id+' and customer_id='+c_id)
                #Fadil: More updating values
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
        #Fadil: Code is working without errors (I think)
        #Fadil: Siddharth remind me to add a new column named 'Date' in the sales table

def DeleteSalesRecord():
    print("\n1. Choose and delete")
    print("2. Delete all records")
    c3=input("Enter your choice: ")
    if c3=='1':
        b_id=input("\nEnter Book ID: ")
        c_id=input("Enter Customer ID: ")
        cursor.execute('select * from sales where book_id='+b_id+' and customer_id='+c_id)          #Fadil: This part is to show what is being deleted
        L=cursor.fetchone()
        print("\nBook ID:", L[0])
        print("Book Name:", L[1])
        print("Customer ID:", L[2])
        print("Customer phone:", L[3])
        print("Customer name:", L[4])
        c4=input("Are you sure you want to delete this record? (y/n): ")
        if c4=='y':
            cursor.execute('delete from sales where book_id='+b_id+' and customer_id='+c_id)
            db.commit()         #Fadil: db.commit() here is not a good idea (or anywhere else). For now I'm going to keep it here but will be removed later and added as a seperate option when the user is choosing. That way any mistakes can be undoed
            print("Record deleted sucessfully")
        elif c3=='2':
            c4=input("Are you sure you want to delete all records? (y/n): ")
            if c4=='y':
                cursor.execute('delete from sales')
                db.commit()
                print("Record(s) deleted sucessfully")

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
        #Fadil: Cool searching thing I made using the LIKE operator in SQL
        c4=input("Enter your choice: ")
        if c4=='1':
            c5=input("Enter Book ID: ")
            cursor.execute('select * from sales where book_id like "%'+c5+'%"')         #Fadil: Basically takes the value and uses the LIKE operator to find something similiar to what the user entered
        elif c4=='2':
            c5=input("Enter Book name: ")
            cursor.execute('select * from sales where book_name like "%'+c5+'%"')
        elif c4=='3':
            c5=input("Enter Customer ID: ")
            cursor.execute('select * from sales where customer_id like "%'+c5+'%"')
        elif c4=='4':
            c5=input("Enter Customer phone: ")
            cursor.execute('select * from sales where customer_phone like "%'+c5+'%"')
        elif c4=='5':
            c5=input("Enter Customer name: ")
            cursor.execute('select * from sales where customer_name like "%'+c5+'%"')
        L=cursor.fetchall()
        #Fadil: I did not expect this to work but damn it works
        for i in L:
            print("\nBook ID:", i[0])
            print("Book Name:", i[1])
            print("Customer ID:", i[2])
            print("Customer phone:", i[3])
            print("Customer name:", i[4])
    elif c3=='2':
        cursor.execute("select * from sales")
        L=cursor.fetchall()
        for i in L:
            print("\nBook ID:", i[0])
            print("Book Name:", i[1])
            print("Customer ID:", i[2])
            print("Customer phone:", i[3])
            print("Customer name:", i[4])


print(db)       #Fadil: Checking connection. Not required
print("[Insert Welcome text]")      #Fadil: Ignore this for now
ch_books={1: AddRecord, 2: UpdateRecord, 3: DeleteBooksRecord, 4: DisplayStock}
ch_sales={1: AddPurchase, 2: EditSales, 3: DeleteSalesRecord, 4: DisplaySales}

while True:
    #Fadil: while loop for the user to do things
    print("\n--------------------------------------------")
    print("MAIN MENU")
    print("--------------------------------------------")
    print("Choose table:")
    print("1. Books")
    print("2. Sales")
    print("3. Exit")
    c=input("Enter your choice: ")
    if c=='1':
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
        
        #Fadil: Siddharth add some if else elif statements so that these things do something
        #Fadil: Only work on the part of the code that is related with the 'books' table. The 'sales' table is my work and I'll do it
        #Siddharth: I have done the books part but i need help witth the back option
    elif c=='2':
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
    else:
        break
