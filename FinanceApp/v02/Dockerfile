# Použijeme oficiální Python image jako základ
FROM python:3.11-slim

# Nastavení pracovního adresáře v containeru
WORKDIR /app

# Instalace systémových závislostí
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopírování requirements.txt
COPY requirements.txt .

# Instalace závislostí
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Kopírování zdrojových souborů
COPY . .

# Vytvoření adresářů pro data
RUN mkdir -p data/users

# Nastavení portu pro Streamlit
EXPOSE 8080

# Nastavení proměnných prostředí pro Streamlit
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

# Spuštění aplikace
CMD ["streamlit", "run", "App.py"] 