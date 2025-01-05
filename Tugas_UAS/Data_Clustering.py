from metaflow import FlowSpec, step, Parameter, resources
from collections import Counter
import numpy as np

class ManyKmeansFlow(FlowSpec):

    num_docs = Parameter('num-docs', help='Number of documents', default=1000)

    @resources(memory=4000)
    @step
    def start(self):
        import scale_data
        print("Step: Start - Loading Yelp reviews")
        docs = scale_data.load_yelp_reviews(self.num_docs)  # Memanggil fungsi dari scale_data.py
        print("Step: Start - Creating matrix")
        self.mtx, self.cols = scale_data.make_matrix(docs)  # Memanggil fungsi dari scale_data.py
        self.k_params = list(range(3, 6, 1))  # K range: 3 to 5
        print(f"Step: Start - k_params = {self.k_params}")
        self.next(self.train_kmeans, foreach='k_params')

    @step
    def train_kmeans(self):
        from sklearn.cluster import KMeans
        self.k = self.input
        print(f"Step: Train KMeans - Training for k={self.k}")
        kmeans_model = KMeans(n_clusters=self.k)
        kmeans_model.fit(self.mtx)
        self.kmeans_output = kmeans_model.labels_
        print(f"Model for k={self.k} trained successfully.")
        self.next(self.analyze)  # Transisi ke analyze

    @step
    def analyze(self):
        print(f"Analyzing results for k={self.k}")
        clusters = self.kmeans_output
        cluster_docs = {i: [] for i in range(self.k)}

        # Memisahkan dokumen berdasarkan cluster
        for doc_idx, cluster_id in enumerate(clusters):
            cluster_docs[cluster_id].append(doc_idx)

        # Menentukan kata-kata top berdasarkan frekuensi di setiap cluster
        top_words_per_cluster = {}
        for cluster_id, doc_indices in cluster_docs.items():
            word_counts = Counter()
            for doc_idx in doc_indices:
                # Ambil dokumen dari matriks
                word_counts.update(self.mtx[doc_idx].nonzero()[1])

            # Mapping word indices ke kata beserta frekuensinya
            words_with_freq = [(self.cols[word_idx], count) for word_idx, count in word_counts.most_common(3)]
            top_words_per_cluster[cluster_id] = words_with_freq

        self.top_words = top_words_per_cluster
        print(f"Top words for k={self.k}: {self.top_words}")
        self.next(self.join)  # Transisi ke join

    @step
    def join(self, inputs):
        print("Step: Join - Merging results")
        self.top = {inp.k: inp.top_words for inp in inputs}
        self.next(self.end)

    @step
    def end(self):
        print("Step: End - Flow completed")
        
        # Menampilkan hasil ke layar
        print("Top words for each k:")
        for k, clusters in self.top.items():
            print(f"For k={k}:")
            for cluster_id, words in clusters.items():
                print(f"  Cluster {cluster_id}: {words}")
        
        # Analisis hasil
        print("Analysis: Clustering results indicate that...")

if _name_ == '_main_':
    ManyKmeansFlow()