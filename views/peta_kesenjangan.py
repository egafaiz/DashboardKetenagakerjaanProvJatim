import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

master = data["master_kabkota"]
geojson = data["geojson"]

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header("Sebaran Wilayah", "Peta & Kesenjangan Antar Kab/Kota",
                   "TPT, Upah, dan Composite Index untuk 38 Kabupaten/Kota — 2025")

with st.container(border=True):
    utils.section_label("Composite Index", "Atur Bobot TPT vs Upah",
                         "Default 50/50 sesuai desain Tahap 4 — geser untuk eksplorasi skenario lain.")
    bobot_tpt = st.slider("Bobot TPT (semakin rendah TPT = semakin baik)", 0, 100, 50, step=5) / 100
    bobot_upah = 1 - bobot_tpt
    st.caption(f"Bobot Upah otomatis: {bobot_upah:.0%}")

    master_view = master.copy()
    master_view["composite_index_custom"] = (
        master_view["skor_TPT_2025"] * bobot_tpt + master_view["skor_Upah_2025"] * bobot_upah
    ).round(2)
    master_view["rank_composite_custom"] = master_view["composite_index_custom"].rank(ascending=False).astype(int)

    if bobot_tpt != 0.5:
        st.markdown('<div class="note-box">Bobot diubah dari default 50/50 — hasil ranking di bawah ini '
                    'adalah skenario eksplorasi, bukan Composite Index resmi dashboard.</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        utils.judul_tabel("Top 10 — Composite Index Tertinggi")
        utils.tabel_rapi(
            master_view.sort_values("rank_composite_custom").head(10),
            kolom=["Kabupaten/Kota", "TPT 2025", "Upah 2025", "composite_index_custom", "rank_composite_custom"],
        )
    with col_r:
        utils.judul_tabel("Bottom 10 — Composite Index Terendah")
        utils.tabel_rapi(
            master_view.sort_values("rank_composite_custom").tail(10),
            kolom=["Kabupaten/Kota", "TPT 2025", "Upah 2025", "composite_index_custom", "rank_composite_custom"],
        )
    utils.tombol_unduh_csv(master_view, "composite_index_kabkota.csv", key="dl_composite")

st.markdown("")

with st.container(border=True):
    head_l, head_r = st.columns([5, 1])
    with head_l:
        utils.section_label("Peta", "Sebaran TPT per Kabupaten/Kota — 2025")
    with head_r:
        utils.tombol_unduh_csv(master[["Kabupaten/Kota", "TPT 2025", "Upah 2025"]], "tpt_upah_kabkota_2025.csv", key="dl_peta")

    fig_map = px.choropleth(
        master, geojson=geojson, locations="Kabupaten/Kota",
        featureidkey=config.GEOJSON_FEATURE_ID_KEY, color="TPT 2025",
        color_continuous_scale=config.CHOROPLETH_SCALE,
        hover_name="Kabupaten/Kota",
        hover_data={"TPT 2025": ":.2f", "Upah 2025": ":,.0f"},
        labels={"TPT 2025": "TPT (%)", "Upah 2025": "Upah (Rp)"},
    )
    fig_map.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.7)
    fig_map.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig_map.update_layout(
        height=500, margin=dict(l=0, r=0, t=8, b=0),
        coloraxis_colorbar=dict(title="TPT (%)"),
        font_family=config.FONT_BODY, font_color=config.COLOR_INK,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_map, width="stretch", config=config.plotly_config("peta_tpt_kabkota_2025"))
    
st.markdown("")

with st.container(border=True):
    utils.section_label("Compare Mode", "Bandingkan Dua Kab/Kota")

    wilayah_list = sorted(master["Kabupaten/Kota"].unique())
    col_a, col_b = st.columns(2)
    with col_a:
        wilayah_a = st.selectbox("Wilayah A", wilayah_list, index=wilayah_list.index("Kota Surabaya") if "Kota Surabaya" in wilayah_list else 0)
    with col_b:
        default_b = next((w for w in wilayah_list if w != wilayah_a), wilayah_list[0])
        wilayah_b = st.selectbox("Wilayah B", wilayah_list, index=wilayah_list.index(default_b))

    if wilayah_a == wilayah_b:
        st.warning("Pilih dua wilayah yang berbeda untuk dibandingkan.")
    else:
        row_a = master[master["Kabupaten/Kota"] == wilayah_a].iloc[0]
        row_b = master[master["Kabupaten/Kota"] == wilayah_b].iloc[0]

        cA, cB = st.columns(2)
        cA.metric(wilayah_a, f"TPT {row_a['TPT 2025']:.2f}%", f"Upah Rp{row_a['Upah 2025']:,.0f}".replace(",", "."))
        cB.metric(wilayah_b, f"TPT {row_b['TPT 2025']:.2f}%", f"Upah Rp{row_b['Upah 2025']:,.0f}".replace(",", "."))

        fig_cmp = go.Figure(data=[
            go.Bar(name="TPT (%)", x=[wilayah_a, wilayah_b], y=[row_a["TPT 2025"], row_b["TPT 2025"]],
                   marker_color=config.COLOR_PRIMARY),
        ])
        fig_cmp.update_layout(height=320, margin=dict(t=20), font_family=config.FONT_BODY,
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cmp, width="stretch", config=config.plotly_config(f"compare_{wilayah_a}_{wilayah_b}"))

        def _narasi_perbandingan(a, b):
            tpt_winner = a["Kabupaten/Kota"] if a["TPT 2025"] < b["TPT 2025"] else b["Kabupaten/Kota"]
            upah_winner = a["Kabupaten/Kota"] if a["Upah 2025"] > b["Upah 2025"] else b["Kabupaten/Kota"]
            return (
                f"Dibandingkan **{b['Kabupaten/Kota']}**, **{a['Kabupaten/Kota']}** memiliki TPT "
                f"{'lebih rendah' if a['TPT 2025'] < b['TPT 2025'] else 'lebih tinggi'} "
                f"({a['TPT 2025']:.2f}% vs {b['TPT 2025']:.2f}%) — **{tpt_winner}** unggul dalam penyerapan tenaga kerja. "
                f"Untuk upah, **{upah_winner}** mencatat rata-rata lebih tinggi "
                f"(Rp{a['Upah 2025']:,.0f} vs Rp{b['Upah 2025']:,.0f})."
            )

        st.markdown(_narasi_perbandingan(row_a, row_b))