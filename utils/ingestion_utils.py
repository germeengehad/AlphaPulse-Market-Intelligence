import pandas as pd
import re


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens multi-index DataFrame column names into a single level.
    """
    flat_cols = []

    for col in df.columns:
        if isinstance(col, tuple):
            # Filter out empty parts & join with underscore
            clean = "_".join(str(c) for c in col if c and str(c).strip())
            flat_cols.append(clean)
        else:
            flat_cols.append(col)

    df = df.copy()
    df.columns = flat_cols
    return df

# utils/ingestion_utils.py


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to make it safe for filenames.
    Replaces invalid characters with underscores and handles special symbols.
    
    Examples:
        "^GSPC" -> "caretGSPC"
        "EUR/USD=X" -> "EUR_USD_eqX"
    """
    # Replace some common special symbols
    name = name.replace("^", "caret").replace("=", "eq").replace("/", "_")
    
    # Remove any other characters not allowed in filenames
    name = re.sub(r"[^\w\-_.]", "_", name)
    
    return name
