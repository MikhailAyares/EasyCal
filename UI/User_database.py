import sqlite3
import hashlib
from datetime import datetime

conn = sqlite3.connect("../db/users.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER,
    gender TEXT NOT NULL,
    start_weight REAL,
    current_weight REAL,
    goal_weight REAL,
    height REAL,
    activity_level INTEGER,
    weekly_goal REAL,
    last_updated TEXT NOT NULL 
)""")

conn.commit()
conn.close()

conn = sqlite3.connect("../db/users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_calories (
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        breakfast_cal INTEGER DEFAULT 0,
        lunch_cal INTEGER DEFAULT 0,
        dinner_cal INTEGER DEFAULT 0,
        total_cal INTEGER DEFAULT 0,
        UNIQUE(username, date)
    )""")
conn.commit()
conn.close()

def Register(username, password, age, gender, start_weight, goal_weight, activity_level, weekly_goal, height): #masukin data ke db
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute("""INSERT INTO users (username, password, age, gender, start_weight, 
                                              current_weight, goal_weight, activity_level, weekly_goal, 
                                              height, last_updated) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", 
                                             (username, password_hash, age, gender, start_weight, 
                                              start_weight, goal_weight, activity_level, weekly_goal, 
                                              height, current_time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("username already exists")
        return False
    finally:
        conn.close()
    
def login(username,password): #login, check data
        
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    
    try: 
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
        return cursor.fetchone() is not None
    
    finally:
        conn.close()
        
def get_data(username): 
    
    conn = sqlite3.connect('../db/users.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = cursor.fetchone()
        if data:
            return dict(data)
        else: 
            return None
    except sqlite3.Error as e:
        print(f"failed, {e}")
    finally:
        conn.close()

def update_data(username, password, current_weight, goal_weight, activity_level):
    
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        if password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("""
                UPDATE users 
                SET password = ?, current_weight = ?, goal_weight = ?, activity_level = ?, last_updated = ?
                WHERE username = ?
            """, (password_hash, current_weight, goal_weight, activity_level, current_time, username))
        else:
            
            cursor.execute("""
                UPDATE users 
                SET current_weight = ?, goal_weight = ?, activity_level = ?, last_updated = ?
                WHERE username = ?
            """, (current_weight, goal_weight, activity_level, current_time, username))

        if cursor.rowcount == 0:
            print(f"Username '{username}' not found. No data was updated.")
            return False
        else:
            conn.commit()
            print(f"Data for '{username}' has been successfully updated.")
            return True
            
    except sqlite3.Error as e:
        print(f"Failed, {e}")
        return False
        
    finally:
        conn.close()
        
def update_calories(username, date, breakfast_cal, lunch_cal, dinner_cal):
    
    total_cal = breakfast_cal + lunch_cal + dinner_cal
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO daily_calories 
            (username, date, breakfast_cal, lunch_cal, dinner_cal, total_cal) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, date, breakfast_cal, lunch_cal, dinner_cal, total_cal))
        conn.commit()
        print(f"Data kalori untuk {username} pada tanggal {date} berhasil disimpan.")
        return True
    except sqlite3.Error as e:
        print(f"Gagal menyimpan data kalori: {e}")
        return False
    finally:
        conn.close()

def get_calories(username, date):
    conn = sqlite3.connect('../db/users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM daily_calories WHERE username = ? AND date = ?", (username, date))
        data = cursor.fetchone()
        return dict(data) if data else None
    except sqlite3.Error as e:
        print(f"Gagal mengambil data kalori: {e}")
        return None
    finally:
        conn.close()


