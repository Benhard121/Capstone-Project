"""
=============================================================================
  Platform Analisis Sentimen Berita Ekonomi — CC26-PSU386
  Capstone Project: Big Bank Sentiment & Investment Signal Dashboard
  Theme: Ocean Bright
=============================================================================
Jalankan dengan:
    streamlit run dashboard.py
"""

# ─── Imports ──────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentiVest | Big Bank Sentiment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Color Palette — Ocean Bright ─────────────────────────────────────────────
C_GREEN  = "#00B894"
C_RED    = "#D63031"
C_GREY   = "#636E72"
C_BLUE   = "#0984E3"
C_BG     = "#F0F7FF"
C_CARD   = "#FFFFFF"
C_BORDER = "#BDE0FE"
C_TEXT   = "#1A2E4A"
C_MUTED  = "#5A7FA8"
C_YELLOW = "#F9A825"


def rgba(hex_color, alpha):
    """Convert hex + alpha to rgba() string safe for Plotly."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
    background-color: {C_BG};
    color: {C_TEXT};
}}
section[data-testid="stSidebar"] {{
    background: #DDEEFF !important;
    border-right: 2px solid {C_BORDER};
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 1.5rem; }}
.block-container {{
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1400px !important;
}}
.kpi-card {{
    background: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 12px rgba(9,132,227,0.08);
}}
.kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(9,132,227,0.15); }}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), transparent);
}}
.kpi-label {{
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: {C_MUTED}; margin-bottom: 0.4rem;
}}
.kpi-value {{
    font-size: 1.8rem; font-weight: 700; line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
}}
.kpi-sub {{ font-size: 0.78rem; color: {C_MUTED}; margin-top: 0.3rem; }}
.section-header {{
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: {C_MUTED};
    border-bottom: 1.5px solid {C_BORDER};
    padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;
}}
.stSelectbox label, .stMultiSelect label, .stDateInput label, .stSlider label {{
    color: {C_MUTED} !important; font-size: 0.75rem !important;
    font-weight: 600 !important; letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}}
div[data-baseweb="select"] > div {{
    background: #EAF4FF !important; border-color: {C_BORDER} !important;
    border-radius: 8px !important; color: {C_TEXT} !important;
}}
.stDateInput input {{
    background: #EAF4FF !important; border-color: {C_BORDER} !important;
    color: {C_TEXT} !important; border-radius: 8px !important;
}}
hr {{ border-color: {C_BORDER} !important; }}
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {C_BG}; }}
::-webkit-scrollbar-thumb {{ background: {C_BORDER}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ─── Plotly helpers ───────────────────────────────────────────────────────────
AXIS_STYLE = dict(gridcolor="#D6EAFF", linecolor=C_BORDER,
                  tickcolor=C_BORDER, zerolinecolor=C_BORDER)
CHART_CFG  = {"displayModeBar": False}


def base_layout(height=400, title="", showlegend=True):
    """Return a clean Plotly layout dict — no xaxis/yaxis/legend keys included
    so callers can set them freely without duplicate-key conflicts."""
    return dict(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#F8FBFF",
        font=dict(family="Space Grotesk, sans-serif", color=C_TEXT, size=12),
        height=height,
        title=dict(text=title, font=dict(size=14, color=C_TEXT)) if title else None,
        showlegend=showlegend,
        margin=dict(l=10, r=10, t=40 if title else 20, b=10),
        hoverlabel=dict(bgcolor=C_CARD, bordercolor=C_BORDER, font_color=C_TEXT),
    )


# ─── Load & Preprocess ────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("output/final_dataset.csv")
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], dayfirst=False, errors="coerce")
    df = df.dropna(subset=["Tanggal"]).sort_values("Tanggal").reset_index(drop=True)

    def kat(v):
        if v > 0.05:    return "Positif"
        elif v < -0.05: return "Negatif"
        return "Netral"

    df["Kategori_Sentimen"] = df["Nilai_Sentimen"].apply(kat)
    df["MA5_Sentimen"] = (
        df.groupby("Ticker")["Nilai_Sentimen"]
          .transform(lambda x: x.rolling(5, min_periods=1).mean())
    )
    return df


def sinyal(ma5):
    if ma5 > 0.05:  return "BUY",  C_GREEN,  "▲"
    if ma5 < -0.05: return "SELL", C_RED,    "▼"
    return "HOLD", C_YELLOW, "◆"


def fmt_price(v):
    try:    return f"Rp {float(v):,.0f}"
    except: return "—"


def fmt_val(v, d=4):
    try:    return f"{float(v):+.{d}f}"
    except: return "—"


# ─── Data ─────────────────────────────────────────────────────────────────────
with st.spinner("Memuat data…"):
    df_raw = load_data()

TICKERS  = sorted(df_raw["Ticker"].dropna().unique())
MIN_DATE = df_raw["Tanggal"].min().date()
MAX_DATE = df_raw["Tanggal"].max().date()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='margin-bottom:1.5rem'>
        <div style='font-size:1.4rem;font-weight:700;color:{C_TEXT};'>📊 SentiVest</div>
        <div style='font-size:0.72rem;color:{C_MUTED};letter-spacing:0.1em;text-transform:uppercase;'>
            Big Bank Sentiment Intelligence
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    sel_ticker = st.selectbox("Ticker Saham", TICKERS,
                              index=list(TICKERS).index("BBCA.JK") if "BBCA.JK" in TICKERS else 0)
    d_from = st.date_input("Dari Tanggal", value=MAX_DATE - timedelta(days=90),
                           min_value=MIN_DATE, max_value=MAX_DATE)
    d_to   = st.date_input("Sampai Tanggal", value=MAX_DATE,
                           min_value=MIN_DATE, max_value=MAX_DATE)
    sel_sent = st.selectbox("Kategori Sentimen", ["Semua", "Positif", "Netral", "Negatif"])
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.7rem;color:{C_MUTED};'>Data: {MIN_DATE} – {MAX_DATE}</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.7rem;color:{C_MUTED};'>CC26-PSU386 · Capstone Project</div>",
                unsafe_allow_html=True)

# ─── Filtered datasets ────────────────────────────────────────────────────────
mask = (
    (df_raw["Ticker"] == sel_ticker) &
    (df_raw["Tanggal"].dt.date >= d_from) &
    (df_raw["Tanggal"].dt.date <= d_to)
)
if sel_sent != "Semua":
    mask &= df_raw["Kategori_Sentimen"] == sel_sent
df = df_raw[mask].copy()

df_all = df_raw[
    (df_raw["Tanggal"].dt.date >= d_from) &
    (df_raw["Tanggal"].dt.date <= d_to)
].copy()

df_tk = df_raw[df_raw["Ticker"] == sel_ticker].sort_values("Tanggal")

# ─── KPI values ───────────────────────────────────────────────────────────────
ma5_now    = float(df_tk["MA5_Sentimen"].iloc[-1])          if len(df_tk) else 0.0
last_price = float(df_tk["Harga_Penutupan_Saham"].iloc[-1]) if len(df_tk) else np.nan
total_news = len(df)
sig_lbl, sig_clr, sig_ico = sinyal(ma5_now)

if len(df):
    vc = df["Target_Label"].value_counts()
    dom_lbl, dom_pct = vc.idxmax(), vc.max() / vc.sum() * 100
else:
    dom_lbl, dom_pct = "—", 0.0

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;'>
    <div>
        <div style='font-size:1.6rem;font-weight:700;letter-spacing:-0.03em;color:{C_TEXT};'>
            {sel_ticker}
            <span style='color:{C_MUTED};font-weight:400;font-size:1rem;'>
                &nbsp;· Analisis Sentimen Berita
            </span>
        </div>
        <div style='font-size:0.8rem;color:{C_MUTED};margin-top:0.2rem;'>
            {d_from.strftime("%d %b %Y")} — {d_to.strftime("%d %b %Y")}
            &nbsp;·&nbsp; {total_news} berita dimuat
        </div>
    </div>
    <div style='text-align:right;'>
        <div style='font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
                    text-transform:uppercase;color:{C_MUTED};margin-bottom:0.3rem;'>
            Sinyal Rekomendasi
        </div>
        <div style='display:inline-flex;align-items:center;gap:0.6rem;
                    padding:0.6rem 1.4rem;border-radius:50px;font-size:1rem;
                    font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                    background:{rgba(sig_clr, 0.12)};color:{sig_clr};
                    border:1.5px solid {rgba(sig_clr, 0.3)};'>
            {sig_ico}&nbsp;{sig_lbl}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Cards ────────────────────────────────────────────────────────────────
def kpi(col, label, value, sub, accent):
    col.markdown(f"""
    <style>.kpi-card{{--accent:{accent};}}</style>
    <div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value' style='color:{accent};'>{value}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)


