import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

historis = data["historis_gabungan"].copy()
profil_vol = data["profil_volatilitas"].copy()


st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Historis 2008–2025 · Volatilitas · Dampak Krisis",
    "Tren Terkini",
    "Perjalanan TPT & TPAK 38 Kabupaten/Kota sejak 2008, kestabilan tiap wilayah, dan bagaimana "
    "krisis 2008 & COVID-19 memengaruhi pengangguran.",
)

wilayah_list = sorted(historis["Kabupaten/Kota"].unique())

# ── Tren historis per kab/kota ────────────────────────────────
with st.container(border=True):
    utils.section_label("Tren Historis", "TPT & TPAK per Kabupaten/Kota (2008–2025)")
    wilayah_pilihan = st.selectbox("Pilih Kabupaten/Kota", wilayah_list,
                                    index=wilayah_list.index("Kota Surabaya") if "Kota Surabaya" in wilayah_list else 0)

    sub = historis[historis["Kabupaten/Kota"] == wilayah_pilihan].sort_values("tahun")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sub["tahun"], y=sub["TPT"], name="TPT (%)", mode="lines+markers",
        line=dict(color=config.COLOR_DANGER, width=2.5),
        marker=dict(size=[10 if v else 6 for v in sub["is_interpolasi_tpt"]],
                    symbol=["diamond" if v else "circle" for v in sub["is_interpolasi_tpt"]]),
    ))
    fig.add_trace(go.Scatter(
        x=sub["tahun"], y=sub["TPAK"], name="TPAK (%)", mode="lines+markers",
        line=dict(color=config.COLOR_PRIMARY, width=2.5), yaxis="y2",
        marker=dict(size=[10 if v else 6 for v in sub["is_interpolasi_tpak"]],
                    symbol=["diamond" if v else "circle" for v in sub["is_interpolasi_tpak"]]),
    ))
    fig.add_vrect(x0=2007.6, x1=2008.4, fillcolor=config.COLOR_MUTED, opacity=0.10, line_width=0,
                  annotation_text="Krisis 2008", annotation_position="top", annotation_font_size=10)
    fig.add_vrect(x0=2019.6, x1=2021.4, fillcolor=config.COLOR_MUTED, opacity=0.10, line_width=0,
                  annotation_text="COVID-19", annotation_position="top", annotation_font_size=10)
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
    st.plotly_chart(fig, width="stretch", config=config.plotly_config(f"tren_historis_{wilayah_pilihan}"))
    st.caption("◆ Penanda berlian = nilai tahun 2016 hasil interpolasi linear (bukan data pengamatan asli).")
    utils.tombol_unduh_csv(sub, f"historis_{wilayah_pilihan}.csv", key="dl_hist_wilayah")

st.markdown("")

# ── Profil volatilitas ──────────────────────────────────────────
with st.container(border=True):
    utils.section_label("Volatilitas", "Wilayah Paling Stabil vs Paling Fluktuatif",
                         "Diukur dari standar deviasi (std) TPT sepanjang 2008–2025 — semakin tinggi, "
                         "semakin fluktuatif riwayat TPT wilayah tersebut.")

    col_a, col_b = st.columns(2)
    with col_a:
        utils.judul_tabel("10 Wilayah Paling Stabil (std terendah)")
        stabil = profil_vol.sort_values("TPT_std").head(10)
        utils.tabel_rapi(stabil, kolom=["Kabupaten/Kota", "TPT_rata2", "TPT_std", "cv_TPT"])
    with col_b:
        utils.judul_tabel("10 Wilayah Paling Fluktuatif (std tertinggi)")
        fluktuatif = profil_vol.sort_values("TPT_std", ascending=False).head(10)
        utils.tabel_rapi(fluktuatif, kolom=["Kabupaten/Kota", "TPT_rata2", "TPT_std", "cv_TPT"])

    fig_vol = px.bar(
        profil_vol.sort_values("TPT_std", ascending=False).head(15),
        x="TPT_std", y="Kabupaten/Kota", orientation="h",
        color="TPT_std", color_continuous_scale=config.CHOROPLETH_SCALE,
        labels={"TPT_std": "Volatilitas TPT (std)"},
    )
    fig_vol.update_layout(
        height=460, margin=dict(t=20, l=10, r=10, b=10), showlegend=False,
        yaxis=dict(autorange="reversed"),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_vol, width="stretch", config=config.plotly_config("volatilitas_top15"))
    utils.tombol_unduh_csv(profil_vol, "profil_volatilitas_kabkota.csv", key="dl_volatilitas")

st.markdown("")

# ── Dampak krisis 2008 vs COVID-19 ───────────────────────────────
with st.container(border=True):
    utils.section_label("Dampak Krisis", "Krisis Finansial 2008 vs Pandemi COVID-19",
                         "Perubahan TPT (poin persen) di sekitar masing-masing periode krisis, per wilayah.")

    top_terdampak_covid = profil_vol.sort_values("delta_TPT_covid", ascending=False).head(10)
    fig_krisis = go.Figure()
    fig_krisis.add_trace(go.Bar(
        name="Δ TPT Krisis 2008", y=top_terdampak_covid["Kabupaten/Kota"], x=top_terdampak_covid["delta_TPT_krisis2008"],
        orientation="h", marker_color=config.COLOR_MUTED,
    ))
    fig_krisis.add_trace(go.Bar(
        name="Δ TPT COVID-19", y=top_terdampak_covid["Kabupaten/Kota"], x=top_terdampak_covid["delta_TPT_covid"],
        orientation="h", marker_color=config.COLOR_DANGER,
    ))
    fig_krisis.update_layout(
        barmode="group", height=440, margin=dict(t=20, l=10, r=10, b=10),
        xaxis_title="Perubahan TPT (poin persen)",
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", y=1.1),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis_gridcolor=config.COLOR_BORDER,
    )
    st.plotly_chart(fig_krisis, width="stretch", config=config.plotly_config("dampak_krisis_top10_covid"))
    st.caption(
        "10 wilayah dengan kenaikan TPT terbesar di sekitar COVID-19 (2020–2021), dibandingkan "
        "dengan perubahan TPT pada krisis 2008."
    )

    st.markdown("")
    rata_delta_2008 = profil_vol["delta_TPT_krisis2008"].mean()
    rata_delta_covid = profil_vol["delta_TPT_covid"].mean()
    st.markdown(
        f"Secara rata-rata di 38 kab/kota, TPT berubah **{rata_delta_2008:+.2f} poin** di sekitar krisis "
        f"2008 dan **{rata_delta_covid:+.2f} poin** di sekitar COVID-19 — "
        + ("menunjukkan dampak COVID-19 secara rata-rata lebih besar terhadap pengangguran di Jatim."
           if abs(rata_delta_covid) > abs(rata_delta_2008) else
           "menunjukkan dampak krisis 2008 secara rata-rata lebih besar terhadap pengangguran di Jatim.")
    )

st.markdown("")

with st.container(border=True):
    utils.section_label("Data", "Data Mentah — Historis TPT & TPAK Gabungan")
    utils.tabel_rapi(historis, height=230)
    utils.tombol_unduh_csv(historis, "historis_tpt_tpak_2008_2025.csv", key="dl_hist_all")
