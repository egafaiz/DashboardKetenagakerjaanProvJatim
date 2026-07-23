import streamlit as st

import config
import utils
from data_loader import load_all

st.set_page_config(page_title="Ketenagakerjaan Jatim", layout="wide", initial_sidebar_state="expanded")
utils.apply_style()

if "data" not in st.session_state:
    with st.spinner("Memuat seluruh data dashboard..."):
        st.session_state["data"] = load_all()

with st.sidebar:
    st.markdown(
        f"""
        <details class="sidebar-header-details">
            <summary class="sidebar-header-summary">Ketenagakerjaan Jawa Timur</summary>
            <div class="sidebar-header-body">
                <p>Disusun dari data BPS Jatim (Agustus 2025 & Februari 2026), diperkaya
                data historis BPS Web API (2008-2025) untuk analisis volatilitas dan
                skor risiko per kab/kota.</p>
                <p>Data diperbarui: {config.TANGGAL_UPDATE_DASHBOARD}</p>
                <p><strong>Primer:</strong> {config.SUMBER_PRIMER}</p>
                <p><strong>Pendamping:</strong> {config.SUMBER_PENDAMPING}</p>
                <p><strong>API Historis:</strong> {config.SUMBER_API_BPS}</p>
            </div>
        </details>
        """,
        unsafe_allow_html=True,
    )

halaman = [
    st.Page("views/beranda.py", title="Beranda", icon=":material/space_dashboard:", default=True),
    st.Page("views/potret_provinsi.py", title="Potret Provinsi", icon=":material/insights:"),
    st.Page("views/peta_kesenjangan.py", title="Peta & Kesenjangan", icon=":material/map:"),
    st.Page("views/sektor_ekonomi.py", title="Sektor Ekonomi", icon=":material/factory:"),
    st.Page("views/karakteristik_pekerja.py", title="Karakteristik Pekerja", icon=":material/groups:"),
    st.Page("views/tren_terkini.py", title="Tren Terkini", icon=":material/trending_up:"),
    st.Page("views/proyeksi.py", title="Proyeksi TPT & TPAK", icon=":material/query_stats:"),
    st.Page("views/insight_rekomendasi.py", title="Insight & Rekomendasi", icon=":material/lightbulb:"),
]

nav = st.navigation(halaman, position="sidebar")
nav.run()
