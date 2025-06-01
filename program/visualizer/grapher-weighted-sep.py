import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity # You import this but don't use it, consider if it's needed.
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt # You import this but don't use it, consider if it's needed.
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
# Step 2: Normalize Notes (modified)
# -----------------------------
def normalize_components(components_with_type, threshold=90):
    unique_components = list(set(components_with_type))
    mapping = {}

    for comp_with_type in unique_components:
        if mapping:
            result = process.extractOne(comp_with_type, mapping.keys(), scorer=fuzz.token_sort_ratio)
            if result is not None:
                match, score = result
                if score >= threshold:
                    mapping[comp_with_type] = mapping[match]
                    continue
        mapping[comp_with_type] = comp_with_type

    return mapping

# -----------------------------
# Step 3: Build Weighted Matrix (modified)
# -----------------------------
def build_weighted_perfume_component_matrix(df):
    matrix_df = df.pivot_table(index='perfume_name',
                                columns='normalized_component_with_type', # Changed column name
                                values='score',
                                aggfunc='sum',
                                fill_value=0)

    # Optional normalization: Normalize per perfume (row-wise)
    matrix_df = matrix_df.div(matrix_df.sum(axis=1), axis=0).fillna(0)

    return matrix_df.index.tolist(), matrix_df.values, matrix_df

# -----------------------------
# Step 4: Reduce & Plot (modified)
# -----------------------------
def reduce_and_plot(names, matrix, df, n_clusters=5):
    tsne = TSNE(n_components=2, metric="cosine", perplexity=10, random_state=42)
    reduced = tsne.fit_transform(matrix)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10) # Added n_init for KMeans
    labels = kmeans.fit_predict(reduced)

    # Build component description per perfume (modified to use original component and type)
    # This will display "coconut (note), coconut (accord)" for clarity
    df['original_component_display'] = df.apply(lambda row: f"{row['component']} ({row['type']})", axis=1)
    component_map = df.groupby('perfume_name')['original_component_display'].apply(
        lambda components: ', '.join(sorted(set(components)))).to_dict()

    df_plot = pd.DataFrame({
        'perfume': names,
        'x': reduced[:, 0],
        'y': reduced[:, 1],
        'cluster': labels,
        'components': [component_map.get(name, '') for name in names] # Changed key name
    })

    # Sort df_plot by cluster before printing
    df_plot_sorted = df_plot.sort_values(by='cluster').reset_index(drop=True)

    # Console log
    print("\nPerfumes with their components, assigned clusters, and coordinates (Sorted by Cluster):\n")
    for _, row in df_plot_sorted.iterrows(): # Iterate over the sorted DataFrame
        print(f"Perfume: {row['perfume']}")
        print(f"Components: {row['components']}")
        print(f"Assigned Cluster: {row['cluster'] + 1}")
        print(f"x: {row['x']:.2f}, y: {row['y']:.2f}")
        print("-" * 50)

    fig = px.scatter(
        df_plot,
        x='x',
        y='y',
        color='cluster',
        hover_name='perfume',
        # hover_data={'components': True}, # Added hover_data back in
        title='Perfume Clusters Based on Weighted Note & Accord Similarity (Distinct Types)', # Updated title
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
# Step 5: Main Function (modified)
# -----------------------------
def main():
    conn = sqlite3.connect(DB_PATH)
    df = fetch_perfume_notes_and_accords(conn)

    # Create a new column that combines component name and type
    df['component_with_type'] = df.apply(lambda row: f"{row['component']}_{row['type']}", axis=1)

    component_map = normalize_components(df['component_with_type'])
    df['normalized_component_with_type'] = df['component_with_type'].map(component_map)

    perfume_names, matrix_array, matrix_df = build_weighted_perfume_component_matrix(df)
    reduce_and_plot(perfume_names, matrix_array, df)

    conn.close()

if __name__ == '__main__':
    main()