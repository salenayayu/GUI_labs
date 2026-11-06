"""учебная базу"""
import sqlite3
from pathlib import Path


def create_database():
    path = Path(__file__).with_name("students.db")
    if path.exists():
        print("База уже существует:", path)
        return
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                grade INTEGER NOT NULL CHECK (grade BETWEEN 2 AND 5)
            )
        """)
        connection.executemany(
            "INSERT INTO students (name, group_name, grade) VALUES (?, ?, ?)",
            [("Анна", "ИС-21", 5), ("Иван", "ИС-21", 3),
             ("Мария", "ИС-22", 4), ("Павел", "ИС-22", 2),
             ("Ольга", "ИС-21", 5)])
    print("База создана:", path)


if __name__ == "__main__":
    create_database()