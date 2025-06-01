import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from fuzzywuzzy import process, fuzz
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import plotly.io as pio


pio.renderers.default = "browser"  # Open in default browser

DB_PATH = r'D:\sqlite_exp\frag\fragrance_51520251243.db'

def fetch_perfume_notes(conn):
    query = '''
        SELECT p.perfume_name, n.name AS note
        FROM Perfumes p
        JOIN PerfumeNotes pn ON p.id = pn.perfume_id
        JOIN Notes n ON pn.note_id = n.id
    '''
    return pd.read_sql_query(query, conn)
def fetch_perfume_notes_and_accords(conn):
    query = '''
        SELECT p.perfume_name, n.name AS component, 'note' AS type
        FROM Perfumes p
        JOIN PerfumeNotes pn ON p.id = pn.perfume_id
        JOIN Notes n ON pn.note_id = n.id
        UNION ALL
        SELECT p.perfume_name, a.name AS component, 'accord' AS type
        FROM Perfumes p
        JOIN PerfumeAccords pa ON p.id = pa.perfume_id
        JOIN Accords a ON pa.accord_id = a.id
    '''
    return pd.read_sql_query(query, conn)

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

def build_perfume_note_matrix(df):
    perfume_groups = df.groupby('perfume_name')['normalized_note'].apply(lambda x: ' '.join(x))
    vectorizer = CountVectorizer()
    note_matrix = vectorizer.fit_transform(perfume_groups)
    return perfume_groups.index.tolist(), note_matrix


def reduce_and_plot(names, matrix, df, n_clusters=5):
    # Reduce dimensions (t-SNE) with a fixed random state for reproducibility
    tsne = TSNE(n_components=2, metric="cosine", perplexity=10, random_state=42)
    reduced = tsne.fit_transform(matrix.toarray())

    # Apply KMeans clustering with a fixed random state for reproducibility
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(reduced)

    # Group notes for each perfume (for hover)
    note_map = df.groupby('perfume_name')['normalized_note'].apply(lambda notes: ', '.join(sorted(set(notes)))).to_dict()

    # Build DataFrame for plotting
    df_plot = pd.DataFrame({
        'perfume': names,
        'x': reduced[:, 0],
        'y': reduced[:, 1],
        'cluster': labels,
        'notes': [note_map.get(name, '') for name in names]
    })

    # Print each perfume with their notes, assigned cluster, and x, y coordinates in the console
    print("\nPerfumes with their notes, assigned clusters, and coordinates:\n")
    for _, row in df_plot.iterrows():
        perfume_name = row['perfume']
        perfume_notes = row['notes']
        cluster_num = row['cluster'] + 1  # Add 1 for more user-friendly display (e.g., Cluster 1 instead of Cluster 0)
        x_coord = row['x']
        y_coord = row['y']
        print(f"Perfume: {perfume_name}")
        print(f"Notes: {perfume_notes}")
        print(f"Assigned Cluster: {cluster_num}")
        print(f"x: {x_coord:.2f}, y: {y_coord:.2f}")
        print("-" * 50)

    # Create the Plotly scatter plot with a different color palette
    fig = px.scatter(
        df_plot,
        x='x',
        y='y',
        color='cluster',
        hover_name='perfume',
        hover_data={'notes': True},
        title='Perfume Clusters Based on Note Similarity',
        labels={'x': 'Similarity Axis 1', 'y': 'Similarity Axis 2'},
        color_continuous_scale=px.colors.sequential.Purpor    # Apply a sequential color scale
    )

    fig.update_layout(
        autosize=True,
        height=None,
        width=None,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title='Cluster'),
        xaxis=dict(
            gridcolor='#333333'  # Your custom dark grey for x-axis grid
        ),
        yaxis=dict(
            gridcolor='#333333'  # Your custom dark grey for x-axis grid
        ),
        plot_bgcolor='black'  # Optional: Added plot background color
    )
    fig.show()





def main():
    conn = sqlite3.connect(DB_PATH)
    # df = fetch_perfume_notes(conn)
    df = fetch_perfume_notes_and_accords(conn)
    # note_map = normalize_notes(df['note'])
    # df['normalized_note'] = df['note'].map(note_map)
    component_map = normalize_notes(df['component'])
    df['normalized_note'] = df['component'].map(component_map)

    perfume_names, matrix = build_perfume_note_matrix(df)
    reduce_and_plot(perfume_names, matrix, df)

    conn.close()


if __name__ == '__main__':
    main()
