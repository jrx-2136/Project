from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import random
import time

# MySQL configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "jonathan",
    "database": "empdb"
}

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_key'

# Database connection helper
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        raise

# Password generator
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbols = "01234&56789#@$"
def generate_password():
    return ''.join(random.choice(letters + symbols) for _ in range(6))

# Home page: display form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Form submission handler
@app.route('/add_employee', methods=['POST'])
def add_employee():
    code = int(request.form['code'])
    name = request.form['name']
    job = request.form['job']
    department = request.form['department']
    password = generate_password()

    db = connect_db()
    cursor = db.cursor()

    # Check for duplicate code
    cursor.execute("SELECT code FROM employees WHERE code = %s", (code,))
    if cursor.fetchone():
        flash(f"Employee code {code} already exists.", 'error')
        cursor.close()
        db.close()
        return redirect(url_for('index'))

    # Insert into employees and private_info
    try:
        cursor.execute(
            "INSERT INTO employees (code, name, job, salary, department) VALUES (%s, %s, %s, %s, %s)",
            (code, name, job, 0.0, department)
        )
        cursor.execute(
            "INSERT INTO private_info (code, password) VALUES (%s, %s)",
            (code, password)
        )
        db.commit()
        flash(f"Employee added successfully! Password for {name}: {password}", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error while inserting: {e}", 'error')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)