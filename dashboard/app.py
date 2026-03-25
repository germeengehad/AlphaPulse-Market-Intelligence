# # /app/dashboard/app.py
# import streamlit as st
# import plotly.express as px
# import pandas as pd
# from data_prep import load_and_process_all
# from model import train_model, predict_latest
# from backtest import run_backtest

# # =========================
# # Load & cache processed data
# # =========================
# @st.cache_data
# def get_featured_data():
#     return load_and_process_all()

# df_all, df_1d, df_1h, df_15m = get_featured_data()

# # =========================
# # Load & cache model
# # =========================
# @st.cache_data
# def get_model(df):
#     return train_model(df)

# model, features = get_model(df_all)

# # =========================
# # Symbol explanations
# # =========================
# symbol_names = {
#     "^GSPC": "S&P 500 Index – Tracks 500 largest US companies, broad market benchmark",
#     "^DJI": "Dow Jones Industrial Average – Tracks 30 large, influential US companies",
#     "^IXIC": "NASDAQ Composite – Tech-heavy index of ~3,000 NASDAQ stocks",
#     "^TNX": "10-Year US Treasury Yield – Shows bond market trends, interest rate benchmark",
#     "^VIX": "CBOE Volatility Index – Measures expected market volatility, aka 'fear index'"
# }

# # =========================
# # Page layout
# # =========================
# st.set_page_config(
#     page_title="📊 Multi-Symbol Market Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.title("📊 Multi-Symbol Market Dashboard")

# # =========================
# # Sidebar: Select Symbol First
# # =========================
# st.sidebar.header("Select Index / Symbol")
# selected_symbol = st.sidebar.selectbox(
#     "Choose Index",
#     df_1d['symbol'].unique(),
#     format_func=lambda x: symbol_names.get(x, x)
# )

# st.sidebar.markdown("---")
# st.sidebar.header("Symbols & Metrics Explained")
# for sym, desc in symbol_names.items():
#     st.sidebar.markdown(f"**{sym}**: {desc}")

# # =========================
# # Sparkline helper
# # =========================
# def plot_sparkline(series, color="blue"):
#     fig = px.line(series, height=60)
#     fig.update_traces(line_color=color, line_width=2)
#     fig.update_layout(
#         xaxis=dict(showgrid=False, visible=False),
#         yaxis=dict(showgrid=False, visible=False),
#         margin=dict(l=0, r=0, t=0, b=0)
#     )
#     return fig

# # =========================
# # Trend / Regime icons
# # =========================
# def trend_icon(trend_value):
#     return ("⬆️", "green") if trend_value == 1 else ("⬇️", "red")

# def regime_icon(regime):
#     if regime.lower() == "bull":
#         return "⬆️", "green"
#     elif regime.lower() == "bear":
#         return "⬇️", "red"
#     else:
#         return "➡️", "gray"

# # =========================
# # Display Summary for Selected Symbol
# # =========================
# st.subheader(f"📌 Overview – {symbol_names.get(selected_symbol, selected_symbol)}")

# df_sym = df_1d[df_1d['symbol'] == selected_symbol]
# last_day = df_sym.iloc[-1]

# trend_ic, trend_color = trend_icon(last_day['trend'])
# regime_ic, regime_color = regime_icon(last_day['regime'])

# st.metric("Close", f"{last_day['close']:.2f}")
# st.metric("Daily Return", f"{last_day['daily_return']:.4f}")
# st.markdown(f"<h4 style='color:{trend_color}'>{trend_ic} Trend</h4>", unsafe_allow_html=True)
# st.markdown(f"<h4 style='color:{regime_color}'>{regime_ic} Regime</h4>", unsafe_allow_html=True)
# st.plotly_chart(plot_sparkline(df_sym['close'].tail(30)), use_container_width=True)
# st.plotly_chart(plot_sparkline(df_sym['daily_return'].tail(30), color="orange"), use_container_width=True)

# # =========================
# # Detailed View
# # =========================
# st.subheader(f"📈 Detailed Analysis – {symbol_names.get(selected_symbol, selected_symbol)}")

# fig_ma = px.line(df_sym, x='ts', y=['MA_7', 'MA_30'], title="MA7 vs MA30")
# st.plotly_chart(fig_ma, use_container_width=True)

