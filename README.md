# Dashboard Ketenagakerjaan Provinsi Jawa Timur

Dashboard analitik interaktif kondisi ketenagakerjaan 38 kabupaten/kota di Provinsi Jawa Timur, dibangun untuk mendukung kebutuhan monitoring **Satu Data Jatim — Smart Province, Diskominfo Provinsi Jawa Timur**.

Dashboard ini tidak berhenti di angka provinsi. Fokus utamanya adalah **kesenjangan antarwilayah**: kabupaten/kota mana yang tertinggal, wilayah mana yang polanya paling tidak stabil dari waktu ke waktu, dan wilayah mana yang perlu diprioritaskan lebih dulu untuk intervensi kebijakan.

> Status: Project 1, magang Diskominfo Provinsi Jawa Timur (13 Juli – 14 Agustus 2026), dengan mentor Bapak Agus.

---

## Daftar Isi

1. [Ringkasan Proyek](#ringkasan-proyek)
2. [Fitur & Halaman Dashboard](#fitur--halaman-dashboard)
3. [Sumber Data](#sumber-data)
4. [Arsitektur & Alur Data](#arsitektur--alur-data)
5. [Struktur Direktori](#struktur-direktori)
6. [Metodologi Analitik](#metodologi-analitik)
7. [Instalasi & Menjalankan Secara Lokal](#instalasi--menjalankan-secara-lokal)
8. [Deployment](#deployment)
9. [Kamus Data](#kamus-data)
10. [Keterbatasan & Catatan Metodologi](#keterbatasan--catatan-metodologi)
11. [Rencana Pengembangan Lanjutan](#rencana-pengembangan-lanjutan)
12. [Kontak](#kontak)

---

## Ringkasan Proyek

| | |
|---|---|
| **Tujuan** | Menyediakan gambaran ketenagakerjaan Jawa Timur yang granular per kabupaten/kota, bukan sekadar agregat provinsi, untuk mendukung pengambilan keputusan berbasis data di lingkungan Diskominfo Jatim. |
| **Cakupan wilayah** | 38 kabupaten/kota, Provinsi Jawa Timur |
| **Cakupan waktu** | Snapshot Agustus 2023–2025 dan Februari 2024–2026 (data primer & pendamping BPS), diperkaya data historis 2001–2025 (BPS Web API) untuk analisis tren dan volatilitas |
| **Skala analisis** | Provinsi sebagai satu kesatuan cerita besar, dengan granularitas tetap rinci di level kabupaten/kota di mana data tersedia |
| **Teknologi** | Python, Streamlit (multi-page, native `st.navigation`), Pandas, Plotly, scikit-learn (K-Means) |
| **Konsumen** | Diskominfo Provinsi Jawa Timur, dan pihak yang membutuhkan pemetaan ketenagakerjaan Jatim untuk perumusan kebijakan |

Seluruh pipeline pengolahan data (cleaning, validasi, feature engineering, clustering, hingga skor risiko) didokumentasikan penuh di notebook `EDA_KetenagarakerjaanJATIM.ipynb`, dan dashboard ini adalah lapisan penyajian (presentation layer) dari hasil pipeline tersebut.

---

## Fitur & Halaman Dashboard

Dashboard terdiri dari 7 halaman, dapat diakses melalui sidebar (`app.py` → `st.navigation`):

| Halaman | File | Isi |
|---|---|---|
| **Beranda** | `views/beranda.py` | Ringkasan kondisi terkini (TPT & TPAK Februari 2026 vs Februari 2025), peta cepat sebaran TPT antarwilayah |
| **Potret Provinsi** | `views/potret_provinsi.py` | Indikator makro level provinsi — TPT, TPAK, jumlah angkatan kerja, dan tren historis 2008–2025 |
| **Peta & Kesenjangan** | `views/peta_kesenjangan.py` | Choropleth map 38 kab/kota, Composite Index TPT vs Upah dengan **bobot yang bisa diatur pengguna** (slider interaktif), ranking antarwilayah |
| **Sektor Ekonomi** | `views/sektor_ekonomi.py` | Komposisi penyerapan tenaga kerja pada 17 lapangan usaha, level provinsi, 2023–2025 |
| **Karakteristik Pekerja** | `views/karakteristik_pekerja.py` | TPT menurut karakteristik demografis (gender, usia, pendidikan) dan komposisi status pekerjaan (formal/informal), Februari 2024–2026 |
| **Tren Terkini** | `views/tren_terkini.py` | Eksplorasi tren TPT & TPAK historis 2008–2025 per kab/kota (pilih wilayah), profil volatilitas, dampak Krisis 2008 dan COVID-19 |
| **Insight & Rekomendasi** | `views/insight_rekomendasi.py` | Skor risiko early-warning per kab/kota (tier Rendah/Sedang/Tinggi) beserta metodologi penghitungannya |

**Fitur interaktif yang ditonjolkan:**
- Slider bobot Composite Index (TPT vs Upah) — pengguna bisa mengeksplorasi skenario pembobotan selain default 50/50.
- Drill-down per kabupaten/kota di peta dan halaman tren historis.
- Unduh tabel sebagai CSV langsung dari dashboard (`utils.tombol_unduh_csv`).
- Tema warna dan tipografi custom (bukan tema default Streamlit), dikunci ke mode terang agar konsisten di seluruh perangkat pengguna.

---

## Sumber Data

| Berkas | Sumber Resmi | Level | Periode |
|---|---|---|---|
| `Data_Primer_Bersih.xlsx` | BPS Provinsi Jawa Timur — Keadaan Angkatan Kerja Jatim, Agustus 2025 (rilis 17 Maret 2026) | 38 kabupaten/kota | Agustus 2023–2025 |
| `Data_Pendamping_Feb2026.xlsx` | BPS Provinsi Jawa Timur — BRS Jumlah Angkatan Kerja Jatim, Februari 2026 (rilis 5 Mei 2026) | Provinsi | Februari 2024–2026 |
| BPS Web API (`webapi.bps.go.id`) | BPS, domain Jawa Timur (kode 3500) — TPT (`var_id=54`), TPAK (`var_id=277`) | 38 kabupaten/kota | 2001–2025 |
| `jatim_38_kabkota.geojson` | `mahendrayudha/indonesia-geojson` (GitHub), divalidasi manual terhadap nomenklatur BPS | 38 kabupaten/kota | boundary administratif |

Seluruh data mentah disimpan di `data/raw/`. Proses pembersihan, validasi silang, dan transformasi menjadi data siap-pakai (`data/processed/`) dilakukan sepenuhnya di notebook EDA — dashboard **tidak** melakukan pembersihan data saat runtime, hanya membaca hasil akhir yang sudah divalidasi.

---

## Arsitektur & Alur Data

```
                    ┌─────────────────────────────┐
                    │   BPS Jatim (Excel, 2 file)  │
                    │   BPS Web API (historis)     │
                    │   GeoJSON 38 kab/kota         │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
        ┌───────────────────────────────────────────────┐
        │  EDA_KetenagarakerjaanJATIM.ipynb (offline)    │
        │  Data Understanding → Cleaning → EDA →         │
        │  Feature Engineering → Clustering → Skor Risiko│
        └──────────────────────┬──────────────────────────┘
                                │  ekspor .parquet / .csv
                                ▼
                    ┌─────────────────────────┐
                    │   data/processed/*.parquet │
                    └──────────────┬────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────┐
        │   data_loader.py  (cache st.cache_data)      │
        └──────────────────────┬────────────────────────┘
                                │
                                ▼
        ┌─────────────────────────────────────────────┐
        │   app.py → st.navigation → views/*.py        │
        │   utils.py (styling, komponen, format tabel) │
        │   config.py (path, palet warna, label kolom) │
        └─────────────────────────────────────────────┘
                                │
                                ▼
                     Dashboard Streamlit (browser)
```

Prinsip desain: **pipeline analitik berat (join, normalisasi, clustering, scoring) dikerjakan sekali di notebook, bukan di runtime dashboard.** Dashboard hanya membaca file `.parquet` yang sudah bersih dan siap divisualisasikan, sehingga load time tetap cepat meski melibatkan 38 wilayah × banyak indikator × rentang waktu panjang.

---

## Struktur Direktori

```
dashboard/
├── app.py                     # Entry point, konfigurasi navigasi & sidebar
├── config.py                  # Path data, palet warna, label kolom, konfigurasi Plotly
├── data_loader.py             # Fungsi load data dengan caching (st.cache_data)
├── utils.py                   # Styling CSS custom, komponen UI (kartu metrik, tabel, badge)
├── requirements.txt
├── Procfile                   # Konfigurasi deployment (Heroku-style)
├── .streamlit/
│   └── config.toml            # Tema Streamlit dikunci ke mode terang
├── views/
│   ├── beranda.py
│   ├── potret_provinsi.py
│   ├── peta_kesenjangan.py
│   ├── sektor_ekonomi.py
│   ├── karakteristik_pekerja.py
│   ├── tren_terkini.py
│   └── insight_rekomendasi.py
├── assets/
│   └── geojson/
│       └── jatim_38_kabkota.geojson
└── data/
    ├── raw/                   # Data mentah BPS (Excel)
    │   ├── Data_Primer_Bersih.xlsx
    │   └── Data_Pendamping_Feb2026.xlsx
    └── processed/             # Output notebook EDA, siap pakai dashboard
        ├── master_kabkota.parquet / .csv
        ├── kabkota_long.parquet / .csv
        ├── sektor_long.parquet
        ├── table4_karakteristik_tpt.parquet
        ├── table5_karakteristik_pekerja.parquet
        ├── tpt_kabkota_historis_2001_2025.parquet
        ├── tpt_kabkota_historis_reliable_2008_2025.parquet
        ├── tpak_kabkota_historis_reliable.parquet / .csv
        ├── tpt_tpak_gabungan_2008_2025.parquet
        ├── profil_volatilitas_kabkota.parquet / .csv
        └── skor_risiko_kabkota_2025.parquet / .csv
```

---

## Metodologi Analitik

Detail lengkap perhitungan ada di notebook (`EDA_KetenagarakerjaanJATIM.ipynb`, Bagian 4–12). Ringkasan metodologi yang dipakai di dashboard:

### 1. Composite Index (Peta & Kesenjangan)
Skor gabungan TPT dan Upah per kab/kota, dinormalisasi ke skala 0–100 (`skor_TPT_2025`, `skor_Upah_2025`), lalu dijumlahkan berbobot. Default bobot 50/50 sesuai desain awal (Bagian 4 notebook), namun pengguna dashboard dapat mengubah bobot secara interaktif untuk eksplorasi skenario lain.

### 2. Clustering K-Means (referensi notebook, Bagian 6)
Segmentasi 38 kab/kota berdasarkan kombinasi TPT dan Upah 2025 (fitur distandarisasi dengan `StandardScaler`), jumlah klaster ditentukan dengan elbow method. Digunakan untuk memberi label naratif otomatis per wilayah (mis. "Urban-Industri: TPT & Upah tinggi").

### 3. Profil Volatilitas (Tren Terkini)
Dihitung dari data historis 2008–2025 (rentang data yang dinyatakan *reliable*, lihat catatan keterbatasan di bawah): rata-rata dan standar deviasi TPT/TPAK per wilayah, koefisien variasi, serta dampak spesifik Krisis 2008 dan COVID-19 (2020–2021) sebagai perubahan poin persentase dari kondisi sebelum krisis.

### 4. Skor Risiko / Early-Warning (Insight & Rekomendasi)
Menggunakan **skor risiko relatif berbasis percentile per tahun**, bukan ambang absolut. Skor tersusun dari:
- 50% laju perubahan TPT ternormalisasi,
- 40% level TPT relatif terhadap wilayah lain di tahun yang sama,
- bonus 10% konsistensi arah tren (naik berturut-turut).

Tier: **Rendah** (bottom 50%), **Sedang** (50–80 percentile), **Tinggi** (top 20%). Pendekatan ini divalidasi secara retrospektif terhadap kondisi 2020 (periode awal COVID-19) — metode relatif ini berhasil menandai 3 dari 5 wilayah dengan lonjakan pengangguran tertinggi saat itu sebagai tier "Tinggi", dibanding metode ambang absolut yang gagal menandai satupun.

---

## Instalasi & Menjalankan Secara Lokal

### Prasyarat
- Python 3.10+
- pip

### Langkah

```bash
# 1. Clone repository
git clone https://github.com/egafaiz/DashboardKetenagakerjaanProvJatim.git
cd DashboardKetenagakerjaanProvJatim

# 2. (Opsional tapi disarankan) buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependency
pip install -r requirements.txt

# 4. Jalankan dashboard
streamlit run app.py
```

Dashboard akan terbuka otomatis di `http://localhost:8501`.

### Dependency Utama

| Package | Kegunaan |
|---|---|
| `streamlit` | Framework dashboard (>=1.38, memakai `st.navigation` & `st.Page`) |
| `pandas` | Manipulasi data |
| `pyarrow` | Membaca file `.parquet` |
| `plotly` | Visualisasi interaktif (choropleth, line chart, bar chart) |

---

## Deployment

Repo ini menyertakan `Procfile` untuk deployment gaya Heroku/Railway:

```
web: streamlit run home.py --server.port $PORT --server.address 0.0.0.0
```
Tema dashboard dikunci ke mode terang lewat `.streamlit/config.toml` (`base = "light"`) agar tampilan tidak berubah mengikuti preferensi dark mode browser/OS pengguna, yang sebelumnya menyebabkan teks dan judul nyaris tidak terbaca di beberapa perangkat.

---

## Kamus Data

Tabel utama: `master_kabkota.parquet` (1 baris = 1 kabupaten/kota, 38 baris)

| Kolom | Deskripsi |
|---|---|
| `Kabupaten/Kota` | Nama wilayah administratif |
| `Bekerja 2023/2024/2025`, `Pengangguran 2023/2024/2025` | Jumlah penduduk bekerja/menganggur per tahun (Agustus) |
| `TPT 2023/2024/2025` | Tingkat Pengangguran Terbuka (%) |
| `Upah 2023/2024/2025` | Rata-rata upah (Rupiah) |
| `skor_TPT_2025`, `skor_Upah_2025` | Skor ternormalisasi 0–100 |
| `rank_TPT_2025`, `rank_Upah_2025` | Peringkat antarwilayah |
| `composite_index`, `rank_composite` | Skor gabungan default (bobot 50/50) dan peringkatnya |
| `selisih_TPT_vs_prov` | Selisih TPT wilayah terhadap rata-rata provinsi (poin) |
| `selisih_Upah_vs_ratarata` | Selisih upah wilayah terhadap rata-rata provinsi (Rupiah) |

Tabel pendukung lain:

| Berkas | Isi |
|---|---|
| `kabkota_long.parquet` | Versi *long format* dari data kab/kota untuk kebutuhan visualisasi time-series |
| `sektor_long.parquet` | Penyerapan tenaga kerja per 17 lapangan usaha, provinsi, 2023–2025 |
| `table4_karakteristik_tpt.parquet` | TPT menurut karakteristik demografis, Februari 2024–2026 |
| `table5_karakteristik_pekerja.parquet` | Komposisi status pekerjaan (formal/informal) & pendidikan pekerja |
| `tpt_tpak_gabungan_2008_2025.parquet` | TPT & TPAK historis gabungan per kab/kota, basis reliable 2008–2025 |
| `profil_volatilitas_kabkota.parquet` | Rata-rata, std, koefisien variasi TPT/TPAK, dan dampak krisis 2008 & COVID-19 per wilayah |
| `skor_risiko_kabkota_2025.parquet` | Skor risiko relatif dan tier (Rendah/Sedang/Tinggi) per kab/kota, tahun 2025 |

Referensi label kolom yang ditampilkan ke pengguna (istilah teknis → label ramah-pengguna) didefinisikan terpusat di `config.py` (`LABEL_KOLOM`, `FORMAT_KOLOM`) — mengubah cara suatu kolom ditampilkan cukup dilakukan di satu tempat ini.

---

## Keterbatasan & Catatan Metodologi

Transparansi soal keterbatasan data adalah bagian dari standar analisis proyek ini, bukan disembunyikan di balik visualisasi:

1. **Data historis 2001–2007 tidak digunakan untuk analisis tren/volatilitas.** Investigasi nilai ekstrem pada data historis BPS Web API menemukan 17 baris dengan TPT di luar rentang wajar (<0.5% atau >15%), 100% terkonsentrasi pada 2001–2007 dan mayoritas di kota-kota kecil (Kota Pasuruan, Madiun, Blitar, Batu, Kediri) — indikasi *sampling error* Sakernas pada periode tersebut. Rentang yang dipakai untuk analisis tren dan skor risiko dibatasi mulai **2008**.
2. **Gap data tahun 2016** pada beberapa indikator historis ditangani dengan interpolasi linear; baris hasil interpolasi ditandai eksplisit (`is_interpolasi_tpt`, `is_interpolasi_tpak`) agar dapat dibedakan dari data observasi asli.
3. **TPAK historis dari BPS Web API belum tervalidasi silang** dengan sumber Excel resmi (berbeda dengan TPT yang sudah divalidasi di Bagian 9 notebook) — perlu dicatat di halaman metodologi dashboard bila dipakai untuk kesimpulan kebijakan.
4. **Skor risiko early-warning bersifat deskriptif-relatif, bukan prediktif.** Skor ini membandingkan posisi suatu wilayah terhadap wilayah lain pada tahun yang sama (percentile-based), bukan model prediksi probabilitas ke depan. Validasi retrospektif terhadap 2020 menunjukkan performa yang jauh lebih baik dibanding pendekatan ambang absolut, namun kota kecil dengan volume sampel rendah (mis. Kota Batu) berisiko *under-detected* karena noise sampling — keterbatasan ini didokumentasikan, bukan disembunyikan.
5. **Composite Index bersifat subjektif terhadap pilihan bobot.** Bobot default 50/50 (TPT vs Upah) adalah keputusan desain, bukan hasil optimisasi statistik. Fitur slider di halaman "Peta & Kesenjangan" sengaja disediakan agar pengguna dapat mengeksplorasi sensitivitas ranking terhadap perubahan bobot ini.

---

## Rencana Pengembangan Lanjutan

- [ ] Fitur forecasting TPT/TPAK memanfaatkan data historis 2008–2025 yang kini tersedia (dieksplorasi di notebook, belum diintegrasikan ke dashboard).
- [ ] Validasi silang TPAK historis API dengan sumber Excel resmi BPS.
- [ ] Fitur *compare mode* antar dua kabupaten/kota (fungsi narasi otomatis sudah tersedia di notebook, `generate_narasi_perbandingan`, belum dipasang di UI).
- [ ] Otomatisasi pembaruan data (saat ini pipeline notebook dijalankan manual setiap ada rilis BPS baru).

---

## Kontak

**Muhammad Ega Faiz Fadlillah**
Mahasiswa Informatika, Universitas Muhammadiyah Malang · Peserta Magang, Diskominfo Provinsi Jawa Timur

Repository: [github.com/egafaiz/DashboardKetenagakerjaanProvJatim](https://github.com/egafaiz/DashboardKetenagakerjaanProvJatim)