c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Harga Penutupan", fmt_price(last_price), "Harga terakhir tersedia", C_BLUE)
kpi(c2, "MA5 Sentimen",    fmt_val(ma5_now),      "Rata-rata 5 hari terakhir", sig_clr)
kpi(c3, "Total Berita",    f"{total_news:,}",     f"Periode · {sel_sent}", C_GREY)
kpi(c4, "Dominasi Label",  str(dom_lbl),          f"{dom_pct:.1f}% dari total data", C_YELLOW)

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Harga vs Sentimen 30 hari
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>① Harga Penutupan vs Sentimen Harian (30 Hari Terakhir)</div>",
            unsafe_allow_html=True)

df_30 = df_tk[df_tk["Tanggal"].dt.date >= (MAX_DATE - timedelta(days=30))].copy()

if len(df_30) >= 2:
    fig1 = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.65, 0.35], vertical_spacing=0.06,
        subplot_titles=["Harga Penutupan (IDR)", "Sentimen Harian & MA5"],
    )
    fig1.add_trace(go.Scatter(
        x=df_30["Tanggal"], y=df_30["Harga_Penutupan_Saham"],
        name="Harga Penutupan",
        line=dict(color=C_BLUE, width=2),
        fill="tozeroy", fillcolor=rgba(C_BLUE, 0.10),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Harga: Rp %{y:,.0f}<extra></extra>",
    ), row=1, col=1)

    bar_colors = [C_GREEN if v > 0.05 else (C_RED if v < -0.05 else C_GREY)
                  for v in df_30["Nilai_Sentimen"]]
    fig1.add_trace(go.Bar(
        x=df_30["Tanggal"], y=df_30["Nilai_Sentimen"],
        name="Sentimen Harian", marker_color=bar_colors, opacity=0.7,
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sentimen: %{y:.4f}<extra></extra>",
    ), row=2, col=1)

    fig1.add_trace(go.Scatter(
        x=df_30["Tanggal"], y=df_30["MA5_Sentimen"],
        name="MA5 Sentimen",
        line=dict(color=C_YELLOW, width=2, dash="dash"),
        hovertemplate="MA5: %{y:.4f}<extra></extra>",
    ), row=2, col=1)

    fig1.add_hline(y=0.05,  line_dash="dot", line_color=rgba(C_GREEN, 0.6),
                   annotation_text="BUY zone",  annotation_font_color=C_GREEN,
                   annotation_position="bottom right", row=2, col=1)
    fig1.add_hline(y=-0.05, line_dash="dot", line_color=rgba(C_RED, 0.6),
                   annotation_text="SELL zone", annotation_font_color=C_RED,
                   annotation_position="top right", row=2, col=1)

    fig1.update_layout(
        **base_layout(height=480, showlegend=True),
        legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor=C_BORDER, borderwidth=1),
    )
    fig1.update_xaxes(**AXIS_STYLE)
    fig1.update_yaxes(**AXIS_STYLE)
    fig1.update_yaxes(tickprefix="Rp ", tickformat=",.0f", row=1, col=1)
    st.plotly_chart(fig1, width="stretch", config=CHART_CFG)
