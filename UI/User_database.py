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
    activity_level REAL,
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
        current_weight REAL,
        target_cal INTEGER DEFAULT 0,
        UNIQUE(username, date)
    )""")
conn.commit()
conn.close()

conn = sqlite3.connect("../db/users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS meal_log (
        meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        meal_name TEXT NOT NULL,
        log_time TEXT NOT NULL,
        calories REAL DEFAULT 0,
        protein REAL DEFAULT 0,
        fat REAL DEFAULT 0,
        carbs REAL DEFAULT 0,
        portion REAL DEFAULT 1,
        FOREIGN KEY (username) REFERENCES users (username)
    )
""")
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
        
def update_calories(username, calories_to_add):
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_hour = now.hour

    try:
        cursor.execute("SELECT breakfast_cal, lunch_cal, dinner_cal FROM daily_calories WHERE username = ? AND date = ?", (username, current_date))
        existing_data = cursor.fetchone()

        if existing_data:
            breakfast_cal, lunch_cal, dinner_cal = existing_data
        else:
            breakfast_cal, lunch_cal, dinner_cal = 0, 0, 0

        if 0 <= current_hour < 12:  
            breakfast_cal += calories_to_add
            print(f"Menambahkan {calories_to_add} kalori ke sarapan.")
        elif 12 <= current_hour < 18: 
            lunch_cal += calories_to_add
        else: 
            dinner_cal += calories_to_add
            
        total_cal = breakfast_cal + lunch_cal + dinner_cal

        cursor.execute("""
            INSERT OR REPLACE INTO daily_calories 
            (username, date, breakfast_cal, lunch_cal, dinner_cal, total_cal) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, current_date, breakfast_cal, lunch_cal, dinner_cal, total_cal))
        
        conn.commit()
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

def add_meal_log(username, meal_name, calories, protein, fat, carbs, portion):
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        cursor.execute("""
            INSERT INTO meal_log (username, meal_name, log_time, calories, protein, fat, carbs, portion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, meal_name, current_time, calories, protein, fat, carbs, portion))
        conn.commit()
        print(f"Meal log '{meal_name}' untuk '{username}' berhasil ditambahkan.")
        
        update_calories(username, calories)

        return True
    except sqlite3.Error as e:
        print(f"Gagal menambahkan meal log: {e}")
        return False
    finally:
        conn.close()

def get_meal_logs_by_date(username, date):
    conn = sqlite3.connect('../db/users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM meal_log WHERE username = ? AND date(log_time) = ?", (username, date))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Gagal mengambil meal logs: {e}")
        return []
    finally:
        conn.close()

def get_calorie_history(username):
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT total_cal FROM daily_calories WHERE username = ? ORDER BY date ASC", (username,))
        calories = [item[0] for item in cursor.fetchall()]
        return calories
    finally:
        conn.close()

def get_weight_history(username):
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT current_weight FROM daily_calories 
            WHERE username = ? AND current_weight IS NOT NULL 
            ORDER BY date ASC
        """, (username,))
        weights = [item[0] for item in cursor.fetchall()]
        return weights
    finally:
        conn.close()

# Add this new function to your user_database.py file

def get_latest_target_calories(username):
    conn = sqlite3.connect('../db/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT target_cal FROM daily_calories 
            WHERE username = ? 
            ORDER BY date DESC 
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            return result[0]
        else:
            return 2000
    finally:
        conn.close()