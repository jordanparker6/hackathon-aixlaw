import numpy as np
import umap
from sklearn.cluster import DBSCAN

class Compare:
    def __init__(self):
        self.umap = umap.UMAP(n_neighbors=5, min_dist=0.3, random_state=42)
        self.model = DBSCAN(eps=0.2, min_samples=5)

    def fit(self, X: np.ndarray):
        """Fit the model to the data by fitting a 2d dimension and clustering"""
        self._embeddings = self.umap.fit_transform(X)
        self.labels = self.model.fit(self._embeddings)
        self.labels = 
    
    def check(self, X: np.ndarray):
        """Check if a vector is in a cluster"""
        vector = vector_to_check.reshape(1, -1)
        embeddings = self.umap.transform(vector)
        labels = self.model.predict(embeddings)
        return labels

    def is_in_cluster(self, vector, label):
        """Check if in cluster or not"""
        return np.any(self.labels == label)
