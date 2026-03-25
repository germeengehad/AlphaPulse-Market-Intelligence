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
import pandas as pd
from data_prep import load_and_process_all
from model import train_model, predict_latest
from backtest import run_backtest

# =========================
# Page config (FIRST)
# =========================
st.set_page_config(
    page_title="🚀 AlphaPulse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 🔥 PREMIUM UI STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.glow {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #38bdf8;
    text-shadow: 0 0 10px #38bdf8, 0 0 20px #38bdf8;
}
section[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Load data
# =========================
@st.cache_data
def get_featured_data():
    return load_and_process_all()

df_all, df_1d, df_1h, df_15m = get_featured_data()

# =========================
# Load model (FIXED cache bug)
# =========================
@st.cache_resource
def get_model(_df):
    return train_model(_df)

model, features = get_model(df_all)

# =========================
# Symbol explanations
# =========================
symbol_names = {
    "^GSPC": "S&P 500 – Top 500 US companies",
    "^DJI": "Dow Jones – 30 major US companies",
    "^IXIC": "NASDAQ – Tech-focused market",
    "^TNX": "US 10Y Yield – Interest rates",
    "^VIX": "Volatility Index – Fear gauge"
}

# =========================
# Sidebar
# =========================
st.sidebar.title("📊 Select Market")

selected_symbol = st.sidebar.selectbox(
    "Choose Index",
    df_1d['symbol'].unique(),
    format_func=lambda x: symbol_names.get(x, x)
)

st.sidebar.markdown("---")
st.sidebar.info("AI-powered market analysis dashboard")

# =========================
# Prepare data
# =========================
df_sym = df_1d[df_1d['symbol'] == selected_symbol]
df_symbol_all = df_all[df_all['symbol'] == selected_symbol]

if df_sym.empty:
    st.warning("No data available.")
    st.stop()

last_day = df_sym.iloc[-1]

# =========================
# 🚀 HERO SECTION
# =========================
st.markdown("<div class='glow'>🚀 AI Trading Signal</div>", unsafe_allow_html=True)

pred, prob = predict_latest(model, df_symbol_all, features)
confidence = max(prob) * 100

col1, col2, col3 = st.columns(3)

col1.metric("💰 Price", f"{last_day['close']:.2f}")
col2.metric("📊 Return", f"{last_day['daily_return']:.4f}")
col3.metric("⚡ Volatility", f"{last_day['daily_volatility']:.4f}")

# =========================
# 🔥 SIGNAL CARD
# =========================
if confidence > 70:
    if pred == 1:
        st.markdown(
            f"<div class='metric-card'><h2 style='color:#22c55e;'>📈 BUY SIGNAL</h2><h3>{confidence:.2f}% Confidence</h3></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='metric-card'><h2 style='color:#ef4444;'>📉 SELL SIGNAL</h2><h3>{confidence:.2f}% Confidence</h3></div>",
            unsafe_allow_html=True
        )
else:
    st.markdown(
        f"<div class='metric-card'><h2 style='color:#facc15;'>⚠️ NO CLEAR SIGNAL</h2><h3>{confidence:.2f}% Confidence</h3></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# =========================
# 📊 PRICE CHART
# =========================
st.markdown("## 📊 Price Movement")

fig_price = px.line(df_sym, x='ts', y='close')

fig_price.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_price, use_container_width=True)

# =========================
# 📊 MARKET STATUS
# =========================
st.markdown("## 📊 Market Status")

col1, col2, col3 = st.columns(3)

col1.metric("Trend", "Bullish" if last_day['trend'] == 1 else "Bearish")
col2.metric("Regime", last_day['regime'])
col3.metric("Volatility", 
            "High" if last_day['daily_volatility'] > 0.02 else "Normal")

# =========================
# 🧠 AI INSIGHT
# =========================
st.markdown("## 🧠 AI Insight")

if last_day['trend'] == 1 and last_day['daily_volatility'] < 0.02:
    st.success("Stable bullish trend detected.")
elif last_day['trend'] == 1:
    st.warning("Bullish but volatile market.")
elif last_day['trend'] == 0 and last_day['daily_volatility'] > 0.02:
    st.error("Strong bearish pressure.")
else:
    st.info("Sideways market.")

st.markdown("---")

# =========================
# 📈 DETAILED ANALYSIS
# =========================
st.markdown("## 📈 Detailed Analysis")

fig_ma = px.line(df_sym, x='ts', y=['MA_7', 'MA_30'])
fig_ma.update_layout(template="plotly_dark")

st.plotly_chart(fig_ma, use_container_width=True)

fig_vol = px.line(df_sym, x='ts', y='daily_volatility')
fig_vol.update_layout(template="plotly_dark")

st.plotly_chart(fig_vol, use_container_width=True)

# =========================
# 📊 BACKTESTING
# =========================
st.markdown("## 📊 Strategy Backtesting")

results = run_backtest(model, df_all, features)

st.metric("💰 Return", f"{results['total_return']*100:.2f}%")
st.metric("🎯 Win Rate", f"{results['win_rate']*100:.2f}%")
st.metric("📉 Drawdown", f"{results['max_drawdown']*100:.2f}%")

fig_bt = px.line(results['df'], x='ts', y='cum_return')
fig_bt.update_layout(template="plotly_dark")

st.plotly_chart(fig_bt, use_container_width=True)

# =========================
# 📊 FEATURE IMPORTANCE
# =========================
st.markdown("## 📊 Feature Importance")

importances = model.feature_importances_
feat_df = pd.DataFrame({
    "feature": features,
    "importance": importances
}).sort_values(by="importance", ascending=False)

fig_imp = px.bar(feat_df, x='importance', y='feature', orientation='h')
fig_imp.update_layout(template="plotly_dark")

st.plotly_chart(fig_imp, use_container_width=True)

# =========================
# ⚠️ DISCLAIMER
# =========================
st.warning(
    "⚠️ Low accuracy due to limited dataset. This project is for demonstration purposes only."
)

# =========================
# FOOTER
# =========================
st.markdown("""
---
### 👨‍💻 AlphaPulse – AI Trading System  
Built for portfolio & demonstration  
""")