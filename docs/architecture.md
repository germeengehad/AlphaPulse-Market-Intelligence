Architecture Overview
---------------------

Data Sources:
1. Yahoo Finance (price data)
2. News APIs (text sentiment)
3. Proprietary custom features

Components:
- ETL pipeline → SQL
- Feature engine → ML-ready datasets
- ML models → predictions
- Strategy engine → market exposure
- Live runner → updates daily
- API server → external use
