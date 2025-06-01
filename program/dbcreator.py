import sqlite3
import os

def create_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database deleted.")

    # Ensure the folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

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
            name TEXT NOT NULL
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
            width REAL NOT NULL,
            FOREIGN KEY (perfume_id) REFERENCES Perfumes(id),
            FOREIGN KEY (note_id) REFERENCES Notes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PerfumeAccords (
            perfume_id INTEGER NOT NULL,
            accord_id INTEGER NOT NULL,
            width REAL NOT NULL,
            FOREIGN KEY (perfume_id) REFERENCES Perfumes(id),
            FOREIGN KEY (accord_id) REFERENCES Accords(id)
        )
    ''')

    connection.commit()
    connection.close()
    print(f"New database created successfully at: {db_path}")
