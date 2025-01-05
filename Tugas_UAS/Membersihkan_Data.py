import pandas as pd
import re

# 1. Baca File TXT
file_path1 = "Chat WhatsApp dengan Peserta E-SPORT PTMA 2024 Khusus Mahasiswa Yumes.txt"
file_path2 = "Chat WhatsApp dengan UKM BADMINTON 2324.txt"

# Membaca file teks dan menggabungkannya
with open(file_path1, 'r', encoding='utf-8') as file1:
    data1 = file1.readlines()

with open(file_path2, 'r', encoding='utf-8') as file2:
    data2 = file2.readlines()

# Gabungkan kedua data
data = pd.DataFrame(data1 + data2, columns=['raw_message'])

# 2. Ekstrak Pesan
def extract_message(row):
    if isinstance(row, str):  # Cek apakah row berupa string
        match = re.search(r' - [^:]+: (.+)', row)  # Hanya ekstrak pesan
        if match:
            return match.group(1)  # Kembalikan pesan (grup ke-2)
    return None  # Jika tidak ada kecocokan atau bukan string

# Pastikan tidak ada nilai kosong pada 'raw_message'
data['raw_message'] = data['raw_message'].fillna('')

# Terapkan regex untuk mengekstrak hanya pesan
data['message'] = data['raw_message'].apply(extract_message)

# Hapus baris kosong (pesan sistem atau baris tanpa format pengguna-pesan)
data_clean = data.dropna(subset=['message']).copy()

# 3. Bersihkan Pesan
def clean_text(text):
    if not isinstance(text, str):  # Pastikan input adalah string
        return ''
    # Hanya menyimpan angka, huruf, spasi, dan tanda baca umum
    cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?;:\'"-]', '', text)
    return cleaned.strip()

# Bersihkan isi pesan
data_clean.loc[:, 'cleaned_message'] = data_clean['message'].apply(clean_text)

# 4. Simpan Hasil Pembersihan ke File CSV Baru
output_file = "data_group.csv"
data_clean[['cleaned_message']].to_csv(output_file, index=False, encoding='utf-8', header=False)

print(f"Data berhasil dibersihkan dan hanya menyisakan chat. Hasil disimpan ke {output_file}.")
