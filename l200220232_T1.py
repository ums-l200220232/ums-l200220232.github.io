from metaflow import FlowSpec, step

class perjalanan_kuliah(FlowSpec):
    """Simulasi perjalanan akademik di jurusan Informatika."""

    def _init_(self):
        super()._init_()
        self.nilai_uts = None
        self.nilai_uas = None
        self.nilai_akhir = None

    @step
    def start(self):
        """Langkah awal perjalanan kuliah."""
        print("Membayar seluruh biaya kuliah untuk satu semester, "
              "agar perjalanan akademik berjalan tanpa hambatan.")
        self.next(self.proses_pendaftaran)

    @step
    def proses_pendaftaran(self):
        """Langkah untuk melakukan pendaftaran kelas."""
        print("Melakukan pendaftaran ke dalam kelas-kelas yang tersedia...")
        self.next(self.mengikuti_perkuliahan)

    @step
    def mengikuti_perkuliahan(self):
        """Langkah untuk menghadiri dan mengikuti perkuliahan."""
        print("Mengikuti perkuliahan secara rutin dan berpartisipasi aktif dalam kegiatan...")
        self.total_pertemuan = 14
        self.kehadiran = 0

        for pertemuan in range(1, self.total_pertemuan + 1):
            hadir = True  # Simulasi kehadiran setiap pertemuan
            if hadir:
                self.kehadiran += 1
            print(f"Pertemuan {pertemuan}: {'Hadir' if hadir else 'Absen'}")
        
        self.batas_kehadiran = int(0.75 * self.total_pertemuan)
        if self.kehadiran >= self.batas_kehadiran:
            print("Kehadiran memenuhi syarat.")
        else:
            print("Kehadiran tidak memenuhi syarat.")
            self.next(self.end)
        self.next(self.menerima_nilai)

    @step
    def menerima_nilai(self):
        """Langkah untuk mendapatkan nilai UTS dan UAS."""
        self.nilai_uts = 85  # Simulasi nilai UTS
        self.nilai_uas = 88  # Simulasi nilai UAS
        print(f"Nilai UTS: {self.nilai_uts}")
        print(f"Nilai UAS: {self.nilai_uas}")
        self.next(self.hitung_nilai_akhir)

    @step
    def hitung_nilai_akhir(self):
        """Menghitung nilai akhir dari UTS dan UAS."""
        self.nilai_akhir = (self.nilai_uts + self.nilai_uas) / 2
        print(f"Nilai akhir keseluruhan: {self.nilai_akhir}")
        self.next(self.end)

    @step
    def end(self):
        """Akhir dari simulasi perjalanan akademik."""
        print("Proses kuliah selesai dengan sukses!")

if _name_ == '_main_':
    perjalanan_kuliah()