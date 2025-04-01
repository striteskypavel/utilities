# Použijeme oficiální Python image
FROM python:3.11-slim

# Nastavíme pracovní adresář
WORKDIR /app

# Nainstalujeme systémové závislosti pro build numpy a dalších balíčků
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Zkopírujeme requirements.txt a nainstalujeme závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Zkopírujeme zdrojové soubory
COPY . .

# Vytvoříme adresář pro uživatelská data
RUN mkdir -p data/users

# Exponujeme port pro Streamlit
EXPOSE 8501

# Nastavíme proměnné prostředí pro Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Spustíme aplikaci
CMD ["streamlit", "run", "App.py"] 