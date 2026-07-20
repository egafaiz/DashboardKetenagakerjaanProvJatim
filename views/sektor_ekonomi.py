import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

sektor = data["sektor_long"].copy()
KOL_SEKTOR = "Lapangan Pekerjaan Utama"

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Komposisi Lapangan Usaha · Level Provinsi",
    "Sektor Ekonomi",
    "Penyerapan tenaga kerja pada 17 lapangan usaha, Provinsi Jawa Timur, 2023–2025.",
)

tahun_terbaru = int(sektor["tahun"].max())
sektor_terbaru = sektor[sektor["tahun"] == tahun_terbaru].sort_values("Bekerja", ascending=False).reset_index(drop=True)
total_bekerja = sektor_terbaru["Bekerja"].sum()
sektor_terbaru["persen"] = sektor_terbaru["Bekerja"] / total_bekerja * 100

sektor_top = sektor_terbaru.iloc[0]
col1, col2, col3 = st.columns(3)
with col1:
    utils.metric_like(f"Sektor Terbesar ({tahun_terbaru})", sektor_top[KOL_SEKTOR],
                       f"{sektor_top['persen']:.1f}% dari total", delta_positif=True,
                       value_font_size="1.25rem")
col2.metric("Jumlah Lapangan Usaha", f"{sektor_terbaru.shape[0]} sektor",
            help="Jumlah kategori lapangan usaha yang tercatat.")
col3.metric(f"Total Penduduk Bekerja ({tahun_terbaru})", f"{total_bekerja:,.0f}".replace(",", "."),
            help="Total penduduk bekerja di seluruh sektor, provinsi Jawa Timur.")

st.markdown("")

with st.container(border=True):
    head_l, head_r = st.columns([5, 1])
    with head_l:
        utils.section_label("Komposisi", f"Penyerapan Tenaga Kerja per Sektor — {tahun_terbaru}")
    with head_r:
        utils.tombol_unduh_csv(sektor_terbaru, f"sektor_{tahun_terbaru}.csv", key="dl_sektor_terbaru")

    fig_bar = px.bar(
        sektor_terbaru.sort_values("Bekerja"),
        x="Bekerja", y=KOL_SEKTOR, orientation="h",
        color=KOL_SEKTOR, color_discrete_sequence=config.SEKTOR_WARNA,
        text=sektor_terbaru.sort_values("Bekerja")["persen"].map(lambda v: f"{v:.1f}%"),
    )
    fig_bar.update_traces(textposition="outside", cliponaxis=False)
    fig_bar.update_layout(
        showlegend=False, height=560, margin=dict(t=10, l=10, r=40, b=10),
        xaxis_title="Penduduk Bekerja", yaxis_title="",
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor=config.COLOR_BORDER),
    )
    st.plotly_chart(fig_bar, width="stretch", config=config.plotly_config(f"sektor_bekerja_{tahun_terbaru}"))

st.markdown("")

with st.container(border=True):
    utils.section_label("Tren", "Pergeseran Pangsa Sektor, 2023–2025",
                         "5 sektor dengan penyerapan terbesar pada tahun terbaru, ditelusuri sepanjang waktu.")

    total_per_tahun = sektor.groupby("tahun")["Bekerja"].transform("sum")
    sektor = sektor.assign(persen=sektor["Bekerja"] / total_per_tahun * 100)
    top5_sektor = sektor_terbaru.head(5)[KOL_SEKTOR].tolist()
    sektor_top5 = sektor[sektor[KOL_SEKTOR].isin(top5_sektor)]

    fig_line = px.line(
        sektor_top5, x="tahun", y="persen", color=KOL_SEKTOR, markers=True,
        color_discrete_sequence=config.SEKTOR_WARNA,
        labels={"persen": "Pangsa (%)", "tahun": "Tahun"},
    )
    fig_line.update_layout(
        height=400, margin=dict(t=20, l=10, r=10, b=10),
        legend=dict(orientation="h", y=-0.25),
        xaxis=dict(dtick=1, gridcolor=config.COLOR_BORDER),
        yaxis=dict(gridcolor=config.COLOR_BORDER),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_line, width="stretch", config=config.plotly_config("tren_pangsa_sektor_top5"))

st.markdown("")

with st.container(border=True):
    utils.section_label("Data", "Data Mentah — Seluruh Sektor & Tahun")
    utils.tabel_rapi(sektor.sort_values(["tahun", "Bekerja"], ascending=[True, False]), height=230)
    utils.tombol_unduh_csv(sektor, "sektor_long_semua_tahun.csv", key="dl_sektor_all")
