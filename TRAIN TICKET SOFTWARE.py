import mysql.connector
import random
import numpy as np
import matplotlib.pyplot as plt

# Connect to MySQL Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ticketdatabase"
)

# User Registration
def user_creation():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    ph_num = input("Enter your phone number: ")

    cursor = mydb.cursor()
    sql = "INSERT INTO customers (username, password, ph_num) VALUES (%s, %s, %s)"
    val = (username, password, ph_num)

    try:
        cursor.execute(sql, val)
        mydb.commit()
        print("User account created successfully!")
    except mysql.connector.Error as err:
        print("Error:", err)

# Admin Login
def admin_login():
    admin_user = "Manzu"
    admin_pass = "Manzu"

    username = input("Enter Admin username: ")
    password = input("Enter Admin password: ")

    if username == admin_user and password == admin_pass:
        print("Admin logged in successfully!")
        admin_panel()
    else:
        print("Incorrect Admin credentials.")

# Display All Bookings for Admin
def show_all_bookings():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Booking")
    bookings = cursor.fetchall()
    if bookings:
        print("All Bookings:")
        for booking in bookings:
            print(booking)
    else:
        print("No bookings found.")

#PNR Number
def pnr():
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "ticketdatabase"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Booking")
    myresult = mycursor.fetchall()
    pnr = input("Enter a pnr:")
    found = True
    for row in myresult:
        if str(row[0]) == pnr:
            print("Booking found:",row)
            found = False
            break

#Display Train Bookings for Admin Panel
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "ticketdatabase"
)

def show_train_bookings_counts():
    cursor = mydb.cursor()
    sql ="SELECT train_number,COUNT(*)FROM Booking GROUP BY train_number"
    cursor.execute(sql)
    train_counts = cursor.fetchall()

    if train_counts:
        print("\n--- Train Booking Statistics ---")
        for train_num,count in train_counts:
            print(f"Train Number:{train_num},Bookings:{count}")
    else:
        print("No train bookings found to display statistics.")

#Display destination records        
def show_destination_bookings_counts():
    cursor = mydb.cursor()
    sql = ("SELECT destination,COUNT(*)FROM Booking GROUP BY destination")
    cursor.execute(sql)
    destination_counts = cursor.fetchall()
    
    if destination_counts:
        print("\n--- Destination booking statistics ---")
        for destination,count in destination_counts:
            print(f"destination:{destination},bookings:{count}")
    else:
        print("No destination bookings found to display statistics")
        
# Generate unique PNR and Seat Number
def generate_unique_code(column, table, prefix):
    cursor = mydb.cursor()
    while True:
        code = prefix + str(random.randint(1000, 9999))
        cursor.execute(f"SELECT * FROM {table} WHERE {column} = %s", (code,))
        if not cursor.fetchone():
            return code
    
#train Ticket Booking
def book_ticket(username):
    print("\nTicket Booking - Max 5 tickets")
    n = int(input("Enter number of tickets to book: "))
    if n > 5:
        print("Cannot book more than 5 tickets.")
        return

    for i in range(n):
        name = input("Enter passenger name: ")
        age = input("Enter age: ")
        gender = input("Enter gender: ")
        phone = input("Enter phone number: ")
        from_city = input("From city: ")
        destination = input("To city: ")
        train_number = input("Train number: ")
        pnr = generate_unique_code("PNR","Booking","PNR")
        seat = generate_unique_code("Seat_num","Booking","S")
        train_no = []
        i = 0
        j = 0
        while i<n:
            mydb = mysql.connector.connect(host = "localhost",user = "root",password = "root",database = "ticketdatabase")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM train_data")
            myresult = mycursor.fetchall()
            train_no = myresult[j][0]
            if train_number == train_no:
                mycursor = mydb.cursor()
                sql = """INSERT INTO booking (PNR, name, age, gender, phone_num, from_city, destination, train_number, Seat_num) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (pnr, name, age, gender, phone, from_city, destination, train_number, seat)
                mycursor.execute(sql, val)
                mydb.commit()
                print(f"Ticket {i+1} booked successfully! PNR: {pnr}, Seat: {seat}")
                break
            j += 1
# User Login and Booking
def user_login():
    phone = input("Enter your registered phone number: ")
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM customers WHERE ph_num = %s", (phone,))
    user = cursor.fetchone()

    if user:
        print(f"Welcome {user[1]}! Proceed to book tickets.")
        book_ticket(user[1])
    else:
        print("User not found. Please register first.")
#Chart preparing
def chart():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM booking")
    myresult = mycursor.fetchall()
    a = []
    b = []
    i = 0
    j = 0
    n = int(input("Enter how many lines you want:"))
    while i<n:
        a.append(myresult[j][6])
        b.append(myresult[j][3])
        j+=1
        i+=1
        x = np.array(a)
        y = np.array(b)
        plt.bar(x,y)
        plt.show()

#Admin Panel
def admin_panel():
    while True:
        print("\n==== admin panel ====")
        print("1. View all the bookings")
        print("2. View bookings counts by train number")
        print("3. View bookings counts by destination")
        print("4. Back to main ")
        print("5.Chart")
        admin_choice = input("Choose admin option(1/2/3/4/5):")
        if admin_choice == "1":
            show_all_bookings()
        elif admin_choice == "2":
            show_train_bookings_counts()
        elif admin_choice == "3":
            show_destination_bookings_counts()
        elif admin_choice == "4":
            print("Exiting admin panel.")
        elif admin_choice == "5":
            chart()
            break
        else:
            print("Invalid admin option.Please try again. ")


# Main Menu
def main():
    print("\n~~~~~Train Ticket Booking System ~~~~~~~~")
    print("1. Create User Account")
    print("2. Admin Login")
    print("3. User Login and Book Tickets")
    print("4. PNR Number")
    choice = input("Choose an option (1/2/3/4):")

    if choice == "1":
        user_creation()
    elif choice == "2":
        admin_login()
    elif choice == "3":
        user_login()
    elif choice == "4":
        pnr()
    else:
        print("Invalid option.")

# Run Program
if __name__ == "__main__":
    main()
while True:
    main()
    again = input("Press Enter to Run again")          
    if again.lower():
        break
