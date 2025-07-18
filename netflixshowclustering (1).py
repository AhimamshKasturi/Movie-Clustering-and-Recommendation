# -*- coding: utf-8 -*-
"""NetflixShowClustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gr8FHKl4_LXhqI0rh2z3W02Vz6_EArEg
"""

# ==========================
# Install & import packages
# ==========================
!pip install requests pandas numpy scikit-learn seaborn matplotlib
!pip install fuzzywuzzy[speedup]

import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import itertools

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA

from fuzzywuzzy import process

from google.colab import drive
from google.colab import userdata

sns.set(style="whitegrid")

# ==========================
# API Key
# ==========================
API_KEY = userdata.get('TMDB_Key')  # or hardcode your key here

"""Data collection"""

# ==========================
# Get TV shows data from TMDB
# ==========================
def get_tv_shows(api_key, pages=5, endpoint="tv/popular"):
    BASE_URL = 'https://api.themoviedb.org/3'
    dataset = []

    for page in range(1, pages+1):
        url = f"{BASE_URL}/{endpoint}?api_key={api_key}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error:", response.json())
            continue
        shows = response.json()['results']

        for show in shows:
            show_id = show['id']
            details_url = f"{BASE_URL}/tv/{show_id}?api_key={api_key}&language=en-US"
            details = requests.get(details_url).json()

            genres = [g['name'] for g in details.get('genres', [])]
            episode_time = details.get('episode_run_time', [0])[0] if details.get('episode_run_time') else 0

            dataset.append({
                'name': show.get('name'),
                'rating': show.get('vote_average'),
                'episode_run_time': episode_time,
                'genres': genres,
                'popularity': show.get('popularity')
            })

            time.sleep(0.2)  # avoid hitting rate limits

    return pd.DataFrame(dataset)

# Fetch data
df = get_tv_shows(API_KEY, pages=5)
print(df.head())

"""Data preparation & feature engineering"""

# ==========================
# Handle missing genres & one-hot encoding
# ==========================
df['genres'] = df['genres'].apply(lambda x: x if isinstance(x, list) else [])

all_genres = set(g for sublist in df['genres'] for g in sublist)
for genre in all_genres:
    df[genre] = df['genres'].apply(lambda x: 1 if genre in x else 0)

# ==========================
# Prepare features for clustering
# ==========================
X = df[['rating', 'episode_run_time', 'popularity'] + list(all_genres)]
X.fillna(X.mean(), inplace=True)

# ==========================
# Scale data
# ==========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""EDA & Elbow method"""

# ==========================
# Elbow Method to find optimal K
# ==========================
inertia = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8,4))
sns.lineplot(x=K_range, y=inertia, marker='o')
plt.title('Elbow Method - Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

"""Clustering"""

# ==========================
# K-Means
# ==========================
kmeans = KMeans(n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# ==========================
# Hierarchical Clustering
# ==========================
agg = AgglomerativeClustering(n_clusters=4)
df['AggloCluster'] = agg.fit_predict(X_scaled)

# ==========================
# DBSCAN
# ==========================
dbscan = DBSCAN(eps=2, min_samples=5)
df['DBSCANCluster'] = dbscan.fit_predict(X_scaled)

"""PCA Visualization"""

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df['Cluster'], palette='tab10')
plt.title('Netflix Shows Clustering (PCA Reduced)')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

"""Cluster analysis & EDA plots"""

# ==========================
# 🔍 Cluster summaries
# ==========================
print(df.groupby('Cluster')[['rating', 'episode_run_time', 'popularity']].mean())

# ==========================
# 🔍 Dominant genres by cluster
# ==========================
print(df.groupby('Cluster')[list(all_genres)].mean())

# ==========================
# 🔍 Popular genres
# ==========================
all_genres_flat = list(itertools.chain(*df['genres']))
pd.Series(all_genres_flat).value_counts().plot(kind='bar', figsize=(10,5), color='skyblue')
plt.title("Most Common Genres")
plt.ylabel("Count")
plt.show()

# ==========================
# 🔍 Runtime vs Rating
# ==========================
sns.scatterplot(x='episode_run_time', y='rating', data=df)
plt.title("Episode Run Time vs Rating")
plt.show()

# ==========================
# 🔍 Correlation heatmap
# ==========================
corr_features = ['rating', 'episode_run_time', 'popularity'] + list(all_genres)
plt.figure(figsize=(14,10))
sns.heatmap(df[corr_features].corr(), cmap='coolwarm', annot=True)
plt.title("Feature Correlation Heatmap")
plt.show()

"""Recommendations using Fuzzy input"""

def find_best_matches(input_names, choices, cutoff=90):
    matches = []
    for name in input_names:
        best_match, score = process.extractOne(name, choices)
        if score >= cutoff:
            matches.append(best_match)
    return matches

def recommend_custom_input_fuzzy(n=5):
    user_input = input("Enter 1, 2 or 3 shows you like (comma-separated): ")
    liked_show_names = [name.strip() for name in user_input.split(",")]

    choices = df['name'].unique()
    best_matches = find_best_matches(liked_show_names, choices)

    if not best_matches:
        print("No close matches found.")
        print("Some shows you can pick from:", df['name'].sample(5).to_list())
        return

    cluster_id = df[df['name'].isin(best_matches)]['Cluster'].mode().iloc[0]
    recs = df[(df['Cluster'] == cluster_id) & (~df['name'].isin(best_matches))]

    print(f"Found closest matches: {best_matches}")
    print(f"Recommendations from cluster {cluster_id}:")
    print(recs[['name', 'rating', 'episode_run_time', 'genres']].sample(min(n, len(recs))))

recommend_custom_input_fuzzy()

"""Save as CSV"""

# ==========================
# Export for Tableau
# ==========================
drive.mount('/content/drive')
df.to_csv('/content/drive/MyDrive/NetflixShowClustering/netflix_shows_clustered.csv', index=False)