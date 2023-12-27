import mysql.connector
import datetime
import json

mydb = mysql.connector.connect(host="localhost", user="natya", password="hardpass", database="lms")
cursor = mydb.cursor()

def _print_books(books):
    print("")
    for i in books: print(f"({i[0]}) {i[1]}, By {i[2]} ${i[3]}")

def _search_book(val, classifier):
    cursor.execute(f"SELECT * from books WHERE {classifier}=%s", (val, ))
    return [i for i in cursor]

def _get_issues():
    cursor.execute("SELECT * from issues")
    return [i for i in cursor]

def add_book():
    cursor.execute("INSERT INTO books (name, author, price) VALUE (%s, %s, %s)", (input("Book name: "), input("Author name: "), input("Price: ")))
    mydb.commit()

def remove_book():
    cursor.execute("DELETE from books WHERE id=%s", (input("Enter Book ID > "), ))
    mydb.commit()

def search_book():
    print("\nSearch with \n1) ID \n2) Name \n3) Author")
    command = input("> ")
    if command not in ["1", "2", "3"]:
        print("Invalid Input")
        search_book()
        return
    books = _search_book(input("Enter query > "), ["id", "name", "author"][int(command)-1])
    _print_books(books)

def show_books():
    cursor.execute("SELECT * from books")
    _print_books(cursor)

def issue_book():
    command = input("Book ID > ")
    book = _search_book(command, "id")
    if len(book) == 0:
        print(f"Book with ID {command} not found")
        issue_book()
        return
    book = book[0]
    print(f"{book[1]}, By {book[2]} ${book[3]}")
    print("Is this the correct book?")
    command = input("(y/n) > ")
    if command == "n": issue_book(); return
    name = input("Student Name > ")
    ret = input("Return in (days) > ")
    cursor.execute("INSERT INTO issues (student, book_id, issued_on, return_in) VALUES (%s, %s, CURDATE(), %s)", (name, book[0], ret))
    mydb.commit()

def return_book():
    issue_id = input("Issue ID > ")
    cursor.execute("SELECT * from issues WHERE id=%s", (issue_id, ))
    issues = [i for i in cursor]
    if len(issues) == 0:
        print("Invalid ID")
        return_book()
        return
    if issues[0][5]: print("Book already Returned"); return
    cursor.execute("UPDATE issues SET returned=True WHERE id=%s", (issue_id, ))
    mydb.commit()

def show_issues():
    issues = _get_issues()
    print("")
    for i in issues:
        book = _search_book(i[2], "id")[0]
        print(f"({i[0]}) {book[1]}, Issued By {i[1]} on {i[3]} for {i[4]} days ({'Returned' if i[5] else 'Not Returned'})")

def check_dues():
    issues = _get_issues()
    print("")
    for i in issues:
        date = i[3]+datetime.timedelta(days=int(i[4]))
        if not i[5] and datetime.date.today() > date: print(f"({i[0]}) {_search_book(i[2], "id")[0][1]}, Issued By {i[1]} on {i[3]} for {i[4]} days ({'Returned' if i[5] else 'Not Returned'})")

def new_transaction():
    student = input("Student Name > ")
    amt = int(input("Number of books purchased > "))
    books = json.dumps([input(f"Enter Book {i+1} ID > ") for i in range(amt)])

    cursor.execute("INSERT INTO transactions (student, book_ids, purchased_on) VALUES (%s, %s, CURDATE())", (student, books))
    mydb.commit()

def transaction_history():
    cursor.execute("SELECT * FROM transactions")
    for i in cursor: print(f"({i[0]}) {i[1]} purchased {len(json.loads(i[2]))} Book(s) on {i[3]}")

def show_transaction():
    id = input("Enter Transaction ID > ")
    cursor.execute("SELECT * FROM transactions WHERE id=%s", (id, ))
    trs = [i for i in cursor]
    if len(trs) == 0:
        print("Invalid Transaction ID")
        show_transaction()
        return
    tr = trs[0]
    books = [_search_book(i, "id")[0] for i in json.loads(tr[2])]
    print(f"{tr[1]} purchased following Book(s) on {tr[3]}")
    _print_books(books)
    total = sum([i[3] for i in books])
    print(f"\nTotal purchase of: ${total}")

book_management = [add_book, remove_book, search_book, show_books]
book_issues = [issue_book, return_book, show_issues, check_dues]
transactions = [new_transaction, transaction_history, show_transaction]

command = ""

while command!="exit":
    print("\nLibrary Management System")
    print("1) Books management \n2) Book Issues \n3) Transactions")

    command = input("> ")

    if command == "1":
        print("\nBooks Management")
        print("1) Add Book \n2) Remove Books \n3) Search \n4) Show All \n5) Back")

        command = input("> ")
        if command not in ["1", "2", "3", "4", "5"] or command == "5":
            print("Invalid Command" if command!="5" else "")
            continue

        book_management[int(command)-1]()

    elif command == "2":
        print("\nBook issues")
        print("1) Issue Book \n2) Book Return \n3) Show All \n4) Check Dues \n5) Back")

        command = input("> ")
        if command not in ["1", "2", "3", "4", "5"] or command == "5": 
            print("Invalid Command" if command!="5" else "")
            continue

        book_issues[int(command)-1]()

    elif command == "3":
        print("\nTransactions")
        print("1) New Transaction \n2) Transaction History \n3) Show Transaction \n4) Back")

        command = input("> ")
        if command not in ["1", "2", "3", "4"] or command == "4": 
            print("Invalid Command" if command!="4" else "")
            continue

        transactions[int(command)-1]()