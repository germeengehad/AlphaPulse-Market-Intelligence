import pandas as pd
import numpy as np

def run_backtest(model, df, feature_cols):
    df = df.copy().dropna()

    # Features
    X = df[feature_cols]

    # Predictions
    df['prediction'] = model.predict(X)

    # Convert prediction to trading signal
    df['signal'] = df['prediction'].apply(lambda x: 1 if x == 1 else -1)

    # Actual returns
    df['market_return'] = df.groupby('symbol')['close'].pct_change()

    # Strategy returns
    df['strategy_return'] = df['signal'] * df['market_return']

    # Cumulative return
    df['cum_return'] = (1 + df['strategy_return']).cumprod()

    # Metrics
    total_return = df['cum_return'].iloc[-1] - 1
    win_rate = (df['strategy_return'] > 0).mean()

    # Max Drawdown
    cum_max = df['cum_return'].cummax()
    drawdown = df['cum_return'] / cum_max - 1
    max_drawdown = drawdown.min()

    return {
        "total_return": total_return,
        "win_rate": win_rate,
        "max_drawdown": max_drawdown,
        "df": df
    }