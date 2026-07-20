import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

table4 = data["table4"].copy()
table5 = data["table5"].copy()

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Gender · Pendidikan · Formal-Informal · Level Provinsi",
    "Karakteristik Pekerja",
    "TPT menurut karakteristik demografis (Table 4) dan komposisi pekerja menurut status "
    "& pendidikan (Table 5) — Data Pendamping BPS Jatim, Februari 2024–2026.",
)
st.caption(f"Sumber: {config.SUMBER_PENDAMPING}")

tab1, tab2 = st.tabs(["TPT Menurut Karakteristik", "Karakteristik Pekerja"])

with tab1:
    tpt_total = table4[table4["kategori"].isna()].iloc[0]
    st.markdown(
        f'<div class="note-box">TPT Provinsi Jawa Timur (total, Februari 2026): '
        f'<b>{tpt_total["Feb 2026"]:.2f}%</b>, berubah {tpt_total["Perubahan (persen poin)"]:+.2f} poin '
        f'dari Februari 2024.</div>',
        unsafe_allow_html=True,
    )

    for kategori in table4["kategori"].dropna().unique():
        sub = table4[table4["kategori"] == kategori].copy()
        sub["Karakteristik"] = sub["Karakteristik"].str.replace("– ", "", regex=False)

        with st.container(border=True):
            utils.section_label("TPT", kategori)
            col_chart, col_table = st.columns([3, 2])
            with col_chart:
                fig = go.Figure()
                for kolom, warna in zip(["Feb 2024", "Feb 2025", "Feb 2026"],
                                         [config.COLOR_ACCENT, config.COLOR_PRIMARY, config.COLOR_PRIMARY_DARK]):
                    fig.add_trace(go.Bar(name=kolom, x=sub["Karakteristik"], y=sub[kolom], marker_color=warna))
                fig.update_layout(
                    barmode="group", height=320, margin=dict(t=10, l=10, r=10, b=10),
                    yaxis_title="TPT (%)", legend=dict(orientation="h", y=1.15),
                    font_family=config.FONT_BODY, font_color=config.COLOR_INK,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(gridcolor=config.COLOR_BORDER),
                )
                st.plotly_chart(fig, width="stretch", config=config.plotly_config(f"tpt_{kategori}"))
            with col_table:
                utils.tabel_rapi(sub, kolom=["Karakteristik", "Feb 2024", "Feb 2025", "Feb 2026", "Perubahan (persen poin)"])

    st.markdown("")
    with st.container(border=True):
        utils.section_label("Insight", "Mismatch Pendidikan–Lapangan Kerja")
        pend = table4[table4["kategori"] == "TPT Menurut Pendidikan Tertinggi yang Ditamatkan"]
        tertinggi = pend.loc[pend["Feb 2026"].idxmax()]
        st.markdown(
            f"TPT tertinggi pada Februari 2026 justru berada pada lulusan "
            f"**{tertinggi['Karakteristik'].replace('– ', '')}** ({tertinggi['Feb 2026']:.2f}%), bukan "
            f"jenjang pendidikan terendah — mengindikasikan mismatch antara kualifikasi pendidikan dan "
            f"ketersediaan lapangan kerja yang sesuai, konsisten dengan temuan EDA Tahap 3."
        )

    st.markdown("")
    with st.container(border=True):
        utils.section_label("Data", "Data Mentah")
        utils.tabel_rapi(table4, height=230)
        utils.tombol_unduh_csv(table4, "table4_karakteristik_tpt.csv", key="dl_table4")

with tab2:
    st.markdown(
        '<div class="warning-box">Bagian <b>"Lapangan Usaha"</b> pada Table 5 hanya terisi untuk '
        'Februari 2026 — kolom 2024 &amp; 2025 kosong beneran (gap data asli dari sumber BPS, '
        '<b>tidak diimputasi</b>, hanya didokumentasikan apa adanya).</div>',
        unsafe_allow_html=True,
    )

    kategori_list = table5["kategori"].dropna().unique().tolist()
    kategori_pilih = st.selectbox("Pilih Kategori", kategori_list)

    sub5 = table5[table5["kategori"] == kategori_pilih].copy()
    sub5["Karakteristik"] = sub5["Karakteristik"].str.replace("– ", "", regex=False)

    with st.container(border=True):
        utils.section_label("Karakteristik Pekerja", kategori_pilih)

        kolom_persen = [c for c in sub5.columns if c.startswith("Persentase")]
        tahun_tersedia = [c.replace("Persentase ", "").replace(" (%)", "") for c in kolom_persen
                           if sub5[c].notna().any()]

        if kategori_pilih == "Lapangan Usaha":
            st.caption("Hanya tersedia untuk Februari 2026 (lihat catatan gap data di atas).")
            fig = px.pie(
                sub5, names="Karakteristik", values="Persentase 2026 (%)",
                color_discrete_sequence=config.SEKTOR_WARNA, hole=0.4,
            )
            fig.update_layout(height=440, margin=dict(t=10, l=10, r=10, b=10),
                               font_family=config.FONT_BODY,
                               paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, width="stretch", config=config.plotly_config("lapangan_usaha_feb2026"))
        else:
            fig = go.Figure()
            warna_map = {"2024": config.COLOR_ACCENT, "2025": config.COLOR_PRIMARY, "2026": config.COLOR_PRIMARY_DARK}
            for th in tahun_tersedia:
                fig.add_trace(go.Bar(name=f"Feb {th}", x=sub5["Karakteristik"], y=sub5[f"Persentase {th} (%)"],
                                      marker_color=warna_map.get(th, config.COLOR_MUTED)))
            fig.update_layout(
                barmode="group", height=380, margin=dict(t=10, l=10, r=10, b=10),
                yaxis_title="Persentase (%)", legend=dict(orientation="h", y=1.15),
                font_family=config.FONT_BODY, font_color=config.COLOR_INK,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor=config.COLOR_BORDER),
            )
            st.plotly_chart(fig, width="stretch", config=config.plotly_config(f"karakteristik_{kategori_pilih}"))

        kolom_tampil = ["Karakteristik"] + [c for c in sub5.columns if c not in ("Karakteristik", "kategori")
                                             and sub5[c].notna().any()]
        utils.tabel_rapi(sub5, kolom=kolom_tampil)

    st.markdown("")
    with st.container(border=True):
        utils.section_label("Insight", "Formal vs Informal")
        formal = table5[table5["kategori"] == "Kegiatan Formal/Informal"]
        informal_row = formal[formal["Karakteristik"].str.contains("Informal")].iloc[0]
        st.markdown(
            f"Pada Februari 2026, **{informal_row['Persentase 2026 (%)']:.1f}%** pekerja Jawa Timur "
            f"berstatus **informal** — proporsi ini relatif stabil dibanding Februari 2024 "
            f"({informal_row['Persentase 2024 (%)']:.1f}%), menunjukkan struktur pasar kerja yang belum "
            f"banyak bergeser ke sektor formal dalam periode ini."
        )

    st.markdown("")
    with st.container(border=True):
        utils.section_label("Data", "Data Mentah")
        utils.tabel_rapi(table5, height=230)
        utils.tombol_unduh_csv(table5, "table5_karakteristik_pekerja.csv", key="dl_table5")
