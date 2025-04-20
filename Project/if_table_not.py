import mysql.connector

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

def setup_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            code INT PRIMARY KEY,
            name VARCHAR(50),
            job VARCHAR(30),
            salary FLOAT,
            department VARCHAR(30)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS private_info (
            code INT PRIMARY KEY,
            password VARCHAR(10),
            FOREIGN KEY (code) REFERENCES employees(code) ON DELETE CASCADE
        )
    """)
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    setup_db()

