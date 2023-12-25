import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="natya",
    password="hardpass",
    database="lms"
)

mycursor = mydb.cursor()

def add_book():
    pass

def remove_book(id):
    pass

def search_book(id=None, name=None, author=None):
    pass

book_management = [add_book, remove_book, search_book]

command = ""
while command!="exit":

    print("Library Management System")
    print("1) Books management \n2) Book Issues \n3) Transactions")

    command = input("> ")

    if command == "1":
        print("\nBooks Management")
        print("1) Add Book \n2) Remove Books\n3) Search")

        command = input("> ")
        if command not in ["1", "2", "3"]:
            print("Invalid Command")
            continue
        command = int(command)-1
        book_management[command]()

