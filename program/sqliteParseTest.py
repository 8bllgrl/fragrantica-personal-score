import sqlite3
import time

from program.aopadder import AOP
from program.model.parfum import *
from program.testableHtmlParser import scrape_page


@AOP.log_method_call
@AOP.log_execution_time
def get_adjusted_notes(perfume_id, enjoyment, cursor):
    cursor.execute('''
        SELECT Notes.name, PerfumeNotes.width
        FROM PerfumeNotes
        JOIN Notes ON Notes.id = PerfumeNotes.note_id
        WHERE perfume_id = ?
    ''', (perfume_id,))

    return [
        (name, round(width * enjoyment.value, 3))
        for name, width in cursor.fetchall()
    ]


# Adjust note widths by enjoyment for all perfumes, aggregated by note name
@AOP.log_method_call
@AOP.log_execution_time
def get_adjusted_note_scores(cursor, enjoyment=1.0):
    cursor.execute("""
        SELECT n.name, pn.width
        FROM PerfumeNotes pn
        JOIN Notes n ON pn.note_id = n.id
    """)

    adjusted_scores = {}
    for name, width in cursor.fetchall():
        score = width * enjoyment
        adjusted_scores[name] = adjusted_scores.get(name, 0) + score

    # Convert to sorted list of tuples
    return sorted(
        [(name, round(score, 2)) for name, score in adjusted_scores.items()],
        key=lambda x: x[1],
        reverse=True
    )


@AOP.log_method_call
@AOP.log_execution_time
def store_perfume_details(perfume_details: PerfumeDetails, enjoyment: Enjoyment, database_path: str):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    perfume_enjoyment_score = enjoyment.value  # Directly use the value of the Enjoyment enum

    perfume_id = get_perfume_id(cursor, perfume_details.perfume_name, perfume_details.url)
    if perfume_id is None:
        perfume_id = insert_perfume(cursor, perfume_details.perfume_name, perfume_details.url, perfume_enjoyment_score)
    else:
        update_perfume_enjoyment(cursor, perfume_enjoyment_score, perfume_id)

    # Update the width of each note based on enjoyment value
    for note in perfume_details.notes:
        # modified_enjoyment = round(float(note.width) * enjoyment.value, 3)  # Round to 3 decimal places
        note_id = get_or_insert_note(cursor, note)
        # update_perfume_note_score(cursor, perfume_id, note_id, modified_enjoyment)
        update_perfume_note_score(cursor, perfume_id, note_id, note.width)

    # Update the width of each accord based on enjoyment value
    for accord in perfume_details.accords:
        modified_enjoyment = round(float(accord.width) * enjoyment.value, 3)  # Round to 3 decimal places
        accord_id = get_or_insert_accord(cursor, accord)
        update_perfume_accord_score(cursor, perfume_id, accord_id, modified_enjoyment)

    connection.commit()
    connection.close()

@AOP.log_method_call
@AOP.log_execution_time
def get_perfume_id(cursor, perfume_name, url):
    cursor.execute(''' 
        SELECT id FROM Perfumes WHERE perfume_name = ? AND url = ? 
    ''', (perfume_name, url))
    result = cursor.fetchone()  # Fetch the result as a tuple
    if result is not None:
        return result[0]  # Return the first item of the tuple, which is the ID
    return None


@AOP.log_method_call
@AOP.log_execution_time
def insert_perfume(cursor, perfume_name, url, enjoyment_score):
    cursor.execute('''
        INSERT INTO Perfumes (perfume_name, url, enjoyment_score) 
        VALUES (?, ?, ?)
    ''', (perfume_name, url, enjoyment_score))
    return cursor.lastrowid


@AOP.log_method_call
@AOP.log_execution_time
def update_perfume_enjoyment(cursor, enjoyment_score, perfume_id):
    cursor.execute('''
        UPDATE Perfumes SET enjoyment_score = ? WHERE id = ?
    ''', (enjoyment_score, perfume_id))


@AOP.log_method_call
@AOP.log_execution_time
def get_or_insert_note(cursor, note):
    cursor.execute('''
        SELECT id FROM Notes WHERE name = ?
    ''', (note.name,))
    note_id = cursor.fetchone()
    if note_id is None:
        note_id = insert_note(cursor, note)
    else:
        note_id = note_id[0]
    return note_id