# fig_vol = px.line(df_sym, x='ts', y='daily_volatility', title="Daily Volatility")
# st.plotly_chart(fig_vol, use_container_width=True)

# if st.checkbox("Show 1H Data"):
#     df_hour = df_1h[df_1h['symbol'] == selected_symbol]
#     fig_hr = px.line(df_hour, x='ts', y='hourly_mean', title="Hourly Mean Price")
#     st.plotly_chart(fig_hr, use_container_width=True)

# if st.checkbox("Show 15min Data"):
#     df_min15 = df_15m[df_15m['symbol'] == selected_symbol]
#     fig_15 = px.line(df_min15, x='ts', y='min15_mean', title="15min Mean Price")
#     st.plotly_chart(fig_15, use_container_width=True)

# # =========================
# # AI Prediction
# # =========================
# st.subheader("🤖 AI Prediction")
# df_symbol_all = df_all[df_all['symbol'] == selected_symbol]
# pred, prob = predict_latest(model, df_symbol_all, features)
# confidence = max(prob) * 100

# if pred == 1:
#     st.success(f"📈 BUY Signal ({prob[1]*100:.2f}%)")
# else:
#     st.error(f"📉 SELL Signal ({prob[0]*100:.2f}%)")
# st.write(f"Confidence: {confidence:.2f}%")

# # =========================
# # Backtesting
# # =========================
# st.subheader("📊 Backtesting Results")
# results = run_backtest(model, df_all, features)
# st.metric("💰 Total Return", f"{results['total_return']*100:.2f}%")
# st.metric("🎯 Win Rate", f"{results['win_rate']*100:.2f}%")
# st.metric("📉 Max Drawdown", f"{results['max_drawdown']*100:.2f}%")
# fig_bt = px.line(results['df'], x='ts', y='cum_return', title="Strategy Performance")
# st.plotly_chart(fig_bt, use_container_width=True)

# # =========================
# # Prediction Explanation
# # =========================
# st.subheader("🤔 What does this prediction mean?")
# if pred == 1:
#     st.success("The model expects the price to go UP based on recent trends and momentum.")
# else:
#     st.error("The model expects the price to go DOWN based on recent volatility and trend signals.")

# st.info("""
# This prediction is based on:
# - Price trends (MA7, MA30)
# - Daily volatility
# - Multi-timeframe signals (1D, 1H, 15min)
# - AI model features
# """)

# # =========================
# # Feature Importance
# # =========================
# importances = model.feature_importances_
# feat_df = pd.DataFrame({
#     "feature": features,
#     "importance": importances
# }).sort_values(by="importance", ascending=False)

# fig_imp = px.bar(feat_df, x='importance', y='feature', orientation='h', title="Feature Importance")
# st.plotly_chart(fig_imp)

# # =========================
# # Dashboard disclaimer
# # =========================
# st.warning(
#     "⚠️ Low accuracy due to limited dataset; this dashboard is for demo purposes only. "
#     "Signals should not be used for live trading."
#     )

# /app/dashboard/app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_prep import load_and_process_all
from model import train_model, predict_latest
from backtest import run_backtest

# =========================
# Page config (IMPORTANT: must be first Streamlit command)
# =========================
st.set_page_config(
    page_title="📊 Multi-Symbol Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Custom CSS – Dark financial terminal aesthetic
# =========================
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Barlow+Condensed:wght@300;600;700&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0b0f1a;
    --surface:   #111827;
    --border:    #1e2d40;
    --accent:    #00d4aa;
    --accent2:   #3b82f6;
    --bull:      #22c55e;
    --bear:      #ef4444;
    --muted:     #64748b;
    --text:      #e2e8f0;
    --text-dim:  #94a3b8;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Barlow Condensed', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent);
    border-radius: 8px 0 0 8px;
}
[data-testid="metric-container"] label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim) !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--accent) !important;
}

/* ── Plotly chart backgrounds ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Subheaders ── */
h3 { 
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em;
    color: var(--text) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-top: 2rem !important;
}

/* ── Info / warning boxes ── */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}

/* ── Selectbox ── */
div[data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}

