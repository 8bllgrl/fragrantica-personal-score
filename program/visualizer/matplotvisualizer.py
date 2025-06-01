import sqlite3
import matplotlib.pyplot as plt
from matplotlib import cm
from program.model.parfum import Enjoyment

def rgb_string_to_tuple(rgb_string):
    rgb_values = rgb_string.strip("rgb()").split(",")
    return tuple(int(v.strip()) / 255 for v in rgb_values)

def get_adjusted_note_scores(cursor):
    cursor.execute("""
        SELECT
            n.name,
            pn.width,
            p.enjoyment_score
        FROM PerfumeNotes pn
        JOIN Notes n ON pn.note_id = n.id
        JOIN Perfumes p ON pn.perfume_id = p.id
    """)
    adjusted_scores = {}

    for name, width, enjoyment_score in cursor.fetchall():
        try:
            enjoyment = Enjoyment(enjoyment_score)
            multiplier = enjoyment.weight_multiplier
        except ValueError:
            multiplier = 1.0
        score = width * multiplier
        adjusted_scores[name] = adjusted_scores.get(name, 0) + score

    return sorted(
        [(name, round(score, 2)) for name, score in adjusted_scores.items()],
        key=lambda x: x[1],
        reverse=True
    )

def show_plot(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.name, a.background, ROUND(SUM(pa.width), 2)
        FROM PerfumeAccords pa
        JOIN Accords a ON pa.accord_id = a.id
        GROUP BY a.id, a.name, a.background
        ORDER BY 3 DESC
    """)
    accords_data = cursor.fetchall()

    accord_names = [row[0] for row in accords_data]
    accord_scores = [row[2] for row in accords_data]
    accord_colors = [rgb_string_to_tuple(row[1]) for row in accords_data]

    plt.figure("Accords", figsize=(12, 6))
    bars1 = plt.bar(accord_names, accord_scores, color=accord_colors)
    plt.ylabel('Accord Score')
    plt.title('Top Perfume Accords by Score')
    plt.xticks(rotation=45, ha='right')

    for bar, score in zip(bars1, accord_scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f'{score}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    note_scores = get_adjusted_note_scores(cursor)
    note_names = [row[0] for row in note_scores]
    note_values = [row[1] for row in note_scores]

    norm = plt.Normalize(min(note_values), max(note_values))
    cmap = cm.get_cmap('viridis')
    note_colors = [cmap(norm(score)) for score in note_values]

    plt.figure("Notes (Weighted by Enjoyment)", figsize=(14, 7))
    bars2 = plt.bar(note_names, note_values, color=note_colors)
    plt.ylabel('Note Score (Width × Enjoyment Multiplier)')
    plt.title('Note Scores Across All Perfumes (Weighted by Enjoyment)')
    plt.xticks(rotation=45, ha='right')

    for bar, score in zip(bars2, note_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f'{score}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()

    conn.close()
    plt.show()

# CLI entrypoint for standalone usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python matplotvisualizer.py <db_path>")
        sys.exit(1)
    show_plot(sys.argv[1])
