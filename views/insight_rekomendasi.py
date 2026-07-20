import pandas as pd
import plotly.express as px
import streamlit as st

import config
import utils

data = utils.guard_data_loaded()

skor_risiko = data["skor_risiko"].copy()
profil_vol = data["profil_volatilitas"].copy()

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
utils.page_header(
    "Early-Warning · Skor Risiko · Metodologi",
    "Insight & Rekomendasi",
    "Wilayah mana yang perlu perhatian lebih dulu — berbasis skor risiko relatif, bukan ambang prediktif.",
)

# ── Ringkasan tier ────────────────────────────────────────────
n_tinggi = (skor_risiko["tier_risiko"] == "Tinggi").sum()
n_sedang = (skor_risiko["tier_risiko"] == "Sedang").sum()
n_rendah = (skor_risiko["tier_risiko"] == "Rendah").sum()
col1, col2, col3 = st.columns(3)
col1.metric("Tier Tinggi", f"{n_tinggi} wilayah")
col2.metric("Tier Sedang", f"{n_sedang} wilayah")
col3.metric("Tier Rendah", f"{n_rendah} wilayah")

st.markdown("")

# ── Skor risiko early-warning ────────────────────────────────
with st.container(border=True):
    utils.section_label("Early-Warning", "Skor Risiko Kab/Kota (2025)",
                         "Skor relatif (percentile) terhadap 38 kab/kota di tahun yang sama — flag wilayah "
                         "dengan TPT naik 2 tahun berturut-turut dan berada di atas rata-rata provinsi.")

    st.markdown(
        '<div class="note-box">Validasi 2020: 3 dari 5 wilayah paling terdampak COVID-19 ter-tier '
        '"Tinggi" pada metodologi ini. Skor bersifat relatif antar-wilayah, bukan ambang prediktif.</div>',
        unsafe_allow_html=True,
    )

    tier_filter = st.multiselect("Filter Tier Risiko", ["Tinggi", "Sedang", "Rendah"], default=["Tinggi", "Sedang"])
    tampil = skor_risiko[skor_risiko["tier_risiko"].isin(tier_filter)].sort_values("skor_risiko", ascending=False)

    col_chart, col_table = st.columns([2, 3])
    with col_chart:
        fig = px.bar(
            tampil.sort_values("skor_risiko").tail(15), x="skor_risiko", y="Kabupaten/Kota",
            orientation="h", color="tier_risiko",
            color_discrete_map=config.TIER_RISIKO_WARNA,
            labels={"skor_risiko": "Skor Risiko (0-100)", "tier_risiko": "Tier"},
        )
        fig.update_layout(
            height=460, margin=dict(t=10, l=10, r=10, b=10),
            legend=dict(orientation="h", y=1.1),
            font_family=config.FONT_BODY, font_color=config.COLOR_INK,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor=config.COLOR_BORDER),
        )
        st.plotly_chart(fig, width="stretch", config=config.plotly_config("skor_risiko_top15"))
    with col_table:
        utils.judul_tabel("Daftar Wilayah — Terpilih")
        utils.tabel_rapi(
            tampil,
            kolom=["Kabupaten/Kota", "TPT_2025", "kenaikan_3th", "naik_terus_3th", "skor_risiko", "tier_risiko"],
            height=460,
        )
    utils.tombol_unduh_csv(skor_risiko, "skor_risiko_kabkota_2025.csv", key="dl_skor_risiko")

st.markdown("")

# ── Profil volatilitas ─────────────────────────────────────────
with st.container(border=True):
    utils.section_label("Volatilitas", "Profil Volatilitas & Dampak Krisis — Ringkasan",
                         "Lihat halaman Tren Terkini untuk visualisasi lengkap; tabel di bawah untuk referensi cepat.")
    utils.tabel_rapi(profil_vol.sort_values("TPT_std", ascending=False), height=230)
    utils.tombol_unduh_csv(profil_vol, "profil_volatilitas_kabkota.csv", key="dl_vol_insight")

st.markdown("")

# ── Rekomendasi naratif ─────────────────────────────────────────
with st.container(border=True):
    utils.section_label("Rekomendasi", "Ringkasan untuk Pengambil Kebijakan")
    top3 = skor_risiko.sort_values("skor_risiko", ascending=False).head(3)["Kabupaten/Kota"].tolist()
    top3_str = ", ".join(top3[:-1]) + f", dan {top3[-1]}" if len(top3) > 1 else top3[0]

    rekomendasi_items = [
        dict(
            tag="Prioritas", warna="danger", glyph="!",
            judul="Prioritas pemantauan jangka pendek",
            isi=f"<strong>{top3_str}</strong> — skor risiko tertinggi 2025, TPT naik konsisten di atas "
                f"rata-rata provinsi selama 2 tahun terakhir.",
        ),
        dict(
            tag="Catatan", warna="warning", glyph="i",
            judul="Bukan sinyal krisis pasti",
            isi="Skor bersifat relatif antar-wilayah pada satu tahun, sehingga perlu dikombinasikan "
                "dengan konteks lapangan (mis. penutupan industri besar, migrasi tenaga kerja) sebelum "
                "menjadi dasar kebijakan.",
        ),
        dict(
            tag="Insight", warna="primary", glyph="~",
            judul="Wilayah upah tinggi bukan otomatis paling sehat",
            isi="Korelasi Upah vs TPT 2025 justru positif (r≈0,55–0,60), pola <em>urban unemployment</em> "
                "di daerah seperti Sidoarjo, Surabaya, dan Gresik.",
        ),
        dict(
            tag="Roadmap", warna="muted", glyph="…",
            judul="Fitur what-if sengaja tidak disertakan",
            isi="Simulasi proyeksi Upah vs TPT dianggap riskan secara statistik pada sampel 38 kab/kota "
                "di v1 dashboard ini — masuk rencana pengembangan lanjutan.",
        ),
    ]

    kartu_html = "".join(
        f'<div class="rekom-card rekom-card--{r["warna"]}">'
        f'<div class="rekom-card-top">'
        f'<span class="rekom-card-glyph">{r["glyph"]}</span>'
        f'<span class="rekom-card-tag">{r["tag"]}</span>'
        f'</div>'
        f'<div class="rekom-card-judul">{r["judul"]}</div>'
        f'<div class="rekom-card-isi">{r["isi"]}</div>'
        f'</div>'
        for r in rekomendasi_items
    )
    st.markdown(f'<div class="rekom-grid">{kartu_html}</div>', unsafe_allow_html=True)

st.markdown("")

# ── Halaman Metodologi ───────────────────────────────────────────
with st.container(border=True):
    utils.section_label("Metodologi", "Sumber Data, Keputusan, dan Keterbatasan")

    with st.expander("Sumber Data", expanded=True):
        st.markdown(f"""
- **Data Primer** — {config.SUMBER_PRIMER}. Level 38 kab/kota: TPT, TPAK, Upah, 17 sektor (provinsi saja).
- **Data Pendamping** — {config.SUMBER_PENDAMPING}. Level provinsi saja: tren makro, TPT menurut karakteristik, karakteristik pekerja.
- **Data Historis** — {config.SUMBER_API_BPS}.
""")

    st.caption(f"Dashboard diperbarui: {config.TANGGAL_UPDATE_DASHBOARD}")
