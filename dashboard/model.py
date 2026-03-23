from sklearn.ensemble import RandomForestClassifier

def train_model(df):
    features = [
        'daily_return',
        'MA_7',
        'MA_30',
        'daily_volatility',
        'momentum_3',
        'momentum_7',
        'hourly_return',
        'hourly_volatility',
        'min15_return',
        'min15_volatility'
    ]

    df = df.dropna()

    X = df[features]
    y = df['target']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model, features


def predict_latest(model, df, features):
    df = df.dropna()

    latest = df.iloc[-1:]
    X = latest[features]

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    return pred, prob