else:
    st.info("Data tidak cukup. Perluas rentang tanggal.")

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Distribusi Sentimen  +  Volume
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>② Distribusi Sentimen  &amp;  ⑤ Volume Perdagangan</div>",
            unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    if len(df):
        sc = df["Kategori_Sentimen"].value_counts()
        labels = sc.index.tolist()
        values = sc.values.tolist()
        clr_map = {"Positif": C_GREEN, "Netral": C_GREY, "Negatif": C_RED}
        colors  = [clr_map.get(l, C_BLUE) for l in labels]

        fig2 = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors, line=dict(color=C_BG, width=2)),
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(color=C_TEXT, size=12),
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>%{percent}<extra></extra>",
        ))
        fig2.add_annotation(
            text=f"<b>{sum(values)}</b><br>Berita",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=C_TEXT), align="center",
        )
        fig2.update_layout(
            **base_layout(height=340, title="Distribusi Kategori Sentimen", showlegend=True),
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor=C_BORDER, borderwidth=1),
        )
        st.plotly_chart(fig2, width="stretch", config=CHART_CFG)
    else:
        st.info("Tidak ada data.")

with col_b:
    if len(df_30) >= 2:
        fig5 = go.Figure(go.Bar(
            x=df_30["Tanggal"], y=df_30["Volume"],
            name="Volume",
            marker=dict(
                color=df_30["Nilai_Sentimen"],
                colorscale=[[0, C_RED], [0.5, C_GREY], [1, C_GREEN]],
                colorbar=dict(title="Sentimen", thickness=10, len=0.7),
            ),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Volume: %{y:,.0f}<extra></extra>",
        ))
        fig5.update_layout(
            **base_layout(height=340, title="Volume Perdagangan (30 Hari)", showlegend=False),
            xaxis=dict(**AXIS_STYLE),
            yaxis=dict(**AXIS_STYLE, tickformat=".2s"),
        )
        st.plotly_chart(fig5, width="stretch", config=CHART_CFG)
    else:
        st.info("Data volume tidak cukup.")

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Berita Positif per Ticker  +  Target Label per Sentimen
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>③ Berita Positif per Ticker (2026)  &amp;  ④ Proporsi Target Label per Sentimen</div>",
    unsafe_allow_html=True)
