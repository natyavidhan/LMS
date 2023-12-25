import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="natya",
    password="hardpass",
    database="lms"
)

mycursor = mydb.cursor()