
import io

import pandas as pd
import streamlit as st

import config

def apply_style():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        /* Kunci paksa palet terang, apa pun preferensi dark-mode browser/OS
           pengguna — mengganti variabel CSS internal Streamlit langsung,
           sebagai lapisan cadangan selain .streamlit/config.toml. */
        :root, .stApp {{
            color-scheme: light !important;
            --text-color: {config.COLOR_INK} !important;
            --background-color: {config.COLOR_BG} !important;
            --secondary-background-color: {config.COLOR_BG_PAGE} !important;
        }}

        html, body, [class*="css"] {{
            font-family: {config.FONT_BODY};
            color: {config.COLOR_INK} !important;
        }}
        .stApp {{ background-color: {config.COLOR_BG_PAGE} !important; }}
        .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1240px; }}
        h1, h2, h3, h4 {{ font-family: {config.FONT_DISPLAY} !important; color: {config.COLOR_INK} !important; font-weight: 700; }}

        section[data-testid="stSidebar"] {{
            background-color: {config.COLOR_BG} !important;
            border-right: 1px solid {config.COLOR_BORDER};
        }}
        section[data-testid="stSidebar"] * {{ color: {config.COLOR_INK} !important; }}

        .sidebar-brand {{
            font-family: {config.FONT_DISPLAY}; font-weight: 800; font-size: 15px;
            line-height: 1.3; color: {config.COLOR_INK} !important;
            padding: 4px 0 16px 0; margin-bottom: 8px;
            border-bottom: 1px solid {config.COLOR_BORDER};
        }}

        /* Header sidebar: judul besar & bold, dengan panah kecil di sampingnya
           yang bisa diklik untuk membuka keterangan singkat dashboard. */
        details.sidebar-header-details {{
            padding: 4px 0 16px 0; margin-bottom: 10px;
            border-bottom: 1px solid {config.COLOR_BORDER};
        }}
        details.sidebar-header-details summary.sidebar-header-summary {{
            font-family: {config.FONT_DISPLAY}; font-weight: 800; font-size: 17px;
            line-height: 1.35; color: {config.COLOR_INK} !important;
            cursor: pointer; list-style: none; display: flex;
            align-items: center; justify-content: space-between; gap: 8px;
        }}
        details.sidebar-header-details summary.sidebar-header-summary::-webkit-details-marker {{
            display: none;
        }}
        details.sidebar-header-details summary.sidebar-header-summary::after {{
            content: '▾'; font-size: 13px; font-weight: 700; color: {config.COLOR_MUTED};
            transition: transform 0.15s ease; flex-shrink: 0;
        }}
        details.sidebar-header-details[open] summary.sidebar-header-summary::after {{
            transform: rotate(180deg);
        }}
        details.sidebar-header-details .sidebar-header-body {{
            margin-top: 10px; font-size: 12.5px; color: {config.COLOR_MUTED}; line-height: 1.5;
        }}
        details.sidebar-header-details .sidebar-header-body p {{ margin: 0 0 6px 0; }}
        details.sidebar-header-details .sidebar-header-body p:last-child {{ margin-bottom: 0; }}
        details.sidebar-header-details .sidebar-header-body strong {{ color: {config.COLOR_INK}; }}

        section[data-testid="stSidebar"] nav a {{
            border-radius: 10px !important;
            margin: 1px 0 !important;
            font-weight: 500 !important;
            transition: background-color 0.15s ease;
        }}
        section[data-testid="stSidebar"] nav a:hover {{
            background-color: {config.COLOR_BG_PAGE} !important;
        }}
        section[data-testid="stSidebar"] nav a[aria-current="page"] {{
            background-color: #EFF6FF !important;
            font-weight: 700 !important;
        }}
        section[data-testid="stSidebar"] nav a[aria-current="page"] * {{
            color: {config.COLOR_PRIMARY_DARK} !important;
        }}

        .page-eyebrow {{
            font-size: 12.5px; font-weight: 600; letter-spacing: 0.08em;
            text-transform: uppercase; color: {config.COLOR_PRIMARY}; margin-bottom: 6px;
        }}
        .page-title {{ font-size: 30px; font-weight: 800; color: {config.COLOR_INK}; line-height: 1.2; margin: 0; letter-spacing: -0.01em; }}
        .page-subtitle {{ font-size: 14.5px; color: {config.COLOR_MUTED}; margin-top: 4px; font-weight: 400; }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {config.COLOR_CARD};
            border: 1px solid {config.COLOR_BORDER} !important;
            border-radius: 14px !important;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05);
            padding: 20px 22px !important;
            margin-bottom: 18px;
            transition: box-shadow 0.18s ease, transform 0.18s ease;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            box-shadow: 0 8px 20px rgba(15,23,42,0.09);
            transform: translateY(-1px);
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {{
            box-shadow: none; margin-bottom: 0; transform: none;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            box-shadow: none; transform: none;
        }}

        div[data-testid="stMetric"] {{
            background-color: {config.COLOR_CARD};
            border: 1px solid {config.COLOR_BORDER};
            border-radius: 14px; padding: 22px 20px;
            overflow: visible; text-align: center;
            transition: box-shadow 0.18s ease, transform 0.18s ease;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05);
            min-height: 168px;
        }}
        div[data-testid="stMetric"]:hover {{
            box-shadow: 0 8px 20px rgba(15,23,42,0.09);
            transform: translateY(-1px);
        }}
        div[data-testid="stMetricLabel"] {{
            font-weight: 500; font-size: 13px; color: {config.COLOR_MUTED}; justify-content: center;
            white-space: normal !important; overflow: visible !important; text-overflow: unset !important;
            line-height: 1.35;
        }}
        div[data-testid="stMetricLabel"] p {{
            white-space: normal !important; overflow: visible !important; text-overflow: unset !important;
        }}
        div[data-testid="stMetricValue"] {{
            color: {config.COLOR_INK}; font-weight: 800; font-size: 1.9rem !important; justify-content: center;
            white-space: normal !important; overflow: visible !important; text-overflow: unset !important;
            word-break: break-word; line-height: 1.3;
        }}
        div[data-testid="stMetricValue"] > div {{
            white-space: normal !important; overflow: visible !important; text-overflow: unset !important;
        }}
        div[data-testid="stMetricDelta"] {{ justify-content: center; }}
        
        .stat-card {{
            background-color: {config.COLOR_CARD}; border: 1px solid {config.COLOR_BORDER};
            border-radius: 14px; padding: 22px 20px; text-align: center;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05);
            transition: box-shadow 0.18s ease, transform 0.18s ease;
            min-height: 168px;
            display: flex; flex-direction: column; justify-content: center;
        }}
        .stat-card:hover {{ box-shadow: 0 8px 20px rgba(15,23,42,0.09); transform: translateY(-1px); }}
        .stat-card-label {{ font-size: 13px; font-weight: 500; color: {config.COLOR_MUTED}; margin-bottom: 6px; }}
        .stat-card-value {{
            font-size: 1.9rem; font-weight: 800; color: {config.COLOR_INK};
            line-height: 1.25; word-wrap: break-word; white-space: normal;
        }}
        .stat-card-delta {{
            display: inline-flex; align-items: center; gap: 4px; align-self: center;
            margin-top: 8px; font-size: 13px; font-weight: 600;
            padding: 2px 9px; border-radius: 6px;
        }}
        .stat-card-delta::before {{ font-size: 10px; }}
        .stat-card-delta--up::before {{ content: '▲'; }}
        .stat-card-delta--down::before {{ content: '▼'; }}

        .section-label {{
            font-size: 11.5px; font-weight: 600; letter-spacing: 0.06em;
            text-transform: uppercase; color: {config.COLOR_PRIMARY}; margin-bottom: 2px;
        }}
        .section-title {{ font-size: 18px; font-weight: 700; color: {config.COLOR_INK}; margin: 0 0 2px 0; }}
        .section-desc {{ font-size: 13px; color: {config.COLOR_MUTED}; margin-bottom: 14px; }}

        .note-box {{
            background-color: #FFFBEB; border: 1px solid #FDE68A;
            border-left: 3px solid {config.COLOR_SECONDARY}; border-radius: 8px;
            padding: 10px 14px; font-size: 13.5px; color: {config.COLOR_INK}; margin: 4px 0 14px 0;
        }}
        .warning-box {{
            background-color: #FEF2F2; border: 1px solid #FECACA;
            border-left: 3px solid {config.COLOR_DANGER}; border-radius: 8px;
            padding: 10px 14px; font-size: 13.5px; color: {config.COLOR_INK}; margin: 4px 0 14px 0;
        }}

        hr {{ border-color: {config.COLOR_BORDER}; }}
        section[data-testid="stSidebar"] {{ background-color: {config.COLOR_CARD}; }}

        .scope-badge {{
            display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.03em;
            padding: 3px 9px; border-radius: 999px; margin-bottom: 8px;
        }}
        .scope-badge--kabkota {{ background-color: {config.BADGE_KABKOTA_BG}; border: 1px solid {config.BADGE_KABKOTA_BORDER}; color: {config.BADGE_KABKOTA_TEXT}; }}
        .scope-badge--provinsi {{ background-color: {config.BADGE_PROVINSI_BG}; border: 1px solid {config.BADGE_PROVINSI_BORDER}; color: {config.BADGE_PROVINSI_TEXT}; }}

        div[data-testid="stButton"] > button {{
            border-radius: 8px; border-color: {config.COLOR_BORDER}; color: {config.COLOR_INK};
            font-weight: 600; background-color: {config.COLOR_CARD};
        }}
        div[data-testid="stButton"] > button:hover {{ border-color: {config.COLOR_PRIMARY}; color: {config.COLOR_PRIMARY}; }}
        div[data-testid="stDownloadButton"] > button {{
            border-radius: 8px; border-color: {config.COLOR_BORDER}; color: {config.COLOR_MUTED};
            font-weight: 600; font-size: 12.5px; padding: 4px 12px; background-color: {config.COLOR_CARD};
        }}
        div[data-testid="stDownloadButton"] > button:hover {{ border-color: {config.COLOR_PRIMARY}; color: {config.COLOR_PRIMARY}; }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {config.COLOR_BORDER}; border-radius: 12px; overflow: hidden;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05);
        }}
        div[data-testid="stDataFrame"] [role="columnheader"] {{
            background-color: {config.COLOR_BG_PAGE} !important; color: {config.COLOR_MUTED} !important;
            font-weight: 700 !important; font-size: 12.5px !important; text-transform: uppercase;
            letter-spacing: 0.03em; border-bottom: 1px solid {config.COLOR_BORDER} !important;
        }}
        div[data-testid="stDataFrame"] [role="gridcell"] {{ font-size: 13.5px !important; color: {config.COLOR_INK} !important; }}

        .table-caption {{
            font-size: 13px; font-weight: 700; color: {config.COLOR_INK};
            margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
        }}
        .table-caption .dot {{ width: 7px; height: 7px; border-radius: 50%; display: inline-block; background-color: {config.COLOR_PRIMARY}; }}

        .tier-badge {{
            display: inline-block; font-size: 12px; font-weight: 700;
            padding: 3px 10px; border-radius: 999px; color: white;
        }}

        .df-table-wrap {{
            width: 100%; overflow-x: auto; overflow-y: auto;
            border: 1px solid {config.COLOR_BORDER}; border-radius: 12px;
            margin: 4px 0 10px 0;
        }}
        table.df-table {{
            width: 100%; border-collapse: collapse; font-size: 13.5px;
            table-layout: auto;
        }}
        table.df-table thead th {{
            position: sticky; top: 0; z-index: 1;
            background-color: {config.COLOR_BG_PAGE};
            color: {config.COLOR_MUTED}; font-weight: 600; font-size: 12px;
            text-transform: uppercase; letter-spacing: 0.03em;
            text-align: center; padding: 10px 12px;
            border-bottom: 1px solid {config.COLOR_BORDER};
            white-space: nowrap;
        }}
        table.df-table tbody td {{
            padding: 9px 12px; color: {config.COLOR_INK};
            border-bottom: 1px solid {config.COLOR_BORDER};
            white-space: nowrap;
        }}
        table.df-table td.align-kanan {{ text-align: right; font-variant-numeric: tabular-nums; }}
        table.df-table td.align-kiri {{ text-align: left; white-space: normal; min-width: 90px; }}
        table.df-table td.align-tengah {{ text-align: center; }}
        table.df-table tbody tr:last-child td {{ border-bottom: none; }}
        table.df-table tbody tr:nth-child(even) {{ background-color: #FAFBFC; }}
        table.df-table tbody tr:hover {{ background-color: #EFF6FF; }}

        .rekom-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 6px;
        }}
        .rekom-card {{
            border-radius: 14px; padding: 16px 18px; background-color: {config.COLOR_CARD};
            border: 1px solid {config.COLOR_BORDER}; border-left: 4px solid {config.COLOR_MUTED};
            box-shadow: 0 1px 3px rgba(15,23,42,0.05);
            transition: box-shadow 0.18s ease, transform 0.18s ease;
        }}
        .rekom-card:hover {{ box-shadow: 0 10px 22px rgba(15,23,42,0.10); transform: translateY(-2px); }}
        .rekom-card-top {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
        .rekom-card-glyph {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 22px; height: 22px; border-radius: 999px; font-size: 12px; font-weight: 800;
            color: #fff; flex-shrink: 0;
        }}
        .rekom-card-tag {{
            font-size: 11px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
        }}
        .rekom-card-judul {{ font-size: 14.5px; font-weight: 700; color: {config.COLOR_INK}; margin-bottom: 6px; line-height: 1.35; }}
        .rekom-card-isi {{ font-size: 13.5px; color: {config.COLOR_MUTED}; line-height: 1.55; }}
        .rekom-card-isi strong {{ color: {config.COLOR_INK}; }}

        .rekom-card--danger {{ border-left-color: {config.COLOR_DANGER}; }}
        .rekom-card--danger .rekom-card-glyph {{ background-color: {config.COLOR_DANGER}; }}
        .rekom-card--danger .rekom-card-tag {{ color: {config.COLOR_DANGER}; }}

        .rekom-card--warning {{ border-left-color: {config.COLOR_SECONDARY}; }}
        .rekom-card--warning .rekom-card-glyph {{ background-color: {config.COLOR_SECONDARY}; }}
        .rekom-card--warning .rekom-card-tag {{ color: #B45309; }}

        .rekom-card--primary {{ border-left-color: {config.COLOR_PRIMARY}; }}
        .rekom-card--primary .rekom-card-glyph {{ background-color: {config.COLOR_PRIMARY}; }}
        .rekom-card--primary .rekom-card-tag {{ color: {config.COLOR_PRIMARY}; }}

        .rekom-card--muted {{ border-left-color: {config.COLOR_MUTED}; }}
        .rekom-card--muted .rekom-card-glyph {{ background-color: {config.COLOR_MUTED}; }}
        .rekom-card--muted .rekom-card-tag {{ color: {config.COLOR_MUTED}; }}

        @media (max-width: 900px) {{
            .rekom-grid {{ grid-template-columns: 1fr; }}
        }}

        div[data-testid="stHorizontalBlock"] {{ align-items: stretch; }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
            display: flex; flex-direction: column;
        }}
        div[data-testid="column"] > div {{ height: 100%; }}
        a[data-testid="stPageLink"] {{
            font-size: 13px !important; font-weight: 600 !important;
            color: {config.COLOR_PRIMARY} !important; margin-top: 6px;
        }}
        a[data-testid="stPageLink"]:hover {{ color: {config.COLOR_PRIMARY_DARK} !important; }}

        .nav-card {{ display: flex; align-items: baseline; gap: 10px; margin-bottom: 2px; }}
        .nav-card-no {{
            font-family: {config.FONT_DISPLAY}; font-size: 12px; font-weight: 800;
            color: {config.COLOR_PRIMARY}; letter-spacing: 0.02em;
        }}
        .nav-card-title {{ font-size: 15px; font-weight: 700; color: {config.COLOR_INK}; }}

        div[data-testid="stVerticalBlockBorderWrapper"]:has(a[data-testid="stPageLink"]) {{
            position: relative;
            min-height: 116px;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(a[data-testid="stPageLink"]) a[data-testid="stPageLink"] {{
            position: absolute; inset: 0; margin: 0; padding: 0;
            font-size: 0 !important; opacity: 0; z-index: 5;
        }}
        .nav-card-metric {{ text-align: center; padding: 4px 0 2px 0; }}
        .nav-card-label {{
            font-size: 13px; font-weight: 500; color: {config.COLOR_MUTED}; margin-bottom: 6px;
        }}
        .nav-card-value {{
            font-size: 1.35rem; font-weight: 800; color: {config.COLOR_INK}; line-height: 1.3;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"]:has(a[data-testid="stPageLink"]) {{
            position: relative;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(a[data-testid="stPageLink"]) a[data-testid="stPageLink"] {{
            position: absolute; inset: 0; margin: 0; padding: 0;
            font-size: 0 !important; opacity: 0; z-index: 5;
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            display: flex !important;
            flex-direction: column !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stSidebarNav"],
        section[data-testid="stSidebar"] nav[data-testid="stSidebarNav"],
        section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"],
        section[data-testid="stSidebar"] nav {{
            order: 2 !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]:has(.sidebar-header-details) {{
            order: 1 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def page_header(eyebrow: str, title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="page-eyebrow">{eyebrow}</div>
        <p class="page-title">{title}</p>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")

def section_label(label: str, title: str, desc: str = None) -> None:
    st.markdown(
        f"""
        <div class="section-label">{label}</div>
        <div class="section-title">{title}</div>
        {f'<div class="section-desc">{desc}</div>' if desc else ''}
        """,
        unsafe_allow_html=True,
    )

def judul_tabel(teks: str) -> None:
    st.markdown(f'<div class="table-caption"><span class="dot"></span>{teks}</div>', unsafe_allow_html=True)

def tombol_unduh_csv(df: pd.DataFrame, nama_file: str, label: str = "Unduh CSV", key: str = None) -> None:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    st.download_button(label=label, data="\ufeff" + buffer.getvalue(), file_name=nama_file, mime="text/csv", key=key)

def _format_nilai(v, jenis: str) -> str:
    if pd.isna(v):
        return ""
    if isinstance(v, (bool,)):
        return "Ya" if v else "Tidak"
    if jenis == "persen":
        return f"{v:,.2f}%"
    if jenis == "rupiah":
        return "Rp " + f"{v:,.0f}".replace(",", ".")
    if jenis == "angka":
        if float(v).is_integer():
            return f"{v:,.0f}".replace(",", ".")
        return f"{v:,.2f}"
    return str(v)

def tabel_rapi(df: pd.DataFrame, kolom: list = None, height: int = None) -> None:
    import html as _html

    tampil = [c for c in (kolom or df.columns) if c not in config.KOLOM_TERSEMBUNYI]
    df_tampil = df[tampil].copy()

    thead = "<tr>" + "".join(
        f'<th>{_html.escape(config.LABEL_KOLOM.get(k, k))}</th>' for k in tampil
    ) + "</tr>"

    baris = []
    for _, row in df_tampil.iterrows():
        sel = []
        for k in tampil:
            jenis = config.FORMAT_KOLOM.get(k, "teks")
            if k == "tier_risiko":
                sel.append(f'<td class="align-tengah">{tier_badge_html(row[k])}</td>')
                continue
            nilai = _format_nilai(row[k], jenis)
            align = "align-kanan" if jenis in ("persen", "rupiah", "angka") else "align-kiri"
            sel.append(f'<td class="{align}">{_html.escape(nilai)}</td>')
        baris.append("<tr>" + "".join(sel) + "</tr>")

    style_scroll = f'style="max-height:{height}px;"' if height else ""
    st.markdown(
        f'<div class="df-table-wrap" {style_scroll}>'
        f'<table class="df-table"><thead>{thead}</thead><tbody>{"".join(baris)}</tbody></table>'
        f'</div>',
        unsafe_allow_html=True,
    )

def metric_like(label: str, value: str, delta: str = None, delta_positif: bool = True,
                 help_text: str = None, value_font_size: str = "1.9rem") -> None:
    delta_html = ""
    if delta:
        warna = config.COLOR_SUCCESS if delta_positif else config.COLOR_DANGER
        bg = "#F0FDF4" if delta_positif else "#FEF2F2"
        arah = "up" if delta_positif else "down"
        delta_html = (
            f'<div class="stat-card-delta stat-card-delta--{arah}" '
            f'style="color:{warna};background-color:{bg};">{delta}</div>'
        )
    title_attr = f' title="{help_text}"' if help_text else ""
    st.markdown(
        f'<div class="stat-card"{title_attr}>'
        f'<div class="stat-card-label">{label}</div>'
        f'<div class="stat-card-value" style="font-size:{value_font_size};">{value}</div>'
        f'{delta_html}</div>',
        unsafe_allow_html=True,
    )

def stat_card(label: str, value: str, delta: str = None, delta_positif: bool = True, help_text: str = None) -> None:
    delta_html = ""
    if delta:
        warna = config.COLOR_SUCCESS if delta_positif else config.COLOR_DANGER
        bg = "#F0FDF4" if delta_positif else "#FEF2F2"
        arah = "up" if delta_positif else "down"
        delta_html = (
            f'<div class="stat-card-delta stat-card-delta--{arah}" '
            f'style="color:{warna};background-color:{bg};">{delta}</div>'
        )
    title_attr = f' title="{help_text}"' if help_text else ""
    st.markdown(
        f'<div class="stat-card"{title_attr}>'
        f'<div class="stat-card-label">{label}</div>'
        f'<div class="stat-card-value">{value}</div>'
        f'{delta_html}</div>',
        unsafe_allow_html=True,
    )

def flatten_koordinat(coords):
    if coords and isinstance(coords[0], (int, float)):
        yield (coords[0], coords[1])
    else:
        for sub in coords:
            yield from flatten_koordinat(sub)

def tier_badge_html(tier: str) -> str:
    warna = config.TIER_RISIKO_WARNA.get(tier, config.COLOR_MUTED)
    return f'<span class="tier-badge" style="background-color:{warna}">{tier}</span>'

def guard_data_loaded():
    if "data" not in st.session_state:
        st.warning("Silakan buka halaman **Home** terlebih dahulu agar data termuat ke sesi ini.")
        st.stop()
    return st.session_state["data"]