col_c, col_d = st.columns(2)

with col_c:
    df_2026  = df_raw[df_raw["Tanggal"].dt.year == 2026].copy()
    df_pos26 = df_2026[df_2026["Kategori_Sentimen"] == "Positif"]

    if len(df_pos26):
        pos_cnt = (df_pos26.groupby("Ticker").size()
                           .reset_index(name="Jumlah_Berita_Positif")
                           .sort_values("Jumlah_Berita_Positif", ascending=True))
        avg_px  = (df_2026.groupby("Ticker")["Harga_Penutupan_Saham"]
                          .mean().reset_index(name="Avg_Harga"))
        pos_cnt = pos_cnt.merge(avg_px, on="Ticker", how="left")

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Bar(
            x=pos_cnt["Jumlah_Berita_Positif"], y=pos_cnt["Ticker"],
            orientation="h", name="Berita Positif",
            marker_color=C_GREEN, opacity=0.85,
            hovertemplate="<b>%{y}</b><br>Berita Positif: %{x}<extra></extra>",
        ), secondary_y=False)
        fig3.add_trace(go.Scatter(
            x=pos_cnt["Avg_Harga"], y=pos_cnt["Ticker"],
            mode="markers", name="Rata-rata Harga 2026",
            marker=dict(symbol="diamond", size=12, color=C_BLUE,
                        line=dict(color=C_TEXT, width=1)),
            hovertemplate="<b>%{y}</b><br>Avg Harga: Rp %{x:,.0f}<extra></extra>",
        ), secondary_y=True)

        fig3.update_layout(
            **base_layout(height=340, title="Berita Positif & Rata-rata Harga (2026)"),
            legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor=C_BORDER, borderwidth=1),
            xaxis=dict(**AXIS_STYLE),
            yaxis=dict(**AXIS_STYLE),
        )
        fig3.update_yaxes(tickprefix="Rp ", secondary_y=True, **AXIS_STYLE)
        st.plotly_chart(fig3, width="stretch", config=CHART_CFG)
    else:
        st.info("Tidak ada data berita positif 2026.")

with col_d:
    if len(df_all) and "Target_Label" in df_all.columns:
        pivot = (df_all.groupby(["Kategori_Sentimen", "Target_Label"])
                       .size().reset_index(name="Count"))
        pivot["Pct"] = (pivot["Count"] /
                        pivot.groupby("Kategori_Sentimen")["Count"].transform("sum") * 100)

        target_labels = sorted(pivot["Target_Label"].unique().tolist())
        pal     = [C_GREEN, C_RED, C_GREY, C_BLUE, C_YELLOW]
        t_clrs  = {t: pal[i % len(pal)] for i, t in enumerate(target_labels)}
        kat_ord = ["Negatif", "Netral", "Positif"]

        fig4 = go.Figure()
        for tl in target_labels:
            sub = (pivot[pivot["Target_Label"] == tl]
                   .set_index("Kategori_Sentimen")
                   .reindex(kat_ord).reset_index())
            fig4.add_trace(go.Bar(
                x=sub["Kategori_Sentimen"], y=sub["Pct"],
                name=str(tl),
                marker_color=t_clrs.get(tl, C_GREY),
                hovertemplate=f"<b>Sentimen: %{{x}}</b><br>Target: {tl}<br>%{{y:.1f}}%<extra></extra>",
            ))

        fig4.update_layout(
            **base_layout(height=340, title="Proporsi Target Label per Kategori Sentimen"),
            barmode="stack",
            legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor=C_BORDER, borderwidth=1),
            xaxis=dict(**AXIS_STYLE, categoryorder="array", categoryarray=kat_ord),
            yaxis=dict(**AXIS_STYLE, ticksuffix="%", range=[0, 105]),
        )
        st.plotly_chart(fig4, width="stretch", config=CHART_CFG)
    else:
        st.info("Data Target_Label tidak tersedia.")

