import sqlite3
import os


def create_db():
    db_path = r'D:/sqlite_exp/frag/fragrance_432025115.db'

    # If the database already exists, delete it
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create a new database and tables
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Perfumes (
            id INTEGER PRIMARY KEY,
            perfume_name TEXT NOT NULL,
            url TEXT NOT NULL,
            enjoyment_score INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accords (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            background TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PerfumeNotes (
            perfume_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (perfume_id) REFERENCES Perfumes(id),
            FOREIGN KEY (note_id) REFERENCES Notes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PerfumeAccords (
            perfume_id INTEGER NOT NULL,
            accord_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (perfume_id) REFERENCES Perfumes(id),
            FOREIGN KEY (accord_id) REFERENCES Accords(id)
        )
    ''')

    connection.commit()
    connection.close()


create_db()
