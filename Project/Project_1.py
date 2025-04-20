import mysql.connector
import random
import time

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "jonathan",  
    "database": "empdb"
}

def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        exit()

def generate_password():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols = "01234&56789#@$"
    return ''.join(random.choice(letters + symbols) for _ in range(6))

def addEmp():
    db = connect_db()
    cursor = db.cursor()

    while True:
        try:
            code = int(input("Enter 4-digit code: "))
            if not (1000 <= code <= 9999):
                print("Invalid code.")
                continue
            cursor.execute("SELECT code FROM employees WHERE code = %s", (code,))
            if cursor.fetchone():
                print("Code already exists.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")

    name = input("Enter Name: ")
    job = input("Enter Job: ")
    salary = float(input("Enter Salary: "))
    dept = input("Enter Department: ")
    password = generate_password()

    try:
        cursor.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s)", 
                       (code, name, job, salary, dept))
        cursor.execute("INSERT INTO private_info VALUES (%s, %s)", (code, password))
        db.commit()
        print(f"Employee added successfully! Password for {name}: {password}")
        print("Date & Time:", time.ctime())
    except Exception as e:
        db.rollback()
        print("Error while inserting:", e)

    cursor.close()
    db.close()

def dispEmp():
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM employees")
        records = cursor.fetchall()
        if not records:
            print("No employee records found.")
        else:
            print("1. Tabular Format\n2. Single Record Format")
            ch = int(input("Choice: "))
            for rec in records:
                if ch == 1:
                    print(f"Code: {rec[0]} \tName: {rec[1]} \tJob: {rec[2]} \tSalary: {rec[3]} \tDepartment: {rec[4]}")
                elif ch == 2:
                    print("-" * 30)
                    print(f"Code: {rec[0]}")
                    print(f"Name: {rec[1]}")
                    print(f"Job: {rec[2]}")
                    print(f"Salary: {rec[3]}")
                    print(f"Department: {rec[4]}")
                    print("-" * 30)
    except Exception as e:
        print("Error:", e)
    cursor.close()
    db.close()

def searchEmp():
    db = connect_db()
    cursor = db.cursor()
    print("1. Search by Name\n2. Search by Code")
    ch = int(input("Choice: "))
    if ch == 1:
        name = input("Enter name to search: ")
        cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))
    else:
        code = int(input("Enter code to search: "))
        cursor.execute("SELECT * FROM employees WHERE code = %s", (code,))
    
    record = cursor.fetchone()
    if record:
        print(f"Code: {record[0]} \tName: {record[1]} \tJob: {record[2]} \tSalary: {record[3]} \tDepartment: {record[4]}")
    else:
        print("Employee not found.")
    cursor.close()
    db.close()

def modEmp():
    db = connect_db()
    cursor = db.cursor()
    code = int(input("Enter employee code to modify: "))
    cursor.execute("SELECT * FROM employees WHERE code = %s", (code,))
    rec = cursor.fetchone()

    if not rec:
        print("Employee not found.")
        return

    print("1. Modify Name\n2. Modify Job\n3. Modify Salary\n4. Modify Code\n5. Modify Department")
    ch = int(input("Your choice: "))

    try:
        if ch == 1:
            new = input("New Name: ")
            cursor.execute("UPDATE employees SET name = %s WHERE code = %s", (new, code))
        elif ch == 2:
            new = input("New Job: ")
            cursor.execute("UPDATE employees SET job = %s WHERE code = %s", (new, code))
        elif ch == 3:
            new = float(input("New Salary: "))
            cursor.execute("UPDATE employees SET salary = %s WHERE code = %s", (new, code))
        elif ch == 4:
            new = int(input("New Code: "))
            cursor.execute("SELECT code FROM employees WHERE code = %s", (new,))
            if cursor.fetchone():
                print("New code already exists.")
                return
            cursor.execute("UPDATE employees SET code = %s WHERE code = %s", (new, code))
            cursor.execute("UPDATE private_info SET code = %s WHERE code = %s", (new, code))

        elif ch == 5:
            new = input("New Department: ")
            cursor.execute("UPDATE employees SET department = %s WHERE code = %s", (new, code))
        db.commit()
        print("Employee record updated.")
    except Exception as e:
        db.rollback()
        print("Error:", e)
    cursor.close()
    db.close()

def delEmp():
    db = connect_db()
    cursor = db.cursor()
    code = int(input("Enter code to delete: "))
    cursor.execute("SELECT * FROM employees WHERE code = %s", (code,))
    rec = cursor.fetchone()
    if not rec:
        print("No such employee.")
    else:
        confirm = input("Are you sure you want to delete (y/n)? ")
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM private_info WHERE code = %s", (code,))
            cursor.execute("DELETE FROM employees WHERE code = %s", (code,))
            db.commit()
            print("Employee deleted.")
    cursor.close()
    db.close()

def display_pass():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM private_info")
    passwords = cursor.fetchall()
    print("Passwords:")
    for pwd in passwords:
        print(f"Code: {pwd[0]} \tPassword: {pwd[1]}")
    cursor.close()
    db.close()

def finances():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*), SUM(salary) FROM employees")
    count, total_salary = cursor.fetchone()
    if not total_salary:
        total_salary = 0
    avg_salary = total_salary / count if count else 0

    while True:
        print("1. Total Salary\n2. Average Salary\n0. Exit")
        ch = int(input("Choice: "))
        if ch == 1:
            print(f"Total Salary: {total_salary}")
        elif ch == 2:
            print(f"Average Salary: {round(avg_salary, 2)}")
        elif ch == 0:
            break
        else:
            print("Invalid choice.")
    cursor.close()
    db.close()

def admin():
    password = input("Enter admin password: ")
    if password == "#A":
        print("Access granted.")
        print("1. Display All Employees\n2. Show Passwords")
        ch = int(input("Choice: "))
        if ch == 1:
            dispEmp()
        elif ch == 2:
            display_pass()
    else:
        print("Access denied.")

def employee_management():
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Search Employee")
        print("4. Modify Employee")
        print("5. Delete Employee")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            addEmp()
        elif choice == 2:
            dispEmp()
        elif choice == 3:
            searchEmp()
        elif choice == 4:
            modEmp()
        elif choice == 5:
            delEmp()
        elif choice == 0:
            break
        else:
            print("Invalid choice.")

def main_menu():
    while True:
        print("\nWelcome to Quantech Inc.")
        print("1. Employee Management")
        print("2. Company Analytics")
        print("3. Admin Access")
        print("0. Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            employee_management()
        elif ch == 2:
            finances()
        elif ch == 3:
            admin()
        elif ch == 0:
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
