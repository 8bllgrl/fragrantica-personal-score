import sqlite3
import matplotlib.pyplot as plt
import random

from matplotlib import cm


# Helper to convert rgb() string to (r, g, b) float tuple
def rgb_string_to_tuple(rgb_string):
    rgb_values = rgb_string.strip("rgb()").split(",")
    return tuple(int(v.strip()) / 255 for v in rgb_values)

# Helper to generate a random color
def random_color():
    return (random.random(), random.random(), random.random())

# Database path
DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_4420251217.db"

# Connect to the database
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Query 1: Accords
query_accords = """
SELECT
    a.name AS accord_name,
    a.background AS color,
    ROUND(SUM(pa.score), 2) AS accord_score
FROM PerfumeAccords pa
JOIN Accords a ON pa.accord_id = a.id
GROUP BY a.id, a.name, a.background
ORDER BY accord_score DESC
"""
cursor.execute(query_accords)
accords_data = cursor.fetchall()

# Query 2: Notes
query_notes = """
SELECT
    n.name AS note_name,
    ROUND(SUM(pn.score), 2) AS note_score
FROM PerfumeNotes pn
JOIN Notes n ON pn.note_id = n.id
GROUP BY n.id, n.name
ORDER BY note_score DESC
"""
cursor.execute(query_notes)
notes_data = cursor.fetchall()

# Close DB connection
conn.close()

### === FIGURE 1: ACCORDS ===
accord_names = [row[0] for row in accords_data]
accord_scores = [row[2] for row in accords_data]
accord_colors = [rgb_string_to_tuple(row[1]) for row in accords_data]

plt.figure("Accords", figsize=(12, 6))
bars1 = plt.bar(accord_names, accord_scores, color=accord_colors)
plt.ylabel('Accord Score')
plt.title('Top Perfume Accords by Score')
plt.xticks(rotation=45, ha='right')

# Add score labels
for bar, score in zip(bars1, accord_scores):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{score}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()

### === FIGURE 2: NOTES (Random Colors) ===
note_names = [row[0] for row in notes_data]
note_scores = [row[1] for row in notes_data]

# Normalize score values for colormap (0 to 1 scale)
norm = plt.Normalize(min(note_scores), max(note_scores))
cmap = cm.get_cmap('plasma')  # Try 'plasma', 'viridis', etc. for other styles
note_colors = [cmap(norm(score)) for score in note_scores]


plt.figure("Notes", figsize=(12, 6))
bars2 = plt.bar(note_names, note_scores, color=note_colors)
plt.ylabel('Note Score')
plt.title('Top Perfume Notes by Score')
plt.xticks(rotation=45, ha='right')

# Add score labels
for bar, score in zip(bars2, note_scores):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{score}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()

# Show both figures
plt.show()
