# import pandas as pd
# from database.connection import get_engine

# # =========================
# # CONFIG
# # =========================
# TABLES = ["market_1d", "market_1h", "market_15m"]

# ROLLING_1D = 7
# ROLLING_30D = 30
# ROLLING_1H = 24
# ROLLING_15M = 16

# # =========================
# # DATA LOADING & CLEANING
# # =========================
# def load_and_clean_table(table_name: str, engine) -> pd.DataFrame:
#     try:
#         df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
#     except Exception as e:
#         raise RuntimeError(f"Error loading table {table_name}: {e}")

#     df['ts'] = pd.to_datetime(df['ts'])

#     if 'adj_close' in df.columns:
#         df = df.drop(columns=['adj_close'])

#     df = df.sort_values(['symbol', 'ts'])

#     df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

#     return df.reset_index(drop=True)

# # =========================
# # FEATURE ENGINEERING
# # =========================
# def feature_engineering_1d(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy().sort_values(['symbol', 'ts'])

#     df['daily_return'] = df.groupby('symbol')['close'].pct_change()

#     df['MA_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_1D).mean())
#     df['MA_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_30D).mean())

#     df['daily_volatility'] = df.groupby('symbol')['daily_return'].transform(
#         lambda x: x.rolling(ROLLING_1D).std()
#     )

#     # 🔥 Momentum (VERY IMPORTANT for model)
#     df['momentum_3'] = df.groupby('symbol')['close'].pct_change(3)
#     df['momentum_7'] = df.groupby('symbol')['close'].pct_change(7)

#     df['trend'] = (df['MA_7'] > df['MA_30']).astype(int)

#     df['regime'] = "sideways"
#     df.loc[df['MA_7'] > df['MA_30'], 'regime'] = "bull"
#     df.loc[df['MA_7'] < df['MA_30'], 'regime'] = "bear"

#     return df


# def feature_engineering_1h(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy().sort_values(['symbol', 'ts'])

#     df['hourly_return'] = df.groupby('symbol')['close'].pct_change()
#     df['hourly_mean'] = df.groupby('symbol')['close'].transform(
#         lambda x: x.rolling(ROLLING_1H).mean()
#     )
#     df['hourly_volatility'] = df.groupby('symbol')['hourly_return'].transform(
#         lambda x: x.rolling(ROLLING_1H).std()
#     )
#     df['hourly_trend'] = (df['hourly_return'] > 0).astype(int)

#     return df


# def feature_engineering_15m(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy().sort_values(['symbol', 'ts'])

#     df['min15_return'] = df.groupby('symbol')['close'].pct_change()
#     df['min15_mean'] = df.groupby('symbol')['close'].transform(
#         lambda x: x.rolling(ROLLING_15M).mean()
#     )
#     df['min15_volatility'] = df.groupby('symbol')['min15_return'].transform(
#         lambda x: x.rolling(ROLLING_15M).std()
#     )
#     df['min15_trend'] = (df['min15_return'] > 0).astype(int)

#     return df

# # =========================
# # MULTI-TIMEFRAME MERGE
# # =========================
# def build_multi_timeframe_dataset(df_1d, df_1h, df_15m):
#     """
#     Align multi-timeframe data using asof merge (per symbol).
#     """

#     merged_list = []

#     symbols = df_1d['symbol'].unique()

#     for symbol in symbols:

#         df1 = df_1d[df_1d['symbol'] == symbol].sort_values('ts').reset_index(drop=True)
#         df2 = df_1h[df_1h['symbol'] == symbol].sort_values('ts').reset_index(drop=True)
#         df3 = df_15m[df_15m['symbol'] == symbol].sort_values('ts').reset_index(drop=True)

#         # ✅ Ensure timestamps are sorted for asof merge
#         assert df1['ts'].is_monotonic_increasing
#         assert df2['ts'].is_monotonic_increasing
#         assert df3['ts'].is_monotonic_increasing

#         # Merge 1H
#         df = pd.merge_asof(
#             df1,
#             df2[['ts', 'hourly_return', 'hourly_volatility']],
#             on='ts',
#             direction='backward'
#         )

#         # Merge 15m
#         df = pd.merge_asof(
#             df,
#             df3[['ts', 'min15_return', 'min15_volatility']],
#             on='ts',
#             direction='backward'
#         )

#         df['symbol'] = symbol
#         merged_list.append(df)

#     df_all = pd.concat(merged_list).reset_index(drop=True)
#     df_all = df_all.dropna()

#     return df_all
# # =========================
# # TARGET
# # =========================
# def add_target(df_all):
#     df_all = df_all.copy()

#     df_all['target'] = (
#         df_all.groupby('symbol')['close'].shift(-1) > df_all['close']
#     ).astype(int)

#     return df_all

# # =========================
# # MAIN PIPELINE
# # =========================
# def load_and_process_all():

#     engine = get_engine()

#     # Load
#     cleaned_tables = {
#         table: load_and_clean_table(table, engine)
#         for table in TABLES
#     }

#     # Feature engineering
#     df_1d = feature_engineering_1d(cleaned_tables['market_1d'])
#     df_1h = feature_engineering_1h(cleaned_tables['market_1h'])
#     df_15m = feature_engineering_15m(cleaned_tables['market_15m'])

#     # 🔥 Merge timeframes
#     df_all = build_multi_timeframe_dataset(df_1d, df_1h, df_15m)

#     # 🔥 Add target
#     df_all = add_target(df_all)

#     # 🔥 Drop NaN before modeling
#     df_all = df_all.dropna()

#     return df_all, df_1d, df_1h, df_15m

import os
import pandas as pd

# =========================
# CONFIG
# =========================
TABLES = ["market_1d", "market_1h", "market_15m"]

ROLLING_1D = 7
ROLLING_30D = 30
ROLLING_1H = 24
ROLLING_15M = 16

# =========================
# DATA DIR (relative to this file)
# =========================
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
print("Loading CSVs from:", DATA_DIR)

# =========================
# DATA LOADING & CLEANING
# =========================
def load_csv_table(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    print("Trying to load:", path)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} does not exist!\nMake sure the CSV file is inside the 'data' folder."
        )
    df = pd.read_csv(path, parse_dates=['ts'])
    df = df.sort_values(['symbol', 'ts']).reset_index(drop=True)
    df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
    if 'adj_close' in df.columns:
        df = df.drop(columns=['adj_close'])
    return df

# =========================
# FEATURE ENGINEERING
# =========================
def feature_engineering_1d(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    df['MA_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_1D).mean())
    df['MA_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_30D).mean())
    df['daily_volatility'] = df.groupby('symbol')['daily_return'].transform(lambda x: x.rolling(ROLLING_1D).std())
    df['momentum_3'] = df.groupby('symbol')['close'].pct_change(3)
    df['momentum_7'] = df.groupby('symbol')['close'].pct_change(7)
    df['trend'] = (df['MA_7'] > df['MA_30']).astype(int)
    df['regime'] = "sideways"
    df.loc[df['MA_7'] > df['MA_30'], 'regime'] = "bull"
    df.loc[df['MA_7'] < df['MA_30'], 'regime'] = "bear"
    return df

def feature_engineering_1h(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['hourly_return'] = df.groupby('symbol')['close'].pct_change()
    df['hourly_mean'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_1H).mean())
    df['hourly_volatility'] = df.groupby('symbol')['hourly_return'].transform(lambda x: x.rolling(ROLLING_1H).std())
    df['hourly_trend'] = (df['hourly_return'] > 0).astype(int)
    return df

def feature_engineering_15m(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['min15_return'] = df.groupby('symbol')['close'].pct_change()
    df['min15_mean'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(ROLLING_15M).mean())
    df['min15_volatility'] = df.groupby('symbol')['min15_return'].transform(lambda x: x.rolling(ROLLING_15M).std())
    df['min15_trend'] = (df['min15_return'] > 0).astype(int)
    return df

# =========================
# MULTI-TIMEFRAME MERGE
# =========================
def build_multi_timeframe_dataset(df_1d, df_1h, df_15m):
    merged_list = []
    symbols = df_1d['symbol'].unique()
    for symbol in symbols:
        df1 = df_1d[df_1d['symbol'] == symbol].sort_values('ts').reset_index(drop=True)
        df2 = df_1h[df_1h['symbol'] == symbol].sort_values('ts').reset_index(drop=True)
        df3 = df_15m[df_15m['symbol'] == symbol].sort_values('ts').reset_index(drop=True)

        df = pd.merge_asof(df1, df2[['ts', 'hourly_return', 'hourly_volatility']], on='ts', direction='backward')
        df = pd.merge_asof(df, df3[['ts', 'min15_return', 'min15_volatility']], on='ts', direction='backward')
        df['symbol'] = symbol
        merged_list.append(df)

    df_all = pd.concat(merged_list).reset_index(drop=True)
    return df_all.dropna()

# =========================
# TARGET
# =========================
def add_target(df_all):
    df_all = df_all.copy()
    df_all['target'] = (df_all.groupby('symbol')['close'].shift(-1) > df_all['close']).astype(int)
    return df_all

# =========================
# MAIN PIPELINE
# =========================
def load_and_process_all():
    df_1d = load_csv_table("market_1d.csv")
    df_1h = load_csv_table("market_1h.csv")
    df_15m = load_csv_table("market_15m.csv")

    df_1d = feature_engineering_1d(df_1d)
    df_1h = feature_engineering_1h(df_1h)
    df_15m = feature_engineering_15m(df_15m)

    df_all = build_multi_timeframe_dataset(df_1d, df_1h, df_15m)
    df_all = add_target(df_all)
    df_all = df_all.dropna().reset_index(drop=True)

    return df_all, df_1d, df_1h, df_15m