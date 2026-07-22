
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"
GEOJSON_DIR = BASE_DIR / "assets" / "geojson"

PATH_PRIMER = RAW_DIR / "Data_Primer_Bersih.xlsx"
PATH_PENDAMPING = RAW_DIR / "Data_Pendamping_Feb2026.xlsx"
PATH_GEOJSON = GEOJSON_DIR / "jatim_38_kabkota.geojson"

GEOJSON_FEATURE_ID_KEY = "properties.Kabupaten/Kota"

SUMBER_PRIMER = "BPS Jatim – Keadaan Angkatan Kerja Jatim, Agustus 2025 (rilis 17 Maret 2026)"
SUMBER_PENDAMPING = "BPS Jatim – BRS Jumlah Angkatan Kerja Jatim, Februari 2026 (rilis 5 Mei 2026)"
PATH_TPT_UMUR_PROVINSI = DATA_DIR / "tpt_umur_provinsi_agustus2025.parquet"
PATH_TPT_UMUR_KABKOTA = DATA_DIR / "tpt_umur_kabkota_agustus2025.parquet"
SUMBER_API_BPS = "BPS Web API (webapi.bps.go.id), domain Jawa Timur — TPT var_id 54, TPAK var_id 277"
SUMBER_DETAIL_AGUSTUS = "BPS Jatim – Keadaan Angkatan Kerja Provinsi Jawa Timur, Agustus 2025 (Tabel 17, 35, 116)"
TANGGAL_UPDATE_DASHBOARD = "Juli 2026"

COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_DARK = "#1D4ED8"
COLOR_INK = "#1F2937"
COLOR_SECONDARY = "#F59E0B"
COLOR_ACCENT = "#60A5FA"
COLOR_BG = "#FFFFFF"
COLOR_BG_PAGE = "#F8F9FA"
COLOR_CARD = "#FFFFFF"
COLOR_BORDER = "#E5E7EB"
COLOR_MUTED = "#6B7280"
COLOR_DANGER = "#DC2626"
COLOR_WARNING = "#D97706"
COLOR_SUCCESS = "#16A34A"

TIPE_WILAYAH_WARNA = {"Kabupaten": "#2563EB", "Kota": "#F59E0B"}

CHOROPLETH_SCALE = "YlOrRd"

TIER_RISIKO_WARNA = {"Rendah": "#16A34A", "Sedang": "#D97706", "Tinggi": "#DC2626"}

BADGE_KABKOTA_BG, BADGE_KABKOTA_BORDER, BADGE_KABKOTA_TEXT = "#EFF6FF", "#BFDBFE", "#1D4ED8"
BADGE_PROVINSI_BG, BADGE_PROVINSI_BORDER, BADGE_PROVINSI_TEXT = "#FFFBEB", "#FDE68A", "#B45309"

PLOTLY_TEMPLATE = "plotly_white"

FONT_DISPLAY = "'Inter', 'Plus Jakarta Sans', -apple-system, sans-serif"
FONT_BODY = "'Inter', 'Plus Jakarta Sans', -apple-system, sans-serif"

SEKTOR_WARNA = [
    "#2563EB", "#60A5FA", "#93C5FD", "#BFDBFE", "#F59E0B",
    "#FBBF24", "#FDE68A", "#9CA3AF", "#D1D5DB", "#6B7280",
    "#14B8A6", "#5EEAD4", "#8B5CF6", "#C4B5FD", "#EF4444",
    "#FCA5A5", "#22C55E",
]

