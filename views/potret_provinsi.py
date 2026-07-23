import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

ringkasan_prov = data["ringkasan_prov"]
historis = data["historis_gabungan"]
tren_prov = data["tren_provinsi"]

rd = ringkasan_prov.set_index("Jenis Kegiatan")

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Indikator Makro · Provinsi Jawa Timur",
    "Potret Provinsi",
    "Kondisi ketenagakerjaan Jawa Timur secara agregat — TPT, TPAK, dan tren historis 2008–2025.",
)

tpt_25, tpt_24 = rd.loc["TPT", "Agustus 2025"], rd.loc["TPT", "Agustus 2024"]
tpak_25, tpak_24 = rd.loc["TPAK", "Agustus 2025"], rd.loc["TPAK", "Agustus 2024"]
bekerja_25, bekerja_24 = rd.loc["Bekerja", "Agustus 2025"], rd.loc["Bekerja", "Agustus 2024"]
angkatan_kerja_25, angkatan_kerja_24 = rd.loc["Angkatan Kerja", "Agustus 2025"], rd.loc["Angkatan Kerja", "Agustus 2024"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("TPT Agustus 2025", f"{tpt_25:.2f}%", f"{tpt_25 - tpt_24:+.2f} poin vs Agustus 2024", delta_color="inverse")
col2.metric("TPAK Agustus 2025", f"{tpak_25:.2f}%", f"{tpak_25 - tpak_24:+.2f} poin vs Agustus 2024")
col3.metric("Penduduk Bekerja", f"{bekerja_25:,.0f}".replace(",", "."),
            f"{(bekerja_25 - bekerja_24) / bekerja_24 * 100:+.2f}% vs Agustus 2024")
col4.metric("Angkatan Kerja", f"{angkatan_kerja_25:,.0f}".replace(",", "."),
            f"{(angkatan_kerja_25 - angkatan_kerja_24) / angkatan_kerja_24 * 100:+.2f}% vs Agustus 2024")

st.caption(f"Sumber: {config.SUMBER_PRIMER}")
st.markdown("")

delta_tpt = tpt_25 - tpt_24
arah_tpt = "membaik (menurun)" if delta_tpt < 0 else "memburuk (meningkat)" if delta_tpt > 0 else "stabil"
delta_tpak = tpak_25 - tpak_24
arah_tpak = "meningkat" if delta_tpak > 0 else "menurun" if delta_tpak < 0 else "stabil"

with st.container(border=True):
    utils.section_label("Ringkasan", "Poin Penting")
    st.markdown(
        f"TPT Jawa Timur **{arah_tpt}** dari {tpt_24:.2f}% (Agustus 2024) menjadi {tpt_25:.2f}% "
        f"(Agustus 2025), sementara TPAK **{arah_tpak}** dari {tpak_24:.2f}% menjadi {tpak_25:.2f}%. "
        f"Total angkatan kerja per Agustus 2025 mencapai {angkatan_kerja_25:,.0f}".replace(",", ".") +
        f" jiwa, dengan {bekerja_25:,.0f}".replace(",", ".") + " jiwa di antaranya bekerja."
    )

st.markdown("")

with st.container(border=True):
    utils.section_label("Historis", "Tren TPT & TPAK Provinsi (2008–2025)",
                         "Rata-rata agregasi 38 kab/kota, hasil olah BPS Web API.")

    tren_hist = historis.groupby("tahun")[["TPT", "TPAK"]].mean().reset_index()
    tahun_interpolasi = sorted(historis.loc[historis["is_interpolasi_tpt"], "tahun"].unique().tolist())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tren_hist["tahun"], y=tren_hist["TPT"], name="TPT (%)", mode="lines+markers",
        line=dict(color=config.COLOR_DANGER, width=2.5), marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=tren_hist["tahun"], y=tren_hist["TPAK"], name="TPAK (%)", mode="lines+markers",
        line=dict(color=config.COLOR_PRIMARY, width=2.5), marker=dict(size=6), yaxis="y2",
    ))
    if tahun_interpolasi:
        fig.add_vrect(
            x0=tahun_interpolasi[0] - 0.5, x1=tahun_interpolasi[-1] + 0.5,
            fillcolor=config.COLOR_WARNING, opacity=0.12, line_width=0,
            annotation_text="2016: interpolasi", annotation_position="top",
            annotation_font_size=11, annotation_font_color=config.COLOR_WARNING,
        )
    fig.update_layout(
        yaxis=dict(title="TPT (%)", gridcolor=config.COLOR_BORDER),
        yaxis2=dict(title="TPAK (%)", overlaying="y", side="right", showgrid=False),
        xaxis=dict(dtick=1, gridcolor=config.COLOR_BORDER),
        legend=dict(orientation="h", y=1.12, x=0),
        height=420, margin=dict(t=40, l=10, r=10, b=10),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch", config=config.plotly_config("tren_tpt_tpak_provinsi_2008_2025"))

    st.markdown(
        '<div class="note-box">Nilai tahun 2016 hasil interpolasi linear (gap data resmi BPS di seluruh '
        '38 kab/kota). Detail lengkap ada di halaman Insight & Rekomendasi → Metodologi.</div>',
        unsafe_allow_html=True,
    )

st.markdown("")

with st.container(border=True):
    utils.section_label("Gabungan Sumber", "Tren Semesteran TPT & TPAK")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=tren_prov["periode"], y=tren_prov["TPT"], name="TPT (%)", mode="lines+markers",
        line=dict(color=config.COLOR_DANGER, width=2.5),
    ))
    fig2.add_trace(go.Scatter(
        x=tren_prov["periode"], y=tren_prov["TPAK"], name="TPAK (%)", mode="lines+markers",
        line=dict(color=config.COLOR_PRIMARY, width=2.5), yaxis="y2",
    ))
    fig2.update_layout(
        yaxis=dict(title="TPT (%)", gridcolor=config.COLOR_BORDER),
        yaxis2=dict(title="TPAK (%)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.15, x=0),
        height=360, margin=dict(t=40, l=10, r=10, b=10),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
    )
    st.plotly_chart(fig2, width="stretch", config=config.plotly_config("tren_semesteran_provinsi"))

st.markdown("")

with st.container(border=True):
    utils.section_label("Data", "Data Mentah — Potret Provinsi")
    utils.tabel_rapi(ringkasan_prov)
    utils.tombol_unduh_csv(ringkasan_prov, "potret_provinsi.csv", key="dl_ringkasan_prov")
