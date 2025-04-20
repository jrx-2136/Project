import pickle
import os
import random
import time


EMP_FILE = 'employ.dat'
PRI_FILE = 'private.dat'
TEMP_FILE= 'C:/Users/User/OneDrive/Documents/Desktop/Python/WPP/Project/temporary.dat'


def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&@#$"
    return ''.join(random.choice(chars) for _ in range(6))

def ensure_files():
    """Create the employee and password files if they do not exist."""
    for filename in (EMP_FILE, PRI_FILE):
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                pass  # just create an empty file

def addEmp():
    # Ensure files exist first.
    ensure_files()

    valid_cod = []

    # Read existing employee codes.
    try:
        with open(EMP_FILE, 'rb') as f:
            while True:
                try:
                    rec = pickle.load(f)
                    valid_cod.append(rec[0])
                except EOFError:
                    break
                except Exception as e:
                    print("Error while reading record:", e)
                    break
    except Exception as e:
        print("Error opening EMP_FILE for reading:", e)

    # Input employee details.
    while True:
        try:
            cod = int(input('Enter 4-digit code: '))
            if 1000 <= cod <= 9999:
                if cod in valid_cod:
                    print("Code already exists. Please enter a unique code.")
                else:
                    break
            else:
                print("Code must be a 4-digit number between 1000 and 9999.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        nam = input('Enter name: ')
        if nam.isalpha():
            break
        print("Invalid name. Please use letters only.")

    while True:
        job = input('Enter job: ')
        if job.isalpha():
            break
        print("Invalid job. Please use letters only.")

    while True:
        try:
            sal = int(input('Enter salary: '))
            break
        except ValueError:
            print("Invalid salary. Please enter a number.")

    while True:
        dept = input('Enter department: ')
        if dept.isalpha():
            break
        print("Invalid department. Please use letters only.")

    rec = [cod, nam, job, sal, dept]
    password = generate_password()
    # storing the password in a list (could also use a dict keyed by employee code)
    pri = [password]

    print("\nEmployee record to be added:", rec)
    print(f"{nam}'s password is: {password}")

    # Write new records to the files.
    try:
        with open(EMP_FILE, 'ab') as f_emp:
            pickle.dump(rec, f_emp)

        with open(PRI_FILE, 'ab') as f_pri:
            pickle.dump(pri, f_pri)

        print("Employee details added successfully!")
        print("Timestamp:", time.ctime())

    except Exception as e:
        print("Error while writing to file:", e)



def dispEmp():
    if not os.path.exists(EMP_FILE):
        print("No employee records found.")
        return

    try:
        with open(EMP_FILE, 'rb') as fob:
            print('1. Display in Tabular format \n2. Display in Single record format ')
            ch = int(input('Enter Choice:\t'))
            while True:
                rec = pickle.load(fob)
                if ch == 1:
                    print('Code:', rec[0], '\t Name:', rec[1], '\t Job:', rec[2], '\t Salary:', rec[3], '\t Department:', rec[4])
                elif ch == 2:
                    print("Code:", rec[0])
                    print("Name:", rec[1])
                    print("Job:", rec[2])
                    print("Salary:", rec[3])
                    print("Department:", rec[4])
                    print('-' * 35)
    except EOFError:
        pass
    except Exception as e:
        print("Error reading file:", e)


def searchEmp():
    if not os.path.exists(EMP_FILE):
        print("No employee records found.")
        return

    try:
        with open(EMP_FILE, 'rb') as fob:
            ch = int(input('1. Search Name \n2. Search Code\nChoice: '))
            if ch == 1:
                nm = input('Enter the name to search:\t')
            while True:
                rec = pickle.load(fob)
                if ch == 1 and rec[1] == nm:
                    print('Code:', rec[0], '\tName:', rec[1], '\tJob:', rec[2], '\t Salary', rec[3])
                    return
                elif ch == 2:
                    cod = int(input('Enter code to search:\t'))
                    if rec[0] == cod:
                        print('Code:', rec[0], '\tName:', rec[1], '\tJob:', rec[2], '\t Salary', rec[3])
                        return
    except EOFError:
        print('No such Employee found!!')
    except Exception as e:
        print("Error occurred:", e)


def modEmp():
    if not os.path.exists(EMP_FILE):
        print("No employee records found.")
        return

    f = 0
    try:
        with open(EMP_FILE, 'rb') as fob1, open(TEMP_FILE, 'wb') as fob2:
            nm = input('Enter the name to Modify: ')
            while True:
                rec = pickle.load(fob1)
                if rec[1] == nm:
                    print('Code:', rec[0], '\tName:', rec[1], '\tJob:', rec[2], '\t Salary', rec[3], '\tDepartment', rec[4])
                    ch1 = input('Want to modify? (y/n): ')
                    if ch1.lower() == 'y':
                        print('1. Modify Name')
                        print('2. Modify Job')
                        print('3. Modify Salary')
                        print('4. Modify Code')
                        print('5. Modify Department')
                        try:
                            ch2 = int(input('Choice: '))
                            if ch2 == 1:
                                rec[1] = input('Enter new name: ')
                            elif ch2 == 2:
                                rec[2] = input('Enter new job: ')
                            elif ch2 == 3:
                                rec[3] = int(input('Enter new salary: '))
                            elif ch2 == 4:
                                rec[0] = int(input('Enter new code: '))
                            elif ch2 == 5:
                                rec[4] = input('Enter new department: ')
                            else:
                                print("Invalid choice. No changes made.")
                        except ValueError:
                            print("Invalid input. No changes made.")
                    f = 1
                pickle.dump(rec, fob2)
    except EOFError:
        pass
    except Exception as e:
        print("Error during modification:", e)

    if f:
        os.remove(EMP_FILE)
        os.rename(TEMP_FILE, EMP_FILE)
        print('Record Modified!')
    else:
        print('No such Employee found')


def delEmp():
    if not os.path.exists(EMP_FILE):
        print("No employee records found.")
        return

    f = 0
    try:
        with open(EMP_FILE, 'rb') as fob1, open(TEMP_FILE, 'wb') as fob2:
            nm = input('Enter the name to delete:\t')
            while True:
                rec = pickle.load(fob1)
                if rec[1] == nm:
                    print('Code:', rec[0], '\tName:', rec[1], '\tJob:', rec[2], '\t Salary', rec[3], 'Department', rec[4])
                    f = 1
                    continue  # Skip dumping to effectively delete
                pickle.dump(rec, fob2)
    except EOFError:
        pass
    except Exception as e:
        print("Error during deletion:", e)

    if f:
        ch1 = input('Want to Delete? (y/n): ')
        if ch1.lower() == 'y':
            os.remove(EMP_FILE)
            os.rename(TEMP_FILE, EMP_FILE)
            print('Record Deleted!')
        else:
            print('RECORD NOT DELETED')
    else:
        print('No such Employee found')


def display_pass():
    if not os.path.exists(PRI_FILE):
        print("No password file found.")
        return

    try:
        with open(PRI_FILE, 'rb') as fob1:
            print("All Passwords:")
            while True:
                rec = pickle.load(fob1)
                for code, pwd in rec.items():
                    print(f"Code {code}: {pwd}")
    except EOFError:
        pass
    except Exception as e:
        print("Error reading password file:", e)


def admin():
    password = input('Enter Password: ')
    if password == '#A':
        print('Access granted')
        try:
            with open(EMP_FILE, 'rb') as fob:
                print('1. Display in Tabular format')
                print('2. Display in Single record format ')
                print('3. Display all employee passwords')
                ch = int(input('Enter Choice:\t'))
                if ch == 3:
                    display_pass()
                    return
                while True:
                    rec = pickle.load(fob)
                    if ch == 1:
                        print('Code:', rec[0], '\t Name:', rec[1], '\t Job:', rec[2], '\t Salary:', rec[3], '\tDepartment', rec[4])
                    elif ch == 2:
                        print('-' * 25)
                        print("Code:", rec[0])
                        print("Name:", rec[1])
                        print("Job:", rec[2])
                        print("Salary:", rec[3])
                        print("Department", rec[4])
                        print('-' * 35)
        except EOFError:
            pass
        except Exception as e:
            print("Error:", e)
    else:
        print('Access denied')


def finances():
    total_salary = 0
    num_employees = 0
    try:
        with open(EMP_FILE, 'rb') as fob:
            while True:
                employee = pickle.load(fob)
                total_salary += employee[3]
                num_employees += 1
    except EOFError:
        pass

    while True:
        print('1. Total Salary\n2. Average Salary\n0.Exit')
        try:
            ch = int(input('Enter choice: '))
        except ValueError:
            print("Invalid input.")
            continue

        if ch == 1:
            print('Total Salary of Employees:', total_salary)
            print('-' * 30)
        elif ch == 2:
            if num_employees > 0:
                avg = round(total_salary / num_employees, 3)
                print("Average Salary of Employees:", avg)
                print('-' * 30)
            else:
                print("No employees found.")
        elif ch == 0:
            break
        else:
            print('Invalid choice')


def employee_management():
    while True:
        print("Employee Management System")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Search Employee")
        print("4. Modify Employee")
        print("5. Delete Employee")
        print("0. Exit")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input.")
            continue

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
            print("Invalid choice. Please choose again.")
        print('-' * 30)


def main_menu():
    while True:
        print('Welcome to Quantech Inc.')
        print('Employee Management System')
        print('1. Employee Management')
        print('2. Company Analytics')
        print('3. Admin')
        print('0. Exit')
        try:
            ch = int(input('Enter your choice: '))
        except ValueError:
            print("Invalid input.")
            continue

        if ch == 1:
            print('-' * 35)
            employee_management()
        elif ch == 2:
            print('-' * 35)
            finances()
        elif ch == 3:
            admin()
        elif ch == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
        print('-' * 35)


main_menu()