LABEL_KOLOM = {
    "Kabupaten/Kota": "Kabupaten/Kota", "kabkota": "Kabupaten/Kota",
    "tipe_wilayah": "Tipe Wilayah",
    "TPT": "TPT (%)", "TPT 2023": "TPT 2023 (%)", "TPT 2024": "TPT 2024 (%)", "TPT 2025": "TPT 2025 (%)", "TPT_2025": "TPT 2025 (%)",
    "TPAK": "TPAK (%)",
    "Upah": "Rata-rata Upah", "Upah 2023": "Upah 2023", "Upah 2024": "Upah 2024", "Upah 2025": "Upah 2025",
    "Bekerja": "Penduduk Bekerja", "Pengangguran": "Pengangguran",
    "composite_index": "Composite Index", "rank_composite": "Peringkat Composite",
    "composite_index_custom": "Composite Index", "rank_composite_custom": "Peringkat",
    "skor_TPT_2025": "Skor TPT (0-100)", "skor_Upah_2025": "Skor Upah (0-100)",
    "rank_TPT_2025": "Peringkat TPT", "rank_Upah_2025": "Peringkat Upah",
    "cluster": "Klaster", "tahun": "Tahun", "periode": "Periode", "sumber": "Sumber Data",
    "Lapangan Pekerjaan Utama": "Lapangan Pekerjaan Utama",
    "TPT_rata2": "Rata-rata TPT Historis (%)", "TPT_std": "Volatilitas TPT (std)",
    "TPAK_rata2": "Rata-rata TPAK Historis (%)", "TPAK_std": "Volatilitas TPAK (std)",
    "cv_TPT": "Koef. Variasi TPT (%)", "cv_TPAK": "Koef. Variasi TPAK (%)",
    "delta_TPT_krisis2008": "Δ TPT Krisis 2008 (poin)", "delta_TPT_covid": "Δ TPT COVID-19 (poin)",
    "skor_risiko": "Skor Risiko (0-100)", "tier_risiko": "Tier Risiko",
    "kenaikan_3th": "Perubahan 3 Tahun Terakhir (poin)",
    "naik_terus_3th": "Naik Berturut 3 Tahun",
    "is_interpolasi": "Nilai Interpolasi (2016)",
    "Golongan_Umur": "Kelompok Usia",
    "Angkatan_Kerja": "Angkatan Kerja", "Bekerja": "Penduduk Bekerja", "Pengangguran": "Pengangguran",
    "is_interpolasi_tpt": "TPT Interpolasi (2016)", "is_interpolasi_tpak": "TPAK Interpolasi (2016)",
    "Bekerja 2023": "Bekerja 2023", "Bekerja 2024": "Bekerja 2024", "Bekerja 2025": "Bekerja 2025",
    "Pengangguran 2023": "Pengangguran 2023", "Pengangguran 2024": "Pengangguran 2024", "Pengangguran 2025": "Pengangguran 2025",
    "selisih_TPT_vs_prov": "Selisih TPT vs Provinsi (poin)", "selisih_Upah_vs_ratarata": "Selisih Upah vs Rata-rata",
    "Karakteristik": "Karakteristik", "kategori": "Kategori",
    "Feb 2024": "Feb 2024 (%)", "Feb 2025": "Feb 2025 (%)", "Feb 2026": "Feb 2026 (%)",
    "Perubahan (persen poin)": "Perubahan (poin)",
    "Jumlah 2024 (juta)": "Jumlah 2024 (juta)", "Jumlah 2025 (juta)": "Jumlah 2025 (juta)", "Jumlah 2026 (juta)": "Jumlah 2026 (juta)",
    "Persentase 2024 (%)": "Persentase 2024 (%)", "Persentase 2025 (%)": "Persentase 2025 (%)", "Persentase 2026 (%)": "Persentase 2026 (%)",
}

KOLOM_TERSEMBUNYI = {"urutan", "kode_wilayah", "kode_wilayah_x", "kode_wilayah_y", "kategori"}

FORMAT_KOLOM = {
    "TPT": "persen", "TPT 2023": "persen", "TPT 2024": "persen", "TPT 2025": "persen", "TPT_2025": "persen",
    "TPAK": "persen", "TPT_rata2": "persen", "TPT_std": "persen",
    "TPAK_rata2": "persen", "TPAK_std": "persen", "cv_TPT": "persen", "cv_TPAK": "persen",
    "skor_TPT_2025": "angka", "skor_Upah_2025": "angka", "composite_index": "angka", "composite_index_custom": "angka",
    "skor_risiko": "angka", "kenaikan_3th": "angka",
    "delta_TPT_krisis2008": "angka", "delta_TPT_covid": "angka",
    "Upah": "rupiah", "Upah 2023": "rupiah", "Upah 2024": "rupiah", "Upah 2025": "rupiah",
    "Bekerja": "angka", "Pengangguran": "angka",
    "Bekerja 2023": "angka", "Bekerja 2024": "angka", "Bekerja 2025": "angka",
    "Pengangguran 2023": "angka", "Pengangguran 2024": "angka", "Pengangguran 2025": "angka",
    "Angkatan_Kerja": "angka", "Bekerja": "angka", "Pengangguran": "angka",
    "selisih_TPT_vs_prov": "angka", "selisih_Upah_vs_ratarata": "rupiah",
    "Feb 2024": "persen", "Feb 2025": "persen", "Feb 2026": "persen", "Perubahan (persen poin)": "angka",
    "Jumlah 2024 (juta)": "angka", "Jumlah 2025 (juta)": "angka", "Jumlah 2026 (juta)": "angka",
    "Persentase 2024 (%)": "persen", "Persentase 2025 (%)": "persen", "Persentase 2026 (%)": "persen",
    "rank_TPT_2025": "angka", "rank_Upah_2025": "angka", "rank_composite": "angka", "rank_composite_custom": "angka", "cluster": "angka",
    "tahun": "teks",
}

def plotly_config(nama_file: str) -> dict:
    return {
        "displaylogo": False,
        "displayModeBar": True,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d",
            "autoScale2d", "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian",
            "toggleSpikelines", "hoverClosestGeo", "toggleHover",
        ],
        "toImageButtonOptions": {"format": "png", "filename": nama_file, "scale": 2},
    }