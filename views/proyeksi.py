import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

historis = data["historis_gabungan"].copy()
forecast = data["forecast"].copy()

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Eksploratif · Holt's Linear Trend dengan Damping (2008–2025 → 2026–2028)",
    "Proyeksi TPT & TPAK",
    "Proyeksi 3 tahun ke depan berbasis tren historis 2008–2025. Bersifat eksploratif, "
    "bukan angka resmi BPS — gunakan sebagai bahan diskusi, bukan dasar tunggal kebijakan.",
)

col_a, col_b, col_c = st.columns(3)
level_pilihan = col_a.radio("Level wilayah", ["Provinsi", "Kabupaten/Kota"], horizontal=True)
variabel_pilihan = col_b.radio("Variabel", ["TPT", "TPAK"], horizontal=True)

if level_pilihan == "Kabupaten/Kota":
    wilayah_list = sorted(historis["Kabupaten/Kota"].unique())
    default_idx = wilayah_list.index("Kota Surabaya") if "Kota Surabaya" in wilayah_list else 0
    wilayah_pilihan = col_c.selectbox("Kabupaten/Kota", wilayah_list, index=default_idx)
    hist_sub = historis[historis["Kabupaten/Kota"] == wilayah_pilihan].sort_values("tahun")
    fc_sub = forecast[
        (forecast["level"] == "kabkota")
        & (forecast["wilayah"] == wilayah_pilihan)
        & (forecast["variabel"] == variabel_pilihan)
    ].sort_values("tahun")
    judul_chart = f"{variabel_pilihan} · {wilayah_pilihan}"
else:
    col_c.markdown("&nbsp;", unsafe_allow_html=True)
    hist_sub = historis.groupby("tahun", as_index=False)[variabel_pilihan].mean()
    fc_sub = forecast[
        (forecast["level"] == "provinsi") & (forecast["variabel"] == variabel_pilihan)
    ].sort_values("tahun")
    judul_chart = f"{variabel_pilihan} · Rata-rata Provinsi (38 kab/kota)"

if fc_sub.empty:
    st.warning("Data historis wilayah ini tidak cukup panjang untuk diproyeksikan.")
else:
    warna_line = config.COLOR_DANGER if variabel_pilihan == "TPT" else config.COLOR_PRIMARY

    tahun_hist = hist_sub["tahun"].tolist()
    nilai_hist = hist_sub[variabel_pilihan].tolist()
    tahun_fc = fc_sub["tahun"].tolist()
    nilai_fc = fc_sub["forecast"].tolist()
    lower_fc = fc_sub["lower"].tolist()
    upper_fc = fc_sub["upper"].tolist()

    sambung_tahun = [tahun_hist[-1]] + tahun_fc
    sambung_nilai = [nilai_hist[-1]] + nilai_fc
    sambung_lower = [nilai_hist[-1]] + lower_fc
    sambung_upper = [nilai_hist[-1]] + upper_fc

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sambung_tahun + sambung_tahun[::-1],
        y=sambung_upper + sambung_lower[::-1],
        fill="toself", fillcolor="rgba(37,99,235,0.12)" if variabel_pilihan == "TPAK" else "rgba(220,38,38,0.10)",
        line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", showlegend=False,
        name="Pita keyakinan",
    ))
    fig.add_trace(go.Scatter(
        x=tahun_hist, y=nilai_hist, mode="lines+markers", name="Historis (2008–2025)",
        line=dict(color=config.COLOR_INK, width=2.5), marker=dict(size=7),
    ))
    fig.add_trace(go.Scatter(
        x=sambung_tahun, y=sambung_nilai, mode="lines+markers", name="Proyeksi (2026–2028)",
        line=dict(color=warna_line, width=2.5, dash="dash"), marker=dict(size=9, symbol="diamond"),
    ))

    fig.update_layout(
        template=config.PLOTLY_TEMPLATE,
        title=judul_chart,
        yaxis_title=f"{variabel_pilihan} (%)",
        xaxis_title="Tahun",
        height=460,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig = utils.clean_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(3)
    for i, row in enumerate(fc_sub.itertuples()):
        with cols[i]:
            utils.stat_card(
                f"Proyeksi {row.tahun}",
                f"{row.forecast:.2f}%",
                f"kisaran {row.lower:.2f}–{row.upper:.2f}%",
                delta_positif=True,
            )

st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
with st.container(border=True):
    utils.section_label("Seluruh Wilayah", f"Proyeksi {variabel_pilihan} 2026–2028 · 38 Kabupaten/Kota")
    tabel_kabkota = forecast[
        (forecast["level"] == "kabkota") & (forecast["variabel"] == variabel_pilihan)
    ].pivot_table(index="wilayah", columns="tahun", values="forecast").reset_index()
    tabel_kabkota.columns = ["Kabupaten/Kota"] + [f"Proyeksi {int(c)}" for c in tabel_kabkota.columns[1:]]
    utils.tabel_rapi(tabel_kabkota, height=360)
    utils.tombol_unduh_csv(tabel_kabkota, f"proyeksi_{variabel_pilihan.lower()}_2026_2028.csv",
                            label=f"Unduh proyeksi {variabel_pilihan} seluruh kab/kota (CSV)")