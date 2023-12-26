import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="natya",
    password="hardpass",
    database="lms"
)

cursor = mydb.cursor()

def _print_books(books):
    print("")
    for i in books:
        print(f"({i[0]}) {i[1]}, By {i[2]} ${i[3]}")
    print("")

def _search_book(val, classifier):
    sql = f"SELECT * from books WHERE {classifier}=%s"
    cursor.execute(sql, (val, ))
    return [i for i in cursor]

def _get_issues():
    sql = "SELECT * from issues"
    cursor.execute(sql)
    return [i for i in cursor]

def add_book():
    name = input("Book name: ")
    author = input("Author name: ")
    price = input("Price: ")
    sql = "INSERT INTO books (name, author, price) VALUE (%s, %s, %s)"
    values = (name, author, price)
    cursor.execute(sql, values)
    mydb.commit()

def remove_book():
    command = input("Enter Book ID > ")
    sql = "DELETE from books WHERE id=%s"
    cursor.execute(sql, (command, ))
    mydb.commit()

def search_book():
    print("\nSearch with \n1) ID \n2) Name \n3) Author")
    command = input("> ")
    if command not in ["1", "2", "3"]:
        print("Invalid Input")
        search_book()
    classifier = ["id", "name", "author"][int(command)-1]
    val = input("Enter query > ")
    books = _search_book(val, classifier)
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
    if command == "n":
        issue_book()
        return
    name = input("Student Name > ")
    ret = input("Return in (days) > ")
    sql = "INSERT INTO issues (student, book_id, issued_on, return_in) VALUES (%s, %s, CURDATE(), %s)"
    cursor.execute(sql, (name, book[0], ret))
    mydb.commit()

def return_book():
    issue_id = input("Issue ID > ")
    cursor.execute("SELECT * from issues WHERE id=%s", (issue_id, ))
    issues = [i for i in cursor]
    if len(issues) == 0:
        print("Invalid ID")
        return_book()
        return
    issue = issues[0]
    if issue[5]:
        print("Book already Returned")
        return
    sql = "UPDATE issues SET returned=True WHERE id=%s"
    cursor.execute(sql, (issue_id, ))
    mydb.commit()

def show_issues():
    issues = _get_issues()
    print("")
    for i in issues:
        book = _search_book(i[2], "id")[0]
        print(f"({i[0]}) {book[1]}, Issued By {i[1]} on {i[3]} for {i[4]} days ({'Returned' if i[5] else 'Not Returned'})")
    print("")

def check_dues():
    issues = _get_issues()
    print("")
    for i in issues:
        date = i[3]+datetime.timedelta(days=int(i[4]))
        if not i[5]:
            if datetime.date.today() > date:
                book = _search_book(i[2], "id")[0]
                print(f"({i[0]}) {book[1]}, Issued By {i[1]} on {i[3]} for {i[4]} days ({'Returned' if i[5] else 'Not Returned'})")
    print("")

book_management = [add_book, remove_book, search_book, show_books]
book_issues = [issue_book, return_book, show_issues, check_dues]

command = ""

while command!="exit":

    print("\nLibrary Management System")
    print("1) Books management \n2) Book Issues \n3) Transactions")

    command = input("> ")

    if command == "1":
        print("\nBooks Management")
        print("1) Add Book \n2) Remove Books \n3) Search \n4) Show All \n5) Back")

        command = input("> ")
        if command not in ["1", "2", "3", "4", "5"]:
            print("Invalid Command")
            continue
        if command == "5":
            continue

        command = int(command)-1
        book_management[command]()

    if command == "2":
        print("\nBook issues")
        print("1) Issue Book \n2) Book Return \n3) Show All \n4) Check Dues \n5) Back")

        command = input("> ")
        if command not in ["1", "2", "3", "4", "5"]:
            print("Invalid Command")
            continue
        if command == "5":
            continue

        command = int(command)-1
        book_issues[command]()