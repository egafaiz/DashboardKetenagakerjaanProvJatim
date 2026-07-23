
import json

import pandas as pd
import streamlit as st

import config

@st.cache_data(show_spinner=False)
def load_geojson() -> dict:
    with open(config.PATH_GEOJSON, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_ringkasan_prov() -> pd.DataFrame:
    return pd.read_excel(config.PATH_PRIMER, sheet_name="Ringkasan_Prov")

@st.cache_data(show_spinner=False)
def load_master_kabkota() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "master_kabkota.parquet")

@st.cache_data(show_spinner=False)
def load_kabkota_long() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "kabkota_long.parquet")

@st.cache_data(show_spinner=False)
def load_sektor_long() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "sektor_long.parquet")

@st.cache_data(show_spinner=False)
def load_table4() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "table4_karakteristik_tpt.parquet")

@st.cache_data(show_spinner=False)
def load_table5() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "table5_karakteristik_pekerja.parquet")

@st.cache_data(show_spinner=False)
def load_historis_gabungan() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "tpt_tpak_gabungan_2008_2025.parquet")

@st.cache_data(show_spinner=False)
def load_profil_volatilitas() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "profil_volatilitas_kabkota.parquet")

@st.cache_data(show_spinner=False)
def load_skor_risiko() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "skor_risiko_kabkota_2025.parquet")

@st.cache_data(show_spinner=False)
def load_tpt_umur_provinsi() -> pd.DataFrame:
    return pd.read_parquet(config.PATH_TPT_UMUR_PROVINSI)

@st.cache_data(show_spinner=False)
def load_tpt_umur_kabkota() -> pd.DataFrame:
    return pd.read_parquet(config.PATH_TPT_UMUR_KABKOTA)

@st.cache_data(show_spinner=False)
def load_ringkasan_feb() -> pd.DataFrame:
    df = pd.read_excel(config.PATH_PENDAMPING, sheet_name="Table 1")
    df = df.set_index(df.columns[0])
    df.index = df.index.str.strip()
    return df

@st.cache_data(show_spinner=False)
def load_forecast() -> pd.DataFrame:
    return pd.read_parquet(config.DATA_DIR / "forecast_tpt_tpak_2026_2028.parquet")

@st.cache_data(show_spinner=False)
def load_tren_provinsi_gabungan() -> pd.DataFrame:
    df_primer = load_ringkasan_prov().set_index("Jenis Kegiatan")
    kolom_agustus = [c for c in df_primer.columns if str(c).startswith("Agustus")]

    baris = []
    for kolom in kolom_agustus:
        tahun = int(str(kolom).split()[-1])
        baris.append({
            "periode": f"Ags {tahun}", "tahun": tahun, "urutan": tahun * 10 + 8,
            "TPT": float(df_primer.loc["TPT", kolom]), "TPAK": float(df_primer.loc["TPAK", kolom]),
            "sumber": "Primer (Agustus)",
        })

    tbl1 = pd.read_excel(config.PATH_PENDAMPING, sheet_name="Table 1")
    tbl4 = pd.read_excel(config.PATH_PENDAMPING, sheet_name="Table 4")
    tbl1 = tbl1.set_index(tbl1.columns[0])
    tbl4 = tbl4.set_index(tbl4.columns[0])

    for kolom in ["Feb 2024", "Feb 2025", "Feb 2026"]:
        if kolom not in tbl1.columns:
            continue
        tahun = int(kolom.split()[-1])
        try:
            tpak_val = tbl1.filter(like="Partisipasi", axis=0).iloc[0][kolom]
            tpt_val = tbl4.filter(like="Pengangguran", axis=0).iloc[0][kolom]
        except (IndexError, KeyError):
            continue
        baris.append({
            "periode": kolom, "tahun": tahun, "urutan": tahun * 10 + 2,
            "TPT": float(tpt_val), "TPAK": float(tpak_val), "sumber": "Pendamping (Februari)",
        })

    return pd.DataFrame(baris).sort_values("urutan").reset_index(drop=True)

def load_all() -> dict:
    return {
        "ringkasan_prov": load_ringkasan_prov(),
        "master_kabkota": load_master_kabkota(),
        "kabkota_long": load_kabkota_long(),
        "sektor_long": load_sektor_long(),
        "table4": load_table4(),
        "table5": load_table5(),
        "tpt_umur_provinsi": load_tpt_umur_provinsi(),
        "tpt_umur_kabkota": load_tpt_umur_kabkota(),
        "historis_gabungan": load_historis_gabungan(),
        "forecast": load_forecast(),
        "profil_volatilitas": load_profil_volatilitas(),
        "skor_risiko": load_skor_risiko(),
        "tren_provinsi": load_tren_provinsi_gabungan(),
        "ringkasan_feb": load_ringkasan_feb(),
        "geojson": load_geojson(),
    }