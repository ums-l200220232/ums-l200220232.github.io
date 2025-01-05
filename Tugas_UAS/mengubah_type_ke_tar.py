import tarfile

# Nama folder yang ingin dikompres
directory_to_compress = 'data_group.csv'  # Ganti dengan nama folder yang ingin dikompres
tar_file = 'data_group.tgz'

# Membuat file TAR dan menambahkan seluruh folder
with tarfile.open(tar_file, 'w:gz') as tar:
    tar.add(directory_to_compress, arcname='data_group.csv')

print(f"Folder {directory_to_compress} telah berhasil dikompres menjadi {tar_file}.")
