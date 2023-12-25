import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="natya",
    password="hardpass",
    database="lms"
)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE books")
mycursor.execute("DROP TABLE issues")
mycursor.execute("DROP TABLE transactions")

mycursor.execute("""CREATE TABLE books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255), 
                        author VARCHAR(255), 
                        price INT
                )""")

mycursor.execute("""CREATE TABLE issues (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    student VARCHAR(255), 
                    book_id VARCHAR(255), 
                    issued_on DATE, 
                    return_in INT
                )""")

mycursor.execute("""CREATE TABLE transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    student VARCHAR(255), 
                    book_id VARCHAR(255), 
                    purchased_on DATE
                )""")