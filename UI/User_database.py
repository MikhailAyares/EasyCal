import sqlite3
import hashlib

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER,
    gender TEXT NOT NULL,
    weight REAL,
    height REAL,
    target_weight REAL
    )""")

conn.commit()
conn.close()

def Register(username, password, age, gender, weight, height, target_weight): #masukin data ke db
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, age, gender, weight, height, target_weight) VALUES(?,?,?,?,?,?,?)", (username,password_hash,age,gender,weight,height,target_weight))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("username already exists")
        return False
    finally:
        conn.close()
    
def login(username,password): #login, check data
        
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try: 
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
        return cursor.fetchone() is not None
    
    finally:
        conn.close()
        
def get_data(username):
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username))
        data = cursor.fetchone()
        return data
    except sqlite3.Error as e:
        print(f"failed, {e}")
    finally:
        conn.close()

def update_data(username, password, age, weight, height, target_weight):
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET password = ?, age = ?, weight = ?, height = ?, target_weight = ?
            WHERE username = ?
        """, (password_hash, age, weight, height, target_weight, username))
        
        if cursor.rowcount == 0:
            print(f"Username '{username}' not found. No data was updated.")
        else:
            conn.commit()
            print(f"Data for '{username}' has been successfully updated.")
            
    except sqlite3.Error as e:
        print(f"Failed, {e}")
        
    finally:
        conn.close()