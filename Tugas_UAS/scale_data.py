import tarfile
from itertools import islice

# Fungsi untuk memuat ulasan Yelp dari file lokal tar
def load_yelp_reviews(num_docs):
    # Path file lokal
    f = '/mnt/d/Virtual Machines/tugas_infrastruktur/ums-l200220232.github.io/Tugas_UAS/data_group.tgz'

    try:
        with tarfile.open(f) as tar:
            print('Reading tar file...')
            # Path relatif file CSV di dalam arsip tar
            datafile = tar.extractfile('data_group.csv')  # Pastikan path ini benar dalam file tar Anda
            if datafile is None:
                raise FileNotFoundError("File 'data_group.csv' tidak ditemukan di dalam arsip tar.")
            return [line.decode('utf-8').strip() for line in islice(datafile, num_docs)]
    except Exception as e:
        print(f"Error saat memuat file tar: {e}")
        raise

def make_matrix(docs):
    # Implementasi dummy untuk membuat matriks data dari dokumen
    # Ganti dengan logika sesuai kebutuhan Anda
    print(f"Creating matrix for {len(docs)} documents...")
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    mtx = vectorizer.fit_transform(docs)
    return mtx, vectorizer.get_feature_names_out()