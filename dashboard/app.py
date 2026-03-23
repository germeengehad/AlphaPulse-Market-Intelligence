# # /app/dashboard/app.py
# import streamlit as st
# import plotly.express as px
# import pandas as pd
# from data_prep import load_and_process_all


# # =========================
# # Load & cache processed data
# # =========================
# @st.cache_data
# def get_featured_data():
#     return load_and_process_all()

# df_all, df_1d, df_1h, df_15m = get_featured_data()

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
# # Sparkline helper
# # =========================
# def plot_sparkline(series, color="blue"):
#     fig = px.line(series, height=50)
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
#     if trend_value == "bull" or trend_value == 1:
#         return "⬆️", "green"
#     elif trend_value == "bear" or trend_value == -1:
#         return "⬇️", "red"
#     else:
#         return "➡️", "gray"

# def regime_icon(regime):
#     if regime.lower() == "bull":
#         return "⬆️", "green"
#     elif regime.lower() == "bear":
#         return "⬇️", "red"
#     else:
#         return "➡️", "gray"

# # =========================
# # Multi-symbol summary cards
# # =========================
# st.subheader("📌 Symbols Summary")
# symbols = df_1d['symbol'].unique()

# # Display cards in a responsive grid (3 columns)
# cols = st.columns(3)

# for i, symbol in enumerate(symbols):
#     col = cols[i % 3]
#     df_sym = df_1d[df_1d['symbol'] == symbol]
#     last_day = df_sym.iloc[-1]

#     trend_ic, trend_color = trend_icon(last_day['trend'])
#     regime_ic, regime_color = regime_icon(last_day['regime'])

#     with col:
#         st.markdown(f"### {symbol}")
#         st.metric("Close", f"{last_day['close']:.2f}")
#         st.plotly_chart(plot_sparkline(df_sym['close'].tail(30), color="blue"), use_container_width=True)

#         st.metric("Daily Return", f"{last_day['daily_return']:.4f}")
#         st.plotly_chart(plot_sparkline(df_sym['daily_return'].tail(30), color="orange"), use_container_width=True)

#         st.markdown(f"<h4 style='color:{trend_color}'>{trend_ic} Trend</h4>", unsafe_allow_html=True)
#         st.write("Bull" if last_day['trend'] == 1 else "Bear")

#         st.markdown(f"<h4 style='color:{regime_color}'>{regime_ic} Regime</h4>", unsafe_allow_html=True)
#         st.write(last_day['regime'].capitalize())

# # =========================
# # Optional: select symbol for detailed plots
# # =========================
# st.subheader("📈 Detailed View")
# selected_symbol = st.selectbox("Select Symbol for Detailed Plots", symbols)
# daily_df = df_1d[df_1d['symbol'] == selected_symbol]

# st.write(f"### Detailed Plots for {selected_symbol}")

# # Daily Moving Averages
# fig_ma = px.line(daily_df, x='ts', y=['MA_7', 'MA_30'], title="MA7 vs MA30")
# st.plotly_chart(fig_ma, use_container_width=True)

# # Daily Volatility
# fig_vol = px.line(daily_df, x='ts', y='daily_volatility', title="Daily Volatility")
# st.plotly_chart(fig_vol, use_container_width=True)

# # Optional High-Frequency Aggregates
# if st.checkbox("Show 1H Aggregates"):
#     df_hour = df_1h[df_1h['symbol'] == selected_symbol]
#     fig_hr = px.line(df_hour, x='ts', y='hourly_mean', title="Hourly Mean Price")
#     st.plotly_chart(fig_hr, use_container_width=True)

# if st.checkbox("Show 15min Aggregates"):
#     df_min15 = df_15m[df_15m['symbol'] == selected_symbol]
#     fig_15 = px.line(df_min15, x='ts', y='min15_mean', title="15min Mean Price")
#     st.plotly_chart(fig_15, use_container_width=True)


# /app/dashboard/app.py
import streamlit as st
import plotly.express as px
import pandas as pd

from data_prep import load_and_process_all
from model import train_model, predict_latest


# =========================
# Load & cache processed data
# =========================
@st.cache_data
def get_featured_data():
    return load_and_process_all()

df_all, df_1d, df_1h, df_15m = get_featured_data()


# =========================
# Load & cache model
# =========================
@st.cache_data
def get_model(df):
    return train_model(df)

