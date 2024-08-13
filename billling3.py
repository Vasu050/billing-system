import mysql.connector
import datetime

try:
    con = mysql.connector.connect(host="localhost", database="billing", user="root", password="vasu2005")
    cursor = con.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")

def clear():
    for _ in range(1):
        print()

def table():
    while True:
        clear()
        print(' M A I N M E N U')
        print('-'*80)
        print('1. Add New Object')
        print('2. Modify Existing Object')
        print('3. Delete Existing Object')
        print('4. Display All Objects')
        print('5. Billing')
        print('6. Search List')
        print('7. Exit')
        choice = int(input('\n\nEnter your choice (1..7): '))
        if choice == 1:
            add_object()
        elif choice == 2:
            modify_object()
        elif choice == 3:
            delete_object()
        elif choice == 4:
            object_list()
        elif choice == 5:
            billing()
        elif choice == 6:
            search_list()
        elif choice == 7:
            break

def search_list():
    while True:
        clear()
        print(' S E A R C H M E N U ')
        print('-'*100)
        print('1. Bill information')
        print('2. Customer information')
        print('3. Display All Bills DB')
        print('4. Back to Main Menu')
        choice = int(input('\n\nEnter your choice (1..4): '))
        if choice == 1:
            search_bill()
        elif choice == 2:
            search_customer()
        elif choice == 3:
            bill_list()
        elif choice == 4:
            break

def add_object():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id VARCHAR(10) PRIMARY KEY,
                item_name VARCHAR(40),
                price INT(10)
            )
        """)
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        con.rollback()
    
    clear()
    print('Add New Item - ')
    print('-'*50)
    item_id = input('Enter Item ID: ')
    item_name = input('Enter Item Name: ')
    price = input('Enter Item Price: ')
    sql = 'SELECT * FROM items WHERE item_id = %s'
    cursor.execute(sql, (item_id,))
    record = cursor.fetchone()
    if record is None:
        sql = 'INSERT INTO items (item_id, item_name, price) VALUES (%s, %s, %s)'
        cursor.execute(sql, (item_id, item_name, price))
        con.commit()
        print('\n\nNew Item added successfully')
    else:
        print('\n\nItem with this ID already exists')

def modify_object():
    clear()
    print('Modify Item Details - Screen')
    print('-'*80)
    item_id = input('Enter Item ID: ')
    item_name = input('Enter New Item Name: ')
    item_price = input('Enter Item Price: ')
    sql = 'UPDATE items SET item_name = %s, price = %s WHERE item_id = %s'
    cursor.execute(sql, (item_name, item_price, item_id))
    con.commit()
    print('\n\nRecord Updated Successfully.....')

def delete_object():
    item_id = input('Enter Item ID: ')
    sql = 'DELETE FROM items WHERE item_id = %s'
    cursor.execute(sql, (item_id,))
    con.commit()
    print('\n\nRecord Deleted Successfully.....')

def object_list():
    clear()
    print("Item ID Item Name Price")
    try:
        cursor.execute("SELECT * FROM items")
        records = cursor.fetchall()
        for row in records:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        con.rollback()

def find_object(no):
    sql = 'SELECT * FROM items WHERE item_id = %s'
    cursor.execute(sql, (no,))
    record = cursor.fetchone()
    print(record)
    return record

def billing():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                bill_no VARCHAR(10) NOT NULL,
                bill_date DATE,
                name VARCHAR(30),
                phone VARCHAR(15),
                amount INT(30),
                PRIMARY KEY (bill_no)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                bill_no VARCHAR(10) NOT NULL,
                item_id VARCHAR(10),
                item_name VARCHAR(30),
                price INT(10),
                qty INT(10),
                PRIMARY KEY (bill_no, item_id),
                FOREIGN KEY (bill_no) REFERENCES bills(bill_no)
            )
        """)
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        con.rollback()
    
    clear()
    items = []
    bill_no = input("Enter Bill ID: ")
    name = input('Enter Customer Name: ')
    phone = input('Enter Phone No: ')
    today = datetime.date.today()
    while True:
        no = int(input('Enter Item No (0 to stop): '))
        if no <= 0:
            break
        else:
            item = find_object(no)
            if item is None:
                print('Item Not Found')
            else:
                qty = int(input('Enter Item Qty: '))
                item = list(item)
                item.append(qty)
                items.append(item)
    
    clear()
    print()
    print(' CHOTU GENERAL STORE ')
    print(' Rajendra Nagar, GZB ')
    print(' Phone: 6392975684 , Email: Chintu6969@gmail.com ')
    print()
    print('Bill No: {} Date: {}'.format(bill_no, today))
    print('-'*100)
    print('Customer Name: {} Phone No: {}'.format(name, phone))
    print('-'*100)
    print('Item ID Item Name Price Qty Amount')
    print('-'*100)
    total = 0
    for item in items:
        print(item[0], item[1], item[2], item[3], item[2]*item[3])
        total += item[2] * item[3]
    print('-'*100)
    print('Total Payable Amount: {}'.format(total))
    print()
    sql = 'INSERT INTO bills (bill_no, bill_date, name, phone, amount) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(sql, (bill_no, today, name, phone, total))
    con.commit()
    for item in items:
        sql = 'INSERT INTO transactions (bill_no, item_id, item_name, price, qty) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (bill_no, item[0], item[1], item[2], item[3]))
        con.commit()

def search_bill():
    clear()
    bill_no = input('Enter Bill Number: ')
    sql = 'SELECT * FROM bills WHERE bill_no = %s'
    cursor.execute(sql, (bill_no,))
    records1 = cursor.fetchall()
    if records1:
        print()
        print(' CHOTU GENERAL STORE ')
        print(' Rajendra Nagar, GZB ')
        print(' Phone: 6392975684 , Email: Chintu6969@gmail.com ')
        print()
        print('Bill No: {} Date: {}'.format(bill_no, records1[0][1]))
        print('-'*100)
        print('Customer Name: {} Phone No: {}'.format(records1[0][2], records1[0][3]))
        print('-'*100)
        print('Item ID Item Name Price Qty Amount')
        print('-'*100)
        sql = 'SELECT * FROM transactions WHERE bill_no = %s'
        cursor.execute(sql, (bill_no,))
        records2 = cursor.fetchall()
        for item in records2:
            print(item[1], item[2], item[3], item[4], int(item[3])*int(item[4]))
        print('-'*100)
        print('Total Payable Amount: {}'.format(records1[0][4]))
        print()
    else:
        print('Bill Not Found')

def search_customer():
    clear()
    name = input("Enter Customer Name: ")
    print("Customer Info:")
    print("Bill No. Date Customer Name Phone Amount Purchased")
    sql = 'SELECT * FROM bills WHERE name LIKE %s'
    cursor.execute(sql, ('%' + name + '%',))
    records = cursor.fetchall()
    for row in records:
        print(row)

def bill_list():
    clear()
    print("All Bills:")
    print("Bill No. Date Customer Name Phone Amount Purchased")
    print()
    try:
        cursor.execute("SELECT * FROM bills")
        records = cursor.fetchall()
        for row in records:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        con.rollback()

# Establishing connection and setting up cursor


table()
