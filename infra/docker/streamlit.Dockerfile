FROM python:3.10-slim

WORKDIR /app

COPY requirements/streamlit.txt .

RUN pip install --no-cache-dir -r streamlit.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "/app/dashboard/app.py", "--server.address=0.0.0.0"]