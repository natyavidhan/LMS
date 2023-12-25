import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="natya",
    password="hardpass",
    database="lms"
)

cursor = mydb.cursor()

def add_book():
    name = input("Book name: ")
    author = input("Author name: ")
    price = input("Price: ")
    sql = "INSERT INTO books (name, author, price) VALUE (%s, %s, %s)"
    values = (name, author, price)
    cursor.execute(sql, values)
    mydb.commit()

def remove_book(id):
    pass

def search_book(id=None, name=None, author=None):
    pass

def show_books():
    cursor.execute("SELECT * from books")
    # mydb.commit()
    print("")
    for i in cursor:
        print(f"({i[0]}) {i[1]}, By {i[2]} ${i[3]}")
    print("")

book_management = [add_book, remove_book, search_book, show_books]

command = ""
while command!="exit":

    print("Library Management System")
    print("1) Books management \n2) Book Issues \n3) Transactions")

    command = input("> ")

    if command == "1":
        print("\nBooks Management")
        print("1) Add Book \n2) Remove Books \n3) Search \n4) Show All Books")

        command = input("> ")
        if command not in ["1", "2", "3", "4"]:
            print("Invalid Command")
            continue
        command = int(command)-1
        book_management[command]()

