import re
import torch
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer


# Load the data into a pandas dataframe
df = pd.read_csv("../data/final_data.csv")

# Text cleaning
df['corpus_text'] = df['corpus_text'].str.lower()
df['corpus_text'] = df['corpus_text'].apply(lambda x: re.sub('[^\w\s]', '', x))
df['corpus_text'] = df['corpus_text'].apply(lambda x: re.sub('\d+', '', x))

model= SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
embedder = SentenceTransformer('all-mpnet-base-v2')
corpus= df['corpus_text'].to_list()
corpus_embeddings = embedder.encode(corpus)

# Normalize the embeddings to unit length
corpus_embeddings = corpus_embeddings /  np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)

# Perform kmean clustering
clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.5, affinity='euclidean', linkage='ward')
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_

clustered_sentences = {}
for sentence_id, cluster_id in enumerate(cluster_assignment):
    if cluster_id not in clustered_sentences:
        clustered_sentences[cluster_id] = []
    clustered_sentences[cluster_id].append(corpus[sentence_id])

df['cluster']=cluster_assignment
df['cluster'].value_counts()

# Generate a name for the cluster labels
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['corpus_text'])

def get_cluster_keywords(cluster_id):
    cluster_rows = df[df['cluster'] == cluster_id]
    cluster_tfidf = tfidf_matrix[cluster_rows.index]
    sums = np.array(cluster_tfidf.sum(axis=0)).ravel()
    sorted_indices = np.argsort(sums)[::-1]
    feature_names = np.array(tfidf.get_feature_names())
    keywords = feature_names[sorted_indices[:5]]
    return ', '.join(keywords)

df['cluster_name'] = df['cluster'].apply(lambda x: get_cluster_keywords(x))
#df[['channel_id', 'channel_url', 'cluster', 'cluster_name']].to_csv('../data/clustered_data.csv')