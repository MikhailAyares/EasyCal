import sqlite3
from datetime import date

DB_FILE = "food.db"

class NutritionDB:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrisi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                calories REAL,
                protein REAL,
                fat REAL,
                carbohydrate REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_id INTEGER,
                grams REAL,
                date TEXT,
                FOREIGN KEY(food_id) REFERENCES nutrition(id)
            )
        """)
        self.conn.commit()

    # --------- DATA NUTRITION ----------
    def add_food(self, name, calories, protein, fat, carbs):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO nutrition (name, calories, protein, fat, carbs)
            VALUES (?, ?, ?, ?, ?)
        """, (name, calories, protein, fat, carbs))
        self.conn.commit()

    def list_foods(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT * FROM nutrition").fetchall()

    # --------- LOG MAKANAN ----------
    def add_meal_log(self, food_id, grams, log_date=None):
        if log_date is None:
            log_date = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO meal_log (food_id, grams, date)
            VALUES (?, ?, ?)
        """, (food_id, grams, log_date))
        self.conn.commit()

    def get_daily_logs(self, log_date=None):
        if log_date is None:
            log_date = date.today().isoformat()
        cursor = self.conn.cursor()
        return cursor.execute("""
            SELECT n.name, m.grams,
                   (n.calories * m.grams / 100.0) as calories,
                   (n.proteins * m.grams / 100.0) as protein,
                   (n.fat * m.grams / 100.0) as fat,
                   (n.carbohydrate * m.grams / 100.0) as carbohydrate
            FROM meal_log m
            JOIN nutrisi n ON m.food_id = n.id
            WHERE m.date = ?
        """, (log_date,)).fetchall()

    def get_daily_summary(self, log_date=None):
        if log_date is None:
            log_date = date.today().isoformat()
        cursor = self.conn.cursor()
        return cursor.execute("""
            SELECT 
                SUM(n.calories * m.grams / 100.0) as total_calories,
                SUM(n.proteins * m.grams / 100.0) as total_protein,
                SUM(n.fat * m.grams / 100.0) as total_fat,
                SUM(n.carbohydrate * m.grams / 100.0) as total_carbs
            FROM meal_log m
            JOIN nutrisi n ON m.food_id = n.id
            WHERE m.date = ?
        """, (log_date,)).fetchone()

    def close(self):
        self.conn.close()


# ---------------- DEMO ----------------
if __name__ == "__main__":
    db = NutritionDB()
    db.create_tables()
    # Tambahkan log makanan

    print("Log Harian:")
    for log in db.get_daily_logs():
        print(log)

    print("\nRingkasan:")
    print(db.get_daily_summary())

    db.close()
