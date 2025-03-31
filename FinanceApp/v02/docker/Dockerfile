FROM python:3.11-slim

WORKDIR /app

# Instalace systémových závislostí
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopírování requirements.txt
COPY requirements.txt .

# Instalace Python závislostí
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir bcrypt

# Kopírování zdrojových souborů
COPY . .

# Vytvoření adresáře pro data a nastavení oprávnění
RUN mkdir -p data/users && \
    chmod -R 777 data

# Nastavení portu
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Spuštění aplikace
ENTRYPOINT ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"] 