import plotly.express as px
import streamlit as st

import config
import utils

data = st.session_state["data"]
ringkasan_feb = data["ringkasan_feb"]
table4 = data["table4"]
master = data["master_kabkota"]
geojson = data["geojson"]

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Satu Data Jatim · Smart Province · Diskominfo Provinsi Jawa Timur",
    "Ketenagakerjaan Jawa Timur, dari Angka ke Wilayah",
    "TPT & penyerapan tenaga kerja per Kabupaten/Kota — bukan cuma angka provinsi.",
)

# ── Kartu ringkasan: Februari 2026 vs Februari 2025 ───────────────
tpt_row = table4[table4["kategori"].isna()].iloc[0]
tpt_26, tpt_25 = tpt_row["Feb 2026"], tpt_row["Feb 2025"]

tpak_26, tpak_25 = ringkasan_feb.loc["Tingkat Partisipasi Angkatan Kerja (TPAK)", "Feb 2026"], \
    ringkasan_feb.loc["Tingkat Partisipasi Angkatan Kerja (TPAK)", "Feb 2025"]
angkatan_26, angkatan_25 = ringkasan_feb.loc["Angkatan Kerja", "Feb 2026"], ringkasan_feb.loc["Angkatan Kerja", "Feb 2025"]
bekerja_26, bekerja_25 = ringkasan_feb.loc["– Bekerja", "Feb 2026"], ringkasan_feb.loc["– Bekerja", "Feb 2025"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("TPT Februari 2026", f"{tpt_26:.2f}%", f"{tpt_26 - tpt_25:+.2f} poin vs Feb 2025", delta_color="inverse",
            help="Tingkat Pengangguran Terbuka — persentase angkatan kerja yang tidak bekerja.")
col2.metric("TPAK Februari 2026", f"{tpak_26:.2f}%", f"{tpak_26 - tpak_25:+.2f} poin vs Feb 2025",
            help="Tingkat Partisipasi Angkatan Kerja — persentase penduduk usia kerja yang aktif secara ekonomi.")
col3.metric("Angkatan Kerja", f"{angkatan_26:.2f} juta", f"{(angkatan_26 - angkatan_25) / angkatan_25 * 100:+.2f}% vs Feb 2025",
            help="Penduduk usia kerja yang bekerja atau sedang mencari kerja.")
col4.metric("Penduduk Bekerja", f"{bekerja_26:.2f} juta", f"{(bekerja_26 - bekerja_25) / bekerja_25 * 100:+.2f}% vs Feb 2025",
            help="Bagian dari angkatan kerja yang sedang bekerja.")

st.caption(f"Sumber: {config.SUMBER_PENDAMPING}")
st.markdown("")

# ── Peta sebaran singkat ───────────────────────────────────────
with st.container(border=True):
    col_map, col_side = st.columns([3, 2])
    with col_map:
        utils.section_label("Sebaran Wilayah", "Peta TPT per Kabupaten/Kota — 2025")
        fig_map = px.choropleth(
            master, geojson=geojson, locations="Kabupaten/Kota",
            featureidkey=config.GEOJSON_FEATURE_ID_KEY, color="TPT 2025",
            color_continuous_scale=config.CHOROPLETH_SCALE,
            hover_name="Kabupaten/Kota", hover_data={"TPT 2025": ":.2f"},
            labels={"TPT 2025": "TPT (%)"},
        )
        fig_map.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.6)
        fig_map.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig_map.update_layout(
            height=340, margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="TPT (%)", thickness=12),
            font_family=config.FONT_BODY, font_color=config.COLOR_INK,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_map, width="stretch", config=config.plotly_config("peta_tpt_beranda"))
    with col_side:
        utils.section_label("Sorotan", "Kesenjangan Antar Wilayah")
        tertinggi = master.loc[master["TPT 2025"].idxmax()]
        terendah = master.loc[master["TPT 2025"].idxmin()]
        st.markdown(
            f"**TPT tertinggi:** {tertinggi['Kabupaten/Kota']} ({tertinggi['TPT 2025']:.2f}%)  \n"
            f"**TPT terendah:** {terendah['Kabupaten/Kota']} ({terendah['TPT 2025']:.2f}%)  \n"
            f"**Selisih:** {tertinggi['TPT 2025'] - terendah['TPT 2025']:.2f} poin persen"
        )
        st.page_link("views/peta_kesenjangan.py", label="Lihat peta lengkap & Compare Mode", icon=":material/arrow_forward:")

st.markdown("")

# ── Navigasi ────────────────────────────────────────────────────
utils.section_label("Navigasi", "Jelajahi Dashboard")
nav_cols = st.columns(3)
halaman = [
    ("01", "views/potret_provinsi.py", "Potret Provinsi", "Indikator makro & tren historis 2008-2025", ":material/insights:"),
    ("02", "views/peta_kesenjangan.py", "Peta & Kesenjangan", "Sebaran TPT/Upah, Composite Index, Compare Mode", ":material/map:"),
    ("03", "views/sektor_ekonomi.py", "Sektor Ekonomi", "Komposisi 17 lapangan usaha (level provinsi)", ":material/factory:"),
    ("04", "views/karakteristik_pekerja.py", "Karakteristik Pekerja", "Gender, pendidikan, formal/informal", ":material/groups:"),
    ("05", "views/tren_terkini.py", "Tren Terkini", "Historis TPT+TPAK, volatilitas & dampak krisis", ":material/trending_up:"),
    ("06", "views/insight_rekomendasi.py", "Insight & Rekomendasi", "Skor risiko early-warning & metodologi", ":material/lightbulb:"),
]
for i, (no, path, judul, desk, icon) in enumerate(halaman):
    with nav_cols[i % 3]:
        with st.container(border=True):
            st.markdown(
                f'<div class="nav-card"><span class="nav-card-no">{no}</span>'
                f'<span class="nav-card-title">{judul}</span></div>',
                unsafe_allow_html=True,
            )
            st.caption(desk)
