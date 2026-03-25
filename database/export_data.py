import pandas as pd
from sqlalchemy import create_engine
import os

# =========================
# DB config
# =========================
DB_USER = "stock_user"
DB_PASSWORD = "stock_pass"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "stock_db"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =========================
# Create folder
# =========================
os.makedirs("../dashboard/data", exist_ok=True)

# =========================
# FIX: Use raw DBAPI connection
# =========================
with engine.connect() as conn:
    raw_conn = conn.connection  # 👈 THIS IS THE MAGIC LINE

    df_1d = pd.read_sql("SELECT * FROM market_1d", raw_conn)
    df_1h = pd.read_sql("SELECT * FROM market_1h", raw_conn)
    df_15m = pd.read_sql("SELECT * FROM market_15m", raw_conn)

# =========================
# Save CSVs
# =========================
df_1d.to_csv("../dashboard/data/market_1d.csv", index=False)
df_1h.to_csv("../dashboard/data/market_1h.csv", index=False)
df_15m.to_csv("../dashboard/data/market_15m.csv", index=False)

print("✅ Data exported successfully!")