import sqlite3
import time
from enum import Enum

from program.aopadder import AOP
from program.model.parfum import *
from program.testableHtmlParser import scrape_page


@AOP.log_method_call  # Logging input and output
@AOP.log_execution_time  # Log execution time
def store_perfume_details(perfume_details: PerfumeDetails, enjoyment: Enjoyment):
    connection = sqlite3.connect(r'D:/sqlite_exp/frag/fragrance_432025115.db')
    cursor = connection.cursor()

    # Map enjoyment levels to score values
    enjoyment_score_map = {
        Enjoyment.LOVE: 3,
        Enjoyment.LIKE: 2,
        Enjoyment.OK: 1,
        Enjoyment.DISLIKE: -1,
        Enjoyment.HATE: -2
    }

    # Calculate the score based on enjoyment
    perfume_enjoyment_score = enjoyment_score_map.get(enjoyment, 0)

    # Insert or update perfume details with enjoyment score
    cursor.execute('''
        SELECT id FROM Perfumes WHERE perfume_name = ? AND url = ?
    ''', (perfume_details.perfume_name, perfume_details.url))
    perfume_id = cursor.fetchone()

    if perfume_id is None:
        # If the perfume doesn't exist, insert it
        cursor.execute('''
            INSERT INTO Perfumes (perfume_name, url, enjoyment_score) 
            VALUES (?, ?, ?)
        ''', (perfume_details.perfume_name, perfume_details.url, perfume_enjoyment_score))
        perfume_id = cursor.lastrowid
    else:
        perfume_id = perfume_id[0]
        # If the perfume exists, update the enjoyment score
        cursor.execute('''
            UPDATE Perfumes SET enjoyment_score = ? WHERE id = ?
        ''', (perfume_enjoyment_score, perfume_id))

    # Insert or update notes
    for note in perfume_details.notes:
        cursor.execute('''
            SELECT id FROM Notes WHERE name = ?
        ''', (note.name,))
        note_id = cursor.fetchone()

        if note_id is None:
            # If the note doesn't exist, insert it
            cursor.execute('''
                INSERT INTO Notes (name, category) 
                VALUES (?, ?)
            ''', (note.name, note.category.name))
            note_id = cursor.lastrowid
        else:
            note_id = note_id[0]

        # Check if the note is already associated with this perfume and update score
        cursor.execute('''
            SELECT score FROM PerfumeNotes WHERE perfume_id = ? AND note_id = ?
        ''', (perfume_id, note_id))
        existing_score = cursor.fetchone()

        if existing_score is None:
            # If no score exists, insert the score
            cursor.execute('''
                INSERT INTO PerfumeNotes (perfume_id, note_id, score) 
                VALUES (?, ?, ?)
            ''', (perfume_id, note_id, perfume_enjoyment_score))
        else:
            # If a score exists, update the score
            cursor.execute('''
                UPDATE PerfumeNotes SET score = ? WHERE perfume_id = ? AND note_id = ?
            ''', (perfume_enjoyment_score, perfume_id, note_id))

    # Insert or update accords
    for accord in perfume_details.accords:
        cursor.execute('''
            SELECT id FROM Accords WHERE name = ?
        ''', (accord.name,))
        accord_id = cursor.fetchone()

        if accord_id is None:
            # If the accord doesn't exist, insert it
            cursor.execute('''
                INSERT INTO Accords (name, background) 
                VALUES (?, ?)
            ''', (accord.name, accord.background))
            accord_id = cursor.lastrowid
        else:
            accord_id = accord_id[0]

        # Check if the accord is already associated with this perfume and update score
        cursor.execute('''
            SELECT score FROM PerfumeAccords WHERE perfume_id = ? AND accord_id = ?
        ''', (perfume_id, accord_id))
        existing_score = cursor.fetchone()

        if existing_score is None:
            # If no score exists, insert the score
            cursor.execute('''
                INSERT INTO PerfumeAccords (perfume_id, accord_id, score) 
                VALUES (?, ?, ?)
            ''', (perfume_id, accord_id, perfume_enjoyment_score))
        else:
            # If a score exists, update the score
            cursor.execute('''
                UPDATE PerfumeAccords SET score = ? WHERE perfume_id = ? AND accord_id = ?
            ''', (perfume_enjoyment_score, perfume_id, accord_id))

    connection.commit()
    connection.close()

def scrape_and_store_multiple(urls, enjoyment):
    """
    Scrapes perfume details from multiple URLs, stores them with enjoyment,
    and waits 10 seconds between each URL.
    """
    for url in urls:
        try:
            perfume_details = scrape_page(url)  # Assuming scrape_page is defined
            store_perfume_details(perfume_details, enjoyment) # Assuming store_perfume_details is defined
            print(f"Successfully processed {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
        time.sleep(2.3)