@AOP.log_method_call
@AOP.log_execution_time
def insert_note(cursor, note):
    cursor.execute('''
        INSERT INTO Notes (name) 
        VALUES (?)
    ''', (note.name,))
    return cursor.lastrowid



@AOP.log_method_call
@AOP.log_execution_time
def update_perfume_note_score(cursor, perfume_id, note_id, width):
    cursor.execute(''' 
        SELECT width FROM PerfumeNotes WHERE perfume_id = ? AND note_id = ? 
    ''', (perfume_id, note_id))
    existing = cursor.fetchone()
    if existing is None:
        cursor.execute(''' 
            INSERT INTO PerfumeNotes (perfume_id, note_id, width) 
            VALUES (?, ?, ?) 
        ''', (perfume_id, note_id, width))
    else:
        cursor.execute(''' 
            UPDATE PerfumeNotes SET width = ? WHERE perfume_id = ? AND note_id = ? 
        ''', (width, perfume_id, note_id))



@AOP.log_method_call
@AOP.log_execution_time
def get_or_insert_accord(cursor, accord):
    cursor.execute('''
        SELECT id FROM Accords WHERE name = ?
    ''', (accord.name,))
    accord_id = cursor.fetchone()
    if accord_id is None:
        accord_id = insert_accord(cursor, accord)
    else:
        accord_id = accord_id[0]
    return accord_id


@AOP.log_method_call
@AOP.log_execution_time
def insert_accord(cursor, accord):
    cursor.execute('''
        INSERT INTO Accords (name, background) 
        VALUES (?, ?)
    ''', (accord.name, accord.background))
    return cursor.lastrowid



@AOP.log_method_call
@AOP.log_execution_time
def update_perfume_accord_score(cursor, perfume_id, accord_id, width):
    cursor.execute(''' 
        SELECT width FROM PerfumeAccords WHERE perfume_id = ? AND accord_id = ? 
    ''', (perfume_id, accord_id))
    existing = cursor.fetchone()
    if existing is None:
        cursor.execute(''' 
            INSERT INTO PerfumeAccords (perfume_id, accord_id, width) 
            VALUES (?, ?, ?) 
        ''', (perfume_id, accord_id, width))
    else:
        cursor.execute(''' 
            UPDATE PerfumeAccords SET width = ? WHERE perfume_id = ? AND accord_id = ? 
        ''', (width, perfume_id, accord_id))



@AOP.log_method_call
@AOP.log_execution_time
def scrape_and_store_multiple(urls, enjoyment, database_path):
    """
    Scrapes perfume details from multiple URLs, stores them with enjoyment,
    and waits 10 seconds between each URL.
    """
    for url in urls:
        try:
            perfume_details = scrape_page(url)
            # perfume_details = debug_perfume_details()  # make so debug mode enabled true makes this turn on instead of comment in or out.
            store_perfume_details(perfume_details, enjoyment, database_path)
            print(f"Successfully processed {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
        time.sleep(5.3)


def debug_perfume_details():
    debug_perfume = PerfumeDetails(perfume_name='TESTER DATATA',
                                   accords=[
                                       Accord(name='floral', background='rgb(255, 95, 141)', width='100%', opacity='1'),
                                       Accord(name='animalic', background='rgb(142, 75, 19)', width='59.0798%',
                                              opacity='0.649255')],
                                   notes=[
                                       Note(name='Frangipani', category=NoteCategory.MIDDLE, width='5.0', opacity='1.0',
                                            image_url='https://fimgs.net/mdimg/sastojci/t.151.jpg'),
                                       Note(name='TestBNote', category=NoteCategory.MIDDLE, width='3.4', opacity='1.0',
                                            image_url='https://fimgs.net/mdimg/sastojci/t.151.jpg'),
                                       Note(name='Iris', category=NoteCategory.MIDDLE, width='2.5', opacity='0.735089',
                                            image_url='https://fimgs.net/mdimg/sastojci/t.11.jpg')], url='no-url')
    return debug_perfume