# ══════════════════════════════════════════════════════════════════════════════
# SINYAL per Ticker
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>① Sinyal Rekomendasi — Semua Ticker</div>",
            unsafe_allow_html=True)

sig_cols = st.columns(len(TICKERS))
for i, tk in enumerate(TICKERS):
    df_tk_i = df_raw[df_raw["Ticker"] == tk].sort_values("Tanggal")
    ma5_i   = float(df_tk_i["MA5_Sentimen"].iloc[-1]) if len(df_tk_i) else 0.0
    lbl_i, clr_i, ico_i = sinyal(ma5_i)
    px_i = float(df_tk_i["Harga_Penutupan_Saham"].iloc[-1]) if len(df_tk_i) else np.nan
    with sig_cols[i]:
        st.markdown(f"""
        <div class='kpi-card' style='--accent:{clr_i};text-align:center;'>
            <div class='kpi-label'>{tk}</div>
            <div style='font-size:1.5rem;font-weight:700;color:{clr_i};margin:0.3rem 0;'>
                {ico_i}&nbsp;{lbl_i}
            </div>
            <div style='font-family:"JetBrains Mono",monospace;font-size:0.85rem;color:{C_MUTED};'>
                MA5: {ma5_i:+.4f}
            </div>
            <div style='font-size:0.8rem;color:{C_MUTED};margin-top:0.2rem;'>
                Rp {px_i:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABEL BERITA TERBARU
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>⑥ Berita Terbaru</div>", unsafe_allow_html=True)

df_news = df.sort_values("Tanggal", ascending=False).head(15)
kat_clr = {"Positif": C_GREEN, "Negatif": C_RED, "Netral": C_GREY}

if len(df_news):
    for _, row in df_news.iterrows():
        kat   = row.get("Kategori_Sentimen", "Netral")
        warna = kat_clr.get(kat, C_GREY)
        teks  = str(row.get("Teks_Berita", ""))
        teks  = teks[:120] + "…" if len(teks) > 120 else teks
        sent  = float(row.get("Nilai_Sentimen", 0))
        tgl   = row["Tanggal"].strftime("%d %b %Y") if pd.notnull(row["Tanggal"]) else "—"

        st.markdown(f"""
        <div style='background:{C_CARD};border:1.5px solid {C_BORDER};
                    border-left:4px solid {warna};border-radius:10px;
                    padding:0.75rem 1rem;margin-bottom:0.45rem;
                    display:flex;gap:1rem;align-items:flex-start;
                    box-shadow:0 1px 6px rgba(9,132,227,0.07);'>
            <div style='min-width:82px;font-size:0.72rem;color:{C_MUTED};padding-top:2px;'>{tgl}</div>
            <div style='flex:1;font-size:0.84rem;line-height:1.4;color:{C_TEXT};'>{teks}</div>
            <div style='min-width:70px;text-align:right;'>
                <span style='background:{rgba(warna,0.12)};color:{warna};border-radius:6px;
                             padding:2px 8px;font-size:0.75rem;font-weight:600;'>{kat}</span>
                <div style='font-family:"JetBrains Mono",monospace;font-size:0.72rem;
                            color:{C_MUTED};margin-top:3px;'>{sent:+.4f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Tidak ada berita untuk filter yang dipilih.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-top:3rem;padding-top:1rem;border-top:1.5px solid {C_BORDER};
            display:flex;justify-content:space-between;align-items:center;
            font-size:0.72rem;color:{C_MUTED};'>
    <div>SentiVest · Platform Analisis Sentimen Berita Ekonomi</div>
    <div>Capstone Project CC26-PSU386 · {datetime.now().strftime("%d %B %Y")}</div>
</div>
""", unsafe_allow_html=True)