/* ── Index card strip in sidebar ── */
.idx-card {
    background: #0f1924;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 6px;
    padding: 8px 10px;
    margin-bottom: 8px;
    font-size: 0.82rem;
}
.idx-card .sym { 
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    color: var(--accent);
    font-size: 0.85rem;
}
.idx-card .desc { color: var(--text-dim); font-size: 0.75rem; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0d1f35 0%, #0b0f1a 60%, #0d1f2e 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em;
    color: var(--text) !important;
    margin: 0 0 4px 0 !important;
    border: none !important;
    padding: 0 !important;
}
.hero p { 
    color: var(--text-dim);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    margin: 0;
    letter-spacing: 0.05em;
}
.hero .tag {
    display: inline-block;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.3);
    color: var(--accent);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 6px;
    margin-top: 10px;
}

/* ── Market snapshot ticker row ── */
.ticker-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.ticker-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
    min-width: 130px;
    flex: 1;
    text-align: center;
}
.ticker-item .t-sym {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.ticker-item .t-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    display: block;
    margin: 2px 0;
}
.ticker-item .t-chg.bull { color: var(--bull); font-size: 0.75rem; }
.ticker-item .t-chg.bear { color: var(--bear); font-size: 0.75rem; }

/* ── Section divider ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
    margin-top: 28px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# Load & cache data
# =========================
@st.cache_data
def get_featured_data():
    return load_and_process_all()

df_all, df_1d, df_1h, df_15m = get_featured_data()


@st.cache_resource
def get_model(_df):
    return train_model(_df)

model, features = get_model(df_all)


# =========================
# Symbol metadata (extended)
# =========================
symbol_meta = {
    "^GSPC":  {"name": "S&P 500",       "desc": "Top 500 US companies",         "category": "Index"},
    "^DJI":   {"name": "Dow Jones",      "desc": "30 major US companies",         "category": "Index"},
    "^IXIC":  {"name": "NASDAQ",         "desc": "Tech-focused US market",        "category": "Index"},
    "^RUT":   {"name": "Russell 2000",   "desc": "Small-cap US stocks",           "category": "Index"},
    "^FTSE":  {"name": "FTSE 100",       "desc": "Top 100 UK companies",          "category": "Global"},
    "^N225":  {"name": "Nikkei 225",     "desc": "Japan's major stock index",     "category": "Global"},
    "^GDAXI": {"name": "DAX 40",         "desc": "Germany's top 40 companies",    "category": "Global"},
    "^TNX":   {"name": "US 10Y Yield",   "desc": "Long-term US interest rates",   "category": "Rates"},
    "^IRX":   {"name": "US 3M T-Bill",   "desc": "Short-term interest rates",     "category": "Rates"},
    "^VIX":   {"name": "VIX",            "desc": "Market fear & volatility gauge","category": "Risk"},
    "GC=F":   {"name": "Gold Futures",   "desc": "Safe-haven commodity",          "category": "Commodity"},
    "CL=F":   {"name": "Crude Oil WTI",  "desc": "Global energy benchmark",       "category": "Commodity"},
    "EURUSD=X":{"name": "EUR/USD",       "desc": "Euro vs US Dollar",             "category": "FX"},
    "JPY=X":  {"name": "USD/JPY",        "desc": "US Dollar vs Japanese Yen",     "category": "FX"},
    "BTC-USD":{"name": "Bitcoin",        "desc": "Largest cryptocurrency",        "category": "Crypto"},
    "ETH-USD":{"name": "Ethereum",       "desc": "Smart contract platform token", "category": "Crypto"},
}

# Fallback for any symbol in data not in meta
def get_meta(sym):
    return symbol_meta.get(sym, {"name": sym, "desc": "Market instrument", "category": "Other"})

# Category color map
cat_colors = {
    "Index":     "#3b82f6",
    "Global":    "#8b5cf6",
    "Rates":     "#f59e0b",
    "Risk":      "#ef4444",
    "Commodity": "#f97316",
    "FX":        "#06b6d4",
    "Crypto":    "#a855f7",
    "Other":     "#64748b",
}


# =========================
# Hero Banner
# =========================
st.markdown("""
<div class="hero">
    <h1>📊 Market Intelligence Dashboard</h1>
    <p>MULTI-SYMBOL · AI-POWERED · MULTI-TIMEFRAME ANALYSIS</p>
    <span class="tag">LIVE DATA</span>
    <span class="tag">ML MODEL</span>
    <span class="tag">BACKTESTED</span>
</div>
""", unsafe_allow_html=True)


# =========================
# Market Snapshot – ticker strip using latest data
# =========================
st.markdown('<div class="section-label">▸ Market Snapshot</div>', unsafe_allow_html=True)

snapshot_syms = ["^GSPC", "^DJI", "^IXIC", "^TNX", "^VIX"]
available_syms = df_1d['symbol'].unique()

ticker_html = '<div class="ticker-row">'
for sym in snapshot_syms:
    if sym not in available_syms:
        continue
    row = df_1d[df_1d['symbol'] == sym].iloc[-1]
    val = row['close']
    ret = row['daily_return']
    chg_class = "bull" if ret >= 0 else "bear"
    arrow = "▲" if ret >= 0 else "▼"
    meta = get_meta(sym)
    ticker_html += f"""
    <div class="ticker-item">
        <div class="t-sym">{meta['name']}</div>
        <span class="t-val">{val:,.2f}</span>
        <span class="t-chg {chg_class}">{arrow} {abs(ret)*100:.2f}%</span>
    </div>"""
ticker_html += '</div>'

st.markdown(ticker_html, unsafe_allow_html=True)


# =========================
# Sidebar
# =========================
st.sidebar.markdown("""
<div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem; 
            letter-spacing:0.15em; color:#00d4aa; margin-bottom:12px;">
▸ INSTRUMENT SELECTOR
</div>
""", unsafe_allow_html=True)

symbols = df_1d['symbol'].unique()

selected_symbol = st.sidebar.selectbox(
    "Choose Index / Instrument",
    symbols,
    format_func=lambda x: f"{x}  —  {get_meta(x)['name']}"
)

# ── Sidebar: full index reference cards ──
st.sidebar.markdown("""
<div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem; 
            letter-spacing:0.15em; color:#00d4aa; margin:16px 0 8px 0;">
▸ INDEX REFERENCE
</div>
""", unsafe_allow_html=True)

# Group by category
categories = {}
for sym in symbols:
    meta = get_meta(sym)
    cat = meta["category"]
    categories.setdefault(cat, []).append(sym)

for cat, syms in categories.items():
    color = cat_colors.get(cat, "#64748b")
    st.sidebar.markdown(
        f'<div style="font-size:0.65rem; font-family:IBM Plex Mono,monospace; '
        f'color:{color}; letter-spacing:0.1em; margin:10px 0 4px 0; '
        f'text-transform:uppercase;">{cat}</div>',
        unsafe_allow_html=True
    )
    for sym in syms:
        m = get_meta(sym)
        is_selected = sym == selected_symbol
        border_color = color if is_selected else "#1e2d40"
        bg = "#0f1f30" if is_selected else "#0f1419"
        st.sidebar.markdown(
            f'<div class="idx-card" style="border-left-color:{color}; background:{bg}; border-color:{border_color};">'
            f'<span class="sym">{sym}</span> '
            f'<span style="color:#94a3b8; font-size:0.7rem;">· {m["name"]}</span><br>'
            f'<span class="desc">{m["desc"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div style="font-family:IBM Plex Mono,monospace; font-size:0.65rem; '
    'color:#475569; text-align:center;">⚠️ Demo only — not financial advice</div>',
    unsafe_allow_html=True
)


# =========================
# Helpers
# =========================
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(11,15,26,0.6)',
    font=dict(family='IBM Plex Mono, monospace', color='#94a3b8', size=11),
    xaxis=dict(gridcolor='#1e2d40', linecolor='#1e2d40', showgrid=True),
    yaxis=dict(gridcolor='#1e2d40', linecolor='#1e2d40', showgrid=True),
    margin=dict(l=40, r=20, t=40, b=40),
)

def styled_chart(fig, title=""):
    fig.update_layout(**CHART_LAYOUT, title=dict(text=title, font=dict(size=13, color='#e2e8f0')))
    return fig


def plot_sparkline(series, color="#00d4aa"):
    fig = go.Figure(go.Scatter(y=series.values, mode='lines',
                               line=dict(color=color, width=2),
                               fill='tozeroy',
                               fillcolor=color.replace(')', ',0.08)').replace('rgb', 'rgba') if 'rgb' in color else color + '14'))
    fig.update_layout(
        height=80,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


def trend_icon(trend_value):
    return ("⬆️", "#22c55e") if trend_value == 1 else ("⬇️", "#ef4444")


def regime_icon(regime):
    if str(regime).lower() == "bull":
        return "⬆️", "#22c55e"
    elif str(regime).lower() == "bear":
        return "⬇️", "#ef4444"
    return "➡️", "#64748b"


# =========================
# Selected symbol data
# =========================
df_sym = df_1d[df_1d['symbol'] == selected_symbol]

if df_sym.empty:
    st.warning("No data available for selected instrument.")
    st.stop()

last_day = df_sym.iloc[-1]
sel_meta = get_meta(selected_symbol)


# =========================
# Overview
# =========================
st.markdown(f'<div class="section-label">▸ Overview — {sel_meta["name"]} ({selected_symbol})</div>',
            unsafe_allow_html=True)

trend_ic, trend_color = trend_icon(last_day['trend'])
regime_ic, regime_color = regime_icon(last_day['regime'])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Close Price",    f"{last_day['close']:.2f}")
col2.metric("Daily Return",   f"{last_day['daily_return']:.4f}")
col3.metric("Volatility",     f"{last_day['daily_volatility']:.4f}")
col4.metric("MA 7",           f"{last_day.get('MA_7', 0):.2f}")
col5.metric("MA 30",          f"{last_day.get('MA_30', 0):.2f}")

# Trend & regime inline badges
st.markdown(
    f"""<div style="display:flex; gap:16px; margin:12px 0;">
        <div style="background:#111827; border:1px solid #1e2d40; border-left:3px solid {trend_color};
                    border-radius:6px; padding:8px 16px; font-family:IBM Plex Mono,monospace; font-size:0.85rem;">
            {trend_ic} <span style="color:{trend_color}; font-weight:600;">TREND</span>
            &nbsp;{'BULLISH' if last_day['trend'] == 1 else 'BEARISH'}
        </div>
        <div style="background:#111827; border:1px solid #1e2d40; border-left:3px solid {regime_color};
                    border-radius:6px; padding:8px 16px; font-family:IBM Plex Mono,monospace; font-size:0.85rem;">
            {regime_ic} <span style="color:{regime_color}; font-weight:600;">REGIME</span>
            &nbsp;{str(last_day['regime']).upper()}
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Sparklines side by side
sp1, sp2 = st.columns(2)
with sp1:
    st.caption("Price (last 30 sessions)")
    st.plotly_chart(plot_sparkline(df_sym['close'].tail(30), color="#00d4aa"), use_container_width=True)
with sp2:
    st.caption("Daily Return (last 30 sessions)")
    st.plotly_chart(plot_sparkline(df_sym['daily_return'].tail(30), color="#f59e0b"), use_container_width=True)


# =========================
# Detailed View
# =========================
st.markdown('<div class="section-label">▸ Technical Analysis</div>', unsafe_allow_html=True)

fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=df_sym['ts'], y=df_sym['MA_7'],
                             name='MA 7', line=dict(color='#3b82f6', width=1.5)))
fig_ma.add_trace(go.Scatter(x=df_sym['ts'], y=df_sym['MA_30'],
                             name='MA 30', line=dict(color='#f59e0b', width=1.5)))
if 'close' in df_sym.columns:
    fig_ma.add_trace(go.Scatter(x=df_sym['ts'], y=df_sym['close'],
                                name='Close', line=dict(color='#94a3b8', width=1, dash='dot')))
st.plotly_chart(styled_chart(fig_ma, "Moving Averages vs Close Price"), use_container_width=True)

fig_vol = go.Figure(go.Scatter(
    x=df_sym['ts'], y=df_sym['daily_volatility'],
    fill='tozeroy', fillcolor='rgba(239,68,68,0.08)',
    line=dict(color='#ef4444', width=1.5), name='Volatility'
))
st.plotly_chart(styled_chart(fig_vol, "Daily Volatility"), use_container_width=True)


# =========================
# AI Prediction
# =========================
st.markdown('<div class="section-label">▸ AI Signal</div>', unsafe_allow_html=True)

df_symbol_all = df_all[df_all['symbol'] == selected_symbol]

if not df_symbol_all.empty:
    pred, prob = predict_latest(model, df_symbol_all, features)
    confidence = max(prob) * 100

    sig_col1, sig_col2 = st.columns([1, 2])
    with sig_col1:
        if confidence < 70:
            st.warning(f"⚠️ Weak Signal — {confidence:.1f}% confidence\nNo clear trade setup.")
        elif pred == 1:
            st.success(f"📈 BUY Signal\n{prob[1]*100:.1f}% confidence")
        else:
            st.error(f"📉 SELL Signal\n{prob[0]*100:.1f}% confidence")

    with sig_col2:
        # Confidence gauge using plotly
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={'suffix': "%", 'font': {'size': 28, 'color': '#e2e8f0', 'family': 'IBM Plex Mono'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#64748b', 'tickfont': {'color': '#64748b'}},
                'bar': {'color': '#00d4aa' if confidence >= 70 else '#64748b'},
                'bgcolor': '#111827',
                'bordercolor': '#1e2d40',
                'steps': [
                    {'range': [0, 50],  'color': 'rgba(239,68,68,0.15)'},
                    {'range': [50, 70], 'color': 'rgba(245,158,11,0.15)'},
                    {'range': [70, 100],'color': 'rgba(34,197,94,0.15)'},
                ],
                'threshold': {'line': {'color': '#f59e0b', 'width': 2}, 'value': 70}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Model Confidence", 'font': {'size': 13, 'color': '#94a3b8'}}
        ))
        fig_gauge.update_layout(
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
else:
    st.warning("No data available for prediction.")


# =========================
# Backtesting
# =========================
st.markdown('<div class="section-label">▸ Backtest Results</div>', unsafe_allow_html=True)

results = run_backtest(model, df_all, features)
display_return = max(results['total_return'], -1)

bt1, bt2, bt3 = st.columns(3)
bt1.metric("💰 Total Return",    f"{display_return*100:.2f}%")
bt2.metric("🎯 Win Rate",        f"{results['win_rate']*100:.2f}%")
bt3.metric("📉 Max Drawdown",    f"{results['max_drawdown']*100:.2f}%")

fig_bt = go.Figure(go.Scatter(
    x=results['df']['ts'], y=results['df']['cum_return'],
    fill='tozeroy', fillcolor='rgba(59,130,246,0.08)',
    line=dict(color='#3b82f6', width=2), name='Cumulative Return'
))
st.plotly_chart(styled_chart(fig_bt, "Strategy Cumulative Performance"), use_container_width=True)


# =========================
# Feature Importance
# =========================
st.markdown('<div class="section-label">▸ Feature Importance</div>', unsafe_allow_html=True)

importances = model.feature_importances_
feat_df = pd.DataFrame({
    "feature": features,
    "importance": importances
}).sort_values(by="importance", ascending=True).tail(15)

fig_imp = go.Figure(go.Bar(
    x=feat_df['importance'],
    y=feat_df['feature'],
    orientation='h',
    marker=dict(
        color=feat_df['importance'],
        colorscale=[[0, '#1e3a5f'], [0.5, '#3b82f6'], [1, '#00d4aa']],
        showscale=False
    )
))
st.plotly_chart(styled_chart(fig_imp, "Top Feature Importances (Model)"), use_container_width=True)


# =========================
# Explanation
# =========================
st.markdown('<div class="section-label">▸ How it works</div>', unsafe_allow_html=True)

st.info("""
**Model Inputs**
- Market trends via moving averages (MA 7 / MA 30)
- Rolling volatility signals
- Multi-timeframe confluence: 1D · 1H · 15min
- Price-derived features (returns, regime labels)

**Output**
Probability-weighted UP / DOWN signal with confidence score.
Signals below 70% confidence are flagged as weak and suppressed.
""")


# =========================
# Disclaimer
# =========================
st.markdown("""
<div style="background:#0f1419; border:1px solid #1e2d40; border-left:3px solid #f59e0b;
            border-radius:8px; padding:12px 18px; margin-top:20px;
            font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#94a3b8;">
⚠️ DISCLAIMER — This is a demo project for educational purposes only.
Model accuracy is limited by available data. Do NOT use this for real trading decisions.
Past performance does not guarantee future results.
</div>
""", unsafe_allow_html=True)