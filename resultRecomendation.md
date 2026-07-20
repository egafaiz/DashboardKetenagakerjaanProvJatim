# Rasional Proyek, Temuan Kunci, dan Rekomendasi
## Dashboard Ketenagakerjaan Provinsi Jawa Timur — Project 1, Magang Diskominfo Provinsi Jawa Timur

**Disusun oleh:** Muhammad Ega Faiz Fadlillah
**Periode:** 13 Juli – 14 Agustus 2026
**Mentor:** Bapak Agus
**Sumber data:** BPS Provinsi Jawa Timur (Agustus 2023–2025, Februari 2024–2026), BPS Web API (2001–2025)

---

## Daftar Isi

1. [Mengapa Topik Ini Dipilih](#1-mengapa-topik-ini-dipilih)
2. [Pertanyaan Analitik yang Dijawab](#2-pertanyaan-analitik-yang-dijawab)
3. [Ringkasan Eksekutif](#3-ringkasan-eksekutif)
4. [Temuan Kunci](#4-temuan-kunci)
5. [Rekomendasi](#5-rekomendasi)
6. [Keterbatasan Analisis](#6-keterbatasan-analisis)
7. [Tindak Lanjut yang Diusulkan](#7-tindak-lanjut-yang-diusulkan)

---

## 1. Mengapa Topik Ini Dipilih

Data ketenagakerjaan yang dipublikasikan BPS Jawa Timur selama ini pada praktiknya paling banyak dikonsumsi dalam bentuk **angka tunggal level provinsi** — TPT Jawa Timur sekian persen, TPAK sekian persen. Angka itu benar, tetapi menyembunyikan sesuatu yang jauh lebih relevan untuk perumusan kebijakan: **provinsi ini terdiri dari 38 kabupaten/kota dengan kondisi pasar kerja yang sangat berbeda satu sama lain**, dan rata-rata provinsi bisa terlihat stabil justru saat kesenjangan di baliknya melebar.

Tiga pertimbangan yang mendasari pemilihan topik ini sebagai Project 1:

1. **Kesenjangan tersembunyi di balik rata-rata.** Selisih upah antara kabupaten/kota dengan upah tertinggi (Kota Surabaya, ± Rp 3,96 juta) dan terendah (Kabupaten Pamekasan, ± Rp 2,02 juta) hampir mencapai **2x lipat** — sebuah kesenjangan yang sama sekali tidak terlihat kalau hanya melaporkan rata-rata provinsi.
2. **Kebutuhan Diskominfo akan aset "Satu Data" yang granular dan reusable.** Diskominfo Jatim mengelola *Satu Data Jatim — Smart Province*, yang idealnya berisi data siap pakai di level wilayah, bukan hanya ringkasan naratif. Dashboard ini dirancang sebagai aset data (parquet terstruktur + antarmuka) yang bisa dipakai ulang oleh OPD lain, bukan laporan sekali pakai.
3. **Data sudah tersedia, tetapi belum diolah jadi keputusan.** BPS Jatim merilis data primer dan pendamping secara rutin, dan BPS Web API menyediakan riwayat panjang sejak 2001. Yang belum ada adalah lapisan analitik yang menyatukan keduanya menjadi indikator siap pakai: ranking, indeks komposit, profil volatilitas, dan skor risiko dini.

Dengan kata lain, topik ini dipilih bukan karena datanya sulit didapat, melainkan karena **nilai analitiknya belum diekstraksi**. Ini pekerjaan seorang data analyst: mengubah rilis statistik resmi menjadi alat bantu keputusan yang bisa dipakai berulang.

---

## 2. Pertanyaan Analitik yang Dijawab

Seluruh pipeline (notebook EDA) dan dashboard dirancang untuk menjawab lima pertanyaan yang secara langsung relevan bagi pembuat kebijakan di level provinsi:

| # | Pertanyaan | Dijawab di |
|---|---|---|
| 1 | Kabupaten/kota mana yang kondisi ketenagakerjaannya paling tertinggal, dan mana yang paling unggul? | Peta & Kesenjangan, Composite Index |
| 2 | Wilayah mana yang polanya paling tidak stabil dari waktu ke waktu — rentan berubah drastis? | Tren Terkini, Profil Volatilitas |
| 3 | Wilayah mana yang perlu diprioritaskan lebih dulu untuk intervensi, berdasarkan tren terkini, bukan hanya kondisi hari ini? | Insight & Rekomendasi, Skor Risiko |
| 4 | Kelompok pekerja mana (gender, pendidikan, status formal/informal) yang paling terdampak pengangguran? | Karakteristik Pekerja |
| 5 | Sektor ekonomi mana yang menyerap tenaga kerja terbanyak, dan apakah strukturnya bergeser dari waktu ke waktu? | Sektor Ekonomi |

---

## 3. Ringkasan Eksekutif

- TPT Provinsi Jawa Timur **membaik** dari 4,66% (Agustus 2023) menjadi 3,78% (Agustus 2025), dan konsisten dengan tren itu, TPT Februari juga turun dari 3,74% (2024) menjadi 3,55% (2026).
- Namun perbaikan level provinsi ini **tidak merata**: rentang TPT antarwilayah pada 2025 terbentang dari 1,33% (Kabupaten Pamekasan) hingga 5,75% (Kabupaten Sidoarjo) — rasio hampir **4,3x** antara wilayah terbaik dan terburuk.
- Metode skor risiko relatif (percentile-based) mengidentifikasi **7 dari 38 wilayah** berada di tier risiko "Tinggi" untuk 2025, didominasi oleh kota-kota (bukan kabupaten) dengan basis ekonomi non-agraris.
- Sektor **Pertanian, Kehutanan dan Perikanan** tetap menjadi penyerap tenaga kerja terbesar di Jawa Timur (32,1%), diikuti Perdagangan (18,5%) dan Industri Pengolahan (14,9%) — struktur ini penting karena berimplikasi langsung pada jenis intervensi yang relevan per wilayah.
- Dampak COVID-19 terhadap TPT **paling terasa di wilayah dengan basis ekonomi urban/perdagangan-jasa**, bukan di wilayah agraris — pola yang berlawanan dengan asumsi umum bahwa daerah pertanian lebih rentan krisis ekonomi.

---

## 4. Temuan Kunci

### Temuan 1 — Perbaikan provinsi menutupi kesenjangan wilayah yang tetap lebar

TPT provinsi turun cukup konsisten selama tiga tahun terakhir, tetapi penurunan ini tidak dialami merata oleh semua wilayah. Pada 2025:

| | TPT (%) | Upah (Rp) |
|---|---|---|
| **5 wilayah TPT tertinggi** | Kab. Sidoarjo (5,75), Kota Malang (5,69), Kab. Gresik (5,47), Kab. Bangkalan (5,31), Kab. Malang (5,00) | — |
| **5 wilayah TPT terendah** | Kab. Pamekasan (1,33), Kab. Pacitan (1,40), Kab. Sumenep (1,64), Kab. Ngawi (2,26), Kab. Sampang (2,44) | — |
| **5 wilayah upah tertinggi** | — | Kota Surabaya (3,96 jt), Kab. Sidoarjo (3,95 jt), Kab. Gresik (3,55 jt), Kab. Bangkalan (3,53 jt), Kota Mojokerto (3,30 jt) |
| **5 wilayah upah terendah** | — | Kab. Pamekasan (2,02 jt), Kab. Lumajang (2,04 jt), Kab. Situbondo (2,12 jt), Kab. Ponorogo (2,20 jt), Kab. Tulungagung (2,20 jt) |

**Implikasi:** kawasan aglomerasi industri Surabaya Raya (Sidoarjo, Gresik) justru menunjukkan pola **upah tinggi tetapi TPT juga tinggi** — konsisten dengan karakteristik pasar kerja urban-industri yang punya angkatan kerja besar dan turnover tinggi, bukan wilayah yang "gagal". Sebaliknya, sejumlah kabupaten dengan TPT sangat rendah (Pamekasan, Pacitan, Sumenep) justru berada di kelompok upah terendah — pola yang lebih mengindikasikan **underemployment / dominasi sektor informal-agraris** ketimbang pasar kerja yang benar-benar sehat. TPT rendah tanpa diimbangi data upah bisa menyesatkan bila dibaca sendirian, dan ini adalah alasan utama dashboard menyandingkan kedua indikator dalam satu Composite Index, bukan menampilkan TPT saja.

### Temuan 2 — Tujuh wilayah masuk tier risiko "Tinggi", didominasi kota

Skor risiko relatif (kombinasi laju perubahan TPT, level TPT relatif, dan konsistensi tren naik) mengklasifikasikan 38 wilayah menjadi: **19 Rendah, 12 Sedang, 7 Tinggi**.

Tujuh wilayah dengan skor risiko tertinggi 2025: **Kota Probolinggo, Kota Mojokerto, Kota Malang, Kabupaten Bangkalan, Kabupaten Blitar, Kota Kediri, Kota Madiun.**

**Implikasi:** lima dari tujuh wilayah tier "Tinggi" berstatus **kota**, bukan kabupaten — pola yang konsisten dengan temuan volatilitas (lihat Temuan 3) bahwa pasar kerja perkotaan skala menengah di Jawa Timur cenderung lebih fluktuatif dibanding kabupaten agraris. Ini bertentangan dengan persepsi umum bahwa kota besar identik dengan pasar kerja yang lebih stabil.

### Temuan 3 — Volatilitas historis tertinggi juga terkonsentrasi di kota menengah

Analisis volatilitas TPT 2008–2025 (standar deviasi dan koefisien variasi) menunjukkan wilayah paling fluktuatif adalah **Kota Madiun** (rata-rata TPT 6,87%, std 2,72), **Kota Mojokerto** (rata-rata 5,93%, std 2,67), **Kabupaten Sidoarjo** (rata-rata 7,20%, std 2,58), dan **Kota Kediri** (rata-rata 6,47%, std 2,29).

**Implikasi:** wilayah-wilayah ini bukan sekadar memiliki TPT yang tinggi, tetapi **secara struktural tidak stabil** — kondisinya bisa berubah signifikan dari satu periode ke periode lain. Bagi perencana kebijakan, ini penting dibedakan dari wilayah dengan TPT tinggi tapi stabil, karena strategi intervensinya berbeda (mitigasi guncangan vs. perbaikan struktural jangka panjang).

### Temuan 4 — Dampak COVID-19 justru paling besar di wilayah non-agraris

Kenaikan TPT akibat COVID-19 (2020–2021) terbesar tercatat di: **Kabupaten Sidoarjo (+6,30 poin)**, **Kota Madiun (+4,35 poin)**, **Kota Mojokerto (+4,27 poin)**, **Kota Surabaya (+3,85 poin)**, **Kota Batu (+3,50 poin)**.

Sebagai pembanding, dampak Krisis 2008 jauh lebih ringan dan lebih terkonsentrasi: **Kota Mojokerto (+3,42 poin)** menjadi satu-satunya wilayah dengan dampak signifikan, disusul Kota Probolinggo (+1,68 poin) — wilayah lain relatif tidak terdampak berarti.

**Implikasi:** kedua krisis mengonfirmasi pola yang sama — **wilayah dengan basis ekonomi industri, perdagangan, dan pariwisata (Sidoarjo, kota-kota) jauh lebih rentan terhadap guncangan eksternal** dibanding wilayah dengan basis agraris. Kabupaten Batu yang bergantung pada pariwisata juga masuk daftar terdampak COVID-19 terbesar, sesuai ekspektasi karena sektor pariwisata terhenti total di masa pandemi.

### Temuan 5 — Struktur sektor ekonomi masih didominasi pertanian, tapi upah tertinggi ada di luar sektor itu

Distribusi tenaga kerja Jawa Timur menurut lapangan usaha (data terbaru): **Pertanian/Kehutanan/Perikanan 32,1%**, **Perdagangan Besar & Eceran 18,5%**, **Industri Pengolahan 14,9%**, **Penyediaan Akomodasi & Makan Minum 8,2%**, **Konstruksi 6,4%**.

**Implikasi:** sepertiga tenaga kerja Jawa Timur masih bergantung pada sektor pertanian — sektor dengan produktivitas dan upah per kapita yang secara umum lebih rendah dibanding industri dan jasa. Ini selaras dengan Temuan 1: kabupaten-kabupaten dengan TPT rendah tapi upah rendah kemungkinan besar adalah kabupaten dengan basis pertanian yang dominan, di mana rendahnya TPT mencerminkan tingginya penyerapan informal, bukan kualitas pekerjaan yang tinggi.

### Temuan 6 — Pengangguran bergeser ke kelompok berpendidikan lebih tinggi

Menurut karakteristik pendidikan (Februari 2024 → Februari 2026):

| Kelompok Pendidikan | Feb 2024 | Feb 2026 | Perubahan |
|---|---|---|---|
| SD ke Bawah | 2,38% | 1,32% | **−0,66 poin** |
| SMK | 6,42% | 5,73% | −0,69 poin |
| Diploma I/II/III | 3,09% | 1,91% | −1,18 poin |
| SMA | 4,64% | **5,75%** | **+1,59 poin** |
| Universitas | 4,07% | **6,04%** | **+0,44 poin, TPT tertinggi dari semua kelompok pendidikan** |

**Implikasi:** ini temuan yang berlawanan dengan intuisi dan patut mendapat perhatian khusus — **TPT justru tertinggi di kelompok lulusan universitas (6,04%)**, bukan di kelompok berpendidikan rendah. Pola ini konsisten dengan fenomena *skills mismatch* yang umum terjadi di banyak daerah: lulusan pendidikan tinggi memilih menganggur lebih lama untuk mencari pekerjaan yang sesuai kualifikasi/ekspektasi gaji, sementara lulusan pendidikan dasar lebih cepat terserap ke sektor informal atau pertanian meski dengan kualitas pekerjaan yang lebih rendah. Selain itu, secara gender, TPT laki-laki turun (4,19%→3,78%) sementara TPT perempuan justru naik (3,12%→3,24%) pada periode yang sama — sinyal awal yang perlu dipantau lebih lanjut.

---

## 5. Rekomendasi

Rekomendasi berikut disusun dengan prinsip: **selaras langsung dengan temuan di atas**, dan dibedakan antara tindakan segera (dapat dijalankan dengan data yang sudah ada) dan tindakan yang butuh data/kajian tambahan.

### Prioritas Tinggi — Dapat ditindaklanjuti dengan data saat ini

1. **Jadikan 7 wilayah tier risiko "Tinggi" (Kota Probolinggo, Kota Mojokerto, Kota Malang, Kab. Bangkalan, Kab. Blitar, Kota Kediri, Kota Madiun) sebagai prioritas program penempatan kerja & pelatihan vokasi periode berikutnya.** Skor risiko ini sudah mempertimbangkan tren tiga tahun terakhir, bukan snapshot satu tahun, sehingga lebih layak dipakai sebagai dasar penentuan prioritas wilayah dibanding hanya melihat TPT tahun berjalan.
2. **Rancang program intervensi berbeda untuk "kota berisiko" vs "kabupaten berisiko".** Karena tier risiko tinggi didominasi kota dengan basis ekonomi industri/jasa yang lebih rentan guncangan eksternal, program mitigasi yang relevan cenderung ke arah stabilisasi sektor formal dan jaring pengaman sosial saat guncangan ekonomi — berbeda dengan kabupaten agraris yang kebutuhannya lebih ke peningkatan produktivitas dan nilai tambah hasil pertanian.
3. **Selidiki lebih lanjut skills mismatch lulusan universitas.** TPT tertinggi ada di kelompok lulusan universitas — ini layak menjadi bahasan lintas OPD (Disnaker, Dinas Pendidikan) untuk mengkaji kesesuaian kurikulum vokasi/perguruan tinggi dengan kebutuhan pasar kerja riil di Jawa Timur, bukan hanya memperbanyak lulusan.
4. **Pantau tren TPT perempuan yang mulai naik**, meski secara agregat masih di bawah TPT laki-laki. Tren berlawanan arah ini (laki-laki turun, perempuan naik) perlu dipantau tiap rilis, karena kalau berlanjut bisa menjadi kesenjangan gender yang melebar.

### Prioritas Menengah — Butuh kajian atau data tambahan

5. **Bangun program penguatan nilai tambah sektor pertanian di kabupaten dengan TPT rendah tapi upah rendah** (mis. Pamekasan, Pacitan, Sumenep, Lumajang). TPT yang rendah di wilayah ini kemungkinan besar mencerminkan penyerapan informal/agraris yang tinggi, bukan pasar kerja yang benar-benar sehat — indikasi ini perlu dikonfirmasi lebih lanjut dengan data status pekerjaan (formal/informal) per wilayah, yang saat ini baru tersedia di level provinsi, bukan kab/kota.
6. **Evaluasi sensitivitas Composite Index untuk kebutuhan alokasi anggaran.** Dashboard menyediakan slider bobot TPT vs Upah agar pengambil kebijakan bisa melihat bagaimana ranking wilayah berubah tergantung prioritas kebijakan (mengejar penyerapan tenaga kerja vs. mengejar kualitas upah) — hasil eksplorasi ini sebaiknya didiskusikan langsung dengan tim perencanaan sebelum dipakai sebagai dasar alokasi program.

### Prioritas Rendah — Pengembangan jangka panjang

7. **Bangun kapasitas forecasting TPT/TPAK** memanfaatkan data historis 2008–2025 yang sudah tersedia di pipeline, agar dashboard bisa memberi proyeksi ke depan (what-if), bukan hanya potret kondisi terkini dan historis.
8. **Validasi silang TPAK historis dari BPS Web API** dengan sumber Excel resmi BPS Jatim, agar seluruh indikator historis punya tingkat kepercayaan yang setara sebelum dipakai untuk kesimpulan kebijakan jangka panjang.

---

## 6. Keterbatasan Analisis

Ditulis eksplisit agar temuan dan rekomendasi di atas dibaca dengan konteks yang tepat, bukan sebagai kesimpulan mutlak:

- **Skor risiko bersifat relatif-deskriptif, bukan model prediktif.** Skor ini membandingkan posisi wilayah terhadap wilayah lain di tahun yang sama, bukan memprediksi probabilitas kondisi masa depan. Validasi retrospektif terhadap 2020 menunjukkan metode ini menandai 3 dari 5 wilayah top-COVID sebagai tier "Tinggi" — performa yang jauh lebih baik dari pendekatan ambang absolut (0 dari 5), tetapi tetap bukan model prediksi formal.
- **Data historis sebelum 2008 tidak digunakan** untuk analisis tren/volatilitas karena investigasi data menemukan indikasi *sampling error* Sakernas terkonsentrasi pada 2001–2007, terutama di kota-kota kecil.
- **TPT rendah tidak selalu berarti pasar kerja yang sehat.** Sebagaimana ditunjukkan di Temuan 1 dan 5, TPT rendah di sejumlah kabupaten kemungkinan mencerminkan tingginya penyerapan sektor informal/agraris, bukan kualitas lapangan kerja yang baik. Dashboard ini belum memiliki indikator kualitas pekerjaan (mis. rasio kerja formal vs informal per kabupaten/kota) untuk mengonfirmasi hipotesis ini secara langsung — data status pekerjaan yang tersedia saat ini masih di level provinsi.
- **Data karakteristik pekerja (gender, pendidikan, formal/informal) hanya tersedia di level provinsi**, sehingga temuan terkait skills mismatch dan tren gender di Temuan 6 belum bisa dipecah per kabupaten/kota dengan data yang ada saat ini.
- **Kota kecil berisiko under-detected** dalam skor risiko maupun profil volatilitas karena ukuran sampel Sakernas yang lebih kecil menghasilkan noise yang lebih tinggi (dicontohkan oleh kasus Kota Batu pada validasi retrospektif 2020).

---

## 7. Tindak Lanjut yang Diusulkan

| Langkah | Pemilik yang Disarankan | Urgensi |
|---|---|---|
| Presentasikan 7 wilayah tier risiko "Tinggi" ke tim perencanaan program Disnaker Jatim | Diskominfo + Disnaker | Tinggi |
| Diskusikan temuan skills mismatch lulusan universitas lintas OPD | Diskominfo + Disnaker + Dinas Pendidikan | Tinggi |
| Perbaikan `Procfile` dan proses deployment dashboard ke lingkungan produksi | Tim IT Diskominfo | Tinggi (teknis) |
| Kajian lanjutan status formal/informal per kabupaten/kota | Disnaker (sumber data tambahan) | Menengah |
| Pengembangan fitur forecasting di dashboard | Tim data analyst / lanjutan magang | Menengah |
| Validasi silang TPAK historis API vs Excel resmi | Tim data analyst | Menengah |

---

*Dokumen ini merupakan bagian dari Project 1 magang Diskominfo Provinsi Jawa Timur dan disusun berdampingan dengan `README.md` (dokumentasi teknis dashboard) dan `EDA_KetenagarakerjaanJATIM.ipynb` (pipeline analitik lengkap). Seluruh angka dalam dokumen ini diambil langsung dari data hasil pipeline (`data/processed/`) per Juli 2026.*
