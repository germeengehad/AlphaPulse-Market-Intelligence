# connection.py
from sqlalchemy import create_engine
from config.base_config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def get_engine(echo=False):
    url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(url, echo=echo)
    return engine
