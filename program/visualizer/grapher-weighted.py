# -----------------------------
# A LITTLE FLAWED as some notes go into the negative only because I rated them that way.
# -----------------------------
import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from fuzzywuzzy import process, fuzz
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

# DB_PATH = r'D:\sqlite_exp\frag\fragrance_51520251243.db'
DB_PATH = r'D:\sqlite_exp\frag\fragrance_520OKONLYforgraphing.db'

# -----------------------------
# Step 1: Fetch Data with Scores
# -----------------------------
def fetch_perfume_notes_and_accords(conn):
    query = '''
        SELECT p.perfume_name, n.name AS component, 'note' AS type, pn.score
        FROM Perfumes p
        JOIN PerfumeNotes pn ON p.id = pn.perfume_id
        JOIN Notes n ON pn.note_id = n.id
        UNION ALL
        SELECT p.perfume_name, a.name AS component, 'accord' AS type, pa.score
        FROM Perfumes p
        JOIN PerfumeAccords pa ON p.id = pa.perfume_id
        JOIN Accords a ON pa.accord_id = a.id
    '''
    return pd.read_sql_query(query, conn)

# -----------------------------
# Step 2: Normalize Notes
# -----------------------------
def normalize_notes(notes, threshold=90):
    unique_notes = list(set(notes))
    mapping = {}

    for note in unique_notes:
        if mapping:
            result = process.extractOne(note, mapping.keys(), scorer=fuzz.token_sort_ratio)
            if result is not None:
                match, score = result
                if score >= threshold:
                    mapping[note] = mapping[match]
                    continue
        mapping[note] = note

    return mapping

# -----------------------------
# Step 3: Build Weighted Matrix
# -----------------------------
def build_weighted_perfume_note_matrix(df):
    matrix_df = df.pivot_table(index='perfume_name',
                                columns='normalized_note',
                                values='score',
                                aggfunc='sum',
                                fill_value=0)

    # Optional normalization: Normalize per perfume (row-wise)
    matrix_df = matrix_df.div(matrix_df.sum(axis=1), axis=0).fillna(0)

    return matrix_df.index.tolist(), matrix_df.values, matrix_df

# -----------------------------
# Step 4: Reduce & Plot
# -----------------------------
def reduce_and_plot(names, matrix, df, n_clusters=5):
    tsne = TSNE(n_components=2, metric="cosine", perplexity=10, random_state=42)
    reduced = tsne.fit_transform(matrix)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(reduced)

    # Build note description per perfume
    note_map = df.groupby('perfume_name')['normalized_note'].apply(
        lambda notes: ', '.join(sorted(set(notes)))).to_dict()

    df_plot = pd.DataFrame({
        'perfume': names,
        'x': reduced[:, 0],
        'y': reduced[:, 1],
        'cluster': labels,
        'notes': [note_map.get(name, '') for name in names]
    })

    # Console log
    print("\nPerfumes with their notes, assigned clusters, and coordinates:\n")
    for _, row in df_plot.iterrows():
        print(f"Perfume: {row['perfume']}")
        print(f"Notes: {row['notes']}")
        print(f"Assigned Cluster: {row['cluster'] + 1}")
        print(f"x: {row['x']:.2f}, y: {row['y']:.2f}")
        print("-" * 50)

    fig = px.scatter(
        df_plot,
        x='x',
        y='y',
        color='cluster',
        hover_name='perfume',
        hover_data={'notes': True},
        title='Perfume Clusters Based on Weighted Note & Accord Similarity',
        labels={'x': 'Similarity Axis 1', 'y': 'Similarity Axis 2'},
        color_continuous_scale=px.colors.sequential.Purpor
    )

    fig.update_layout(
        autosize=True,
        height=None,
        width=None,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title='Cluster'),
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333'),
        plot_bgcolor='black'
    )
    fig.show()

# -----------------------------
# Step 5: Main Function
# -----------------------------
def main():
    conn = sqlite3.connect(DB_PATH)
    df = fetch_perfume_notes_and_accords(conn)

    component_map = normalize_notes(df['component'])
    df['normalized_note'] = df['component'].map(component_map)

    perfume_names, matrix_array, matrix_df = build_weighted_perfume_note_matrix(df)
    reduce_and_plot(perfume_names, matrix_array, df)

    conn.close()

if __name__ == '__main__':
    main()