model, features = get_model(df_all)


# =========================
# Page layout
# =========================
st.set_page_config(
    page_title="📊 Multi-Symbol Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Multi-Symbol Market Dashboard")


# =========================
# Sparkline helper
# =========================
def plot_sparkline(series, color="blue"):
    fig = px.line(series, height=60)
    fig.update_traces(line_color=color, line_width=2)
    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


# =========================
# Trend / Regime icons
# =========================
def trend_icon(trend_value):
    if trend_value == 1:
        return "⬆️", "green"
    else:
        return "⬇️", "red"


def regime_icon(regime):
    if regime.lower() == "bull":
        return "⬆️", "green"
    elif regime.lower() == "bear":
        return "⬇️", "red"
    else:
        return "➡️", "gray"


# =========================
# Multi-symbol summary cards
# =========================
st.subheader("📌 Symbols Overview")

symbols = df_1d['symbol'].unique()
cols = st.columns(3)

for i, symbol in enumerate(symbols):
    col = cols[i % 3]
    df_sym = df_1d[df_1d['symbol'] == symbol]

    if df_sym.empty:
        continue

    last_day = df_sym.iloc[-1]

    trend_ic, trend_color = trend_icon(last_day['trend'])
    regime_ic, regime_color = regime_icon(last_day['regime'])

    with col:
        st.markdown(f"### {symbol}")

        st.metric("Close", f"{last_day['close']:.2f}")
        st.plotly_chart(
            plot_sparkline(df_sym['close'].tail(30)),
            use_container_width=True
        )

        st.metric("Daily Return", f"{last_day['daily_return']:.4f}")
        st.plotly_chart(
            plot_sparkline(df_sym['daily_return'].tail(30), color="orange"),
            use_container_width=True
        )

        st.markdown(
            f"<h4 style='color:{trend_color}'>{trend_ic} Trend</h4>",
            unsafe_allow_html=True
        )
        st.write("Bull" if last_day['trend'] == 1 else "Bear")

        st.markdown(
            f"<h4 style='color:{regime_color}'>{regime_ic} Regime</h4>",
            unsafe_allow_html=True
        )
        st.write(last_day['regime'].capitalize())


# =========================
# Detailed view
# =========================
st.subheader("📈 Detailed View")

selected_symbol = st.selectbox(
    "Select Symbol",
    symbols
)

daily_df = df_1d[df_1d['symbol'] == selected_symbol]

if daily_df.empty:
    st.warning("No data available for selected symbol.")
    st.stop()

st.write(f"### Detailed Analysis for {selected_symbol}")

# Moving averages
fig_ma = px.line(
    daily_df,
    x='ts',
    y=['MA_7', 'MA_30'],
    title="MA7 vs MA30"
)
st.plotly_chart(fig_ma, use_container_width=True)

# Volatility
fig_vol = px.line(
    daily_df,
    x='ts',
    y='daily_volatility',
    title="Daily Volatility"
)
st.plotly_chart(fig_vol, use_container_width=True)


# =========================
# Optional High-Frequency
# =========================
if st.checkbox("Show 1H Data"):
    df_hour = df_1h[df_1h['symbol'] == selected_symbol]

    fig_hr = px.line(
        df_hour,
        x='ts',
        y='hourly_mean',
        title="Hourly Mean Price"
    )
    st.plotly_chart(fig_hr, use_container_width=True)


if st.checkbox("Show 15min Data"):
    df_min15 = df_15m[df_15m['symbol'] == selected_symbol]

    fig_15 = px.line(
        df_min15,
        x='ts',
        y='min15_mean',
        title="15min Mean Price"
    )
    st.plotly_chart(fig_15, use_container_width=True)


# =========================
# 🤖 AI Prediction
# =========================
st.subheader("🤖 AI Prediction")

df_symbol_all = df_all[df_all['symbol'] == selected_symbol]

if df_symbol_all.empty:
    st.warning("No data for prediction.")
else:
    pred, prob = predict_latest(model, df_symbol_all, features)

    confidence = max(prob) * 100

    if pred == 1:
        st.success(f"📈 BUY Signal ({prob[1]*100:.2f}%)")
    else:
        st.error(f"📉 SELL Signal ({prob[0]*100:.2f}%)")

    st.write(f"Confidence: {confidence:.2f}%")