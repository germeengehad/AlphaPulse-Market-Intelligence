# 🚀 AlphaPulse – AI-Powered Market Intelligence System

> End-to-end trading analytics platform combining **data engineering, machine learning, and interactive visualization** to generate actionable market insights.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue) ![Airflow](https://img.shields.io/badge/Airflow-ETL-orange)

---

## 📌 Overview

AlphaPulse is a full-stack market intelligence system designed to simulate how modern trading platforms operate.

It automatically collects financial data, processes it through a data pipeline, applies machine learning models, and delivers real-time insights through an interactive dashboard.

This project demonstrates the ability to **build production-style data systems**, not just standalone ML models.

---

## 🎯 Key Objectives

- Build a complete **data pipeline** from raw market data to insights  
- Apply **machine learning** for trading signal generation  
- Provide **interpretable analytics** for non-technical users  
- Deliver a **professional dashboard experience**  

---

## ⚙️ System Architecture


       ┌───────────────────────┐
       │    Yahoo Finance      │
       │     Market Data       │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │       Airflow         │
       │   ETL & Scheduler     │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │       Postgres        │
       │   Historical Storage  │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │       Streamlit       │
       │ Dashboard + AI Layer  │
       └───────────────────────┘

### 🔹 Components

- **Data Source**
  - Market data fetched from Yahoo Finance

- **Data Engineering**
  - Apache Airflow orchestrates ETL pipelines
  - Scheduled data ingestion and transformation
  - Dockerized environment for reproducibility

- **Storage**
  - PostgreSQL database for structured historical data

- **Machine Learning**
  - Feature engineering across multiple timeframes (1D, 1H, 15min)
  - Predictive model generating BUY/SELL signals
  - Feature importance for interpretability

- **Frontend**
  - Interactive Streamlit dashboard
  - Real-time insights and visual analytics
  - User-friendly explanations of financial metrics

---

## 📊 Features

### 🔥 AI Trading Signals
- BUY / SELL predictions with confidence scores
- Signal filtering based on probability threshold

### 📈 Multi-Timeframe Analysis
- Daily, hourly, and 15-minute data integration
- Moving averages, volatility, and trend detection

### 🧠 Intelligent Insights
- AI-generated explanations of market conditions
- Simplified interpretation for non-experts

### 📊 Backtesting Engine
- Simulates historical trading performance
- Metrics:
  - Total Return
  - Win Rate
  - Maximum Drawdown

### 📉 Visualization
- Interactive charts using Plotly
- Clean, modern UI with dark fintech theme

---

## ⚠️ Model Performance Note

Due to limited dataset size, the model shows:

- Moderate prediction accuracy
- Negative backtesting returns in some scenarios

👉 This is expected in early-stage trading models and is intentionally included to demonstrate:
- Real-world challenges in financial ML
- Importance of data quality and quantity
- Honest evaluation of model limitations

---

## 🌐 Live Demo

👉 [Open Dashboard](https://alphapulse-market-intelligence-n8gya9pdwmar6ad8gf4rxr.streamlit.app/)

---

## 🧠 What This Project Demonstrates

- End-to-end **Data Engineering pipeline design**
- Practical **Machine Learning application**
- Understanding of **financial markets & signals**
- Ability to build **user-focused data products**
- Experience with:
  - Docker
  - Airflow
  - PostgreSQL
  - Streamlit
  - Python ML stack

---

## 🚀 Future Improvements

- Improve model performance with larger datasets
- Add real-time streaming data
- Implement advanced models (LSTM, Transformers)
- Deploy full cloud infrastructure (AWS/GCP)
- Add portfolio optimization & risk management

---

## 👨‍💻 Author

**Germeen Gehad**  
Data Science & Machine Learning Enthusiast  

---

## ⭐ Final Note

This project focuses not only on building models, but on creating a **complete, production-like system** that transforms data into insights.

It reflects the mindset of building **real-world AI products**, not just experiments.
