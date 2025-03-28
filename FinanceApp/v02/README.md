# Finance App

Jednoduchá aplikace pro sledování osobních financí vytvořená pomocí Streamlit.

## Funkce

- Přidávání a správa finančních kategorií
- Editace částek přímo v tabulce
- Vizualizace dat pomocí grafů:
  - Rozložení financí (koláčový graf)
  - Historie změn
  - Porovnání kategorií
- Správa historie změn

## Instalace

1. Naklonujte repozitář:
```bash
git clone <repository-url>
cd FinanceApp
```

2. Vytvořte virtuální prostředí:
```bash
python3 -m venv venv
source venv/bin/activate  # Pro Windows: venv\Scripts\activate
```

3. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

## Spuštění aplikace

```bash
streamlit run App.py
```

Aplikace bude dostupná na:
- Local URL: http://localhost:8501
- Network URL: http://192.168.0.17:8501

## Docker

Aplikaci můžete také spustit pomocí Dockeru:

```bash
docker build -t finance-app .
docker run -p 8501:8501 finance-app
```

## Struktura projektu

- `App.py` - Hlavní aplikační soubor
- `visualizations.py` - Vizualizační komponenty
- `data_manager.py` - Správa dat
- `history_manager.py` - Správa historie
- `config.py` - Konfigurace aplikace
- `data/` - Složka pro ukládání dat
- `Dockerfile` - Konfigurace pro Docker
- `requirements.txt` - Seznam závislostí

## Licence

MIT 

# Finance App - Docker Deployment

## Předpoklady
- Docker
- Docker Compose
- Doména wedos.cz
- SSH přístup k serveru

## Instalace na server

1. Klonování repozitáře:
```bash
git clone <your-repo-url>
cd v02
```

2. Nastavení SSL certifikátu:
```bash
# Upravte email v init-letsencrypt.sh
nano init-letsencrypt.sh

# Nastavte práva pro skript
chmod +x init-letsencrypt.sh

# Spusťte inicializaci SSL
./init-letsencrypt.sh
```

3. Spuštění aplikace:
```bash
docker-compose up -d
```

## Správa aplikace

### Zastavení aplikace
```bash
docker-compose down
```

### Restart aplikace
```bash
docker-compose restart
```

### Zobrazení logů
```bash
# Logy aplikace
docker-compose logs -f finance-app

# Logy Nginx
docker-compose logs -f nginx
```

### Aktualizace aplikace
```bash
# Pull nových změn
git pull

# Rebuild a restart
docker-compose up -d --build
```

## Zálohování dat
Data aplikace jsou uložena v adresáři `./data`. Pro zálohování stačí zkopírovat tento adresář.

## Monitoring
- Aplikace je dostupná na https://wedos.cz
- Nginx logy jsou dostupné v `/var/log/nginx`
- Docker logy jsou dostupné přes `docker-compose logs`

## Bezpečnost
- SSL certifikáty se automaticky obnovují
- Firewall by měl povolovat pouze porty 80 a 443
- Pravidelně aktualizujte Docker image
- Sledujte logy pro podezřelou aktivitu

## Řešení problémů

### SSL certifikát nefunguje
1. Zkontrolujte logy certbotu:
```bash
docker-compose logs certbot
```

2. Zkuste znovu inicializovat certifikát:
```bash
./init-letsencrypt.sh
```

### Aplikace není dostupná
1. Zkontrolujte stav kontejnerů:
```bash
docker-compose ps
```

2. Zkontrolujte logy:
```bash
docker-compose logs
```

3. Zkontrolujte DNS záznamy pro doménu wedos.cz 

# Finance App - Deployment Guide

## Požadavky
- Git
- Docker
- Docker Compose

## Instalace na Linux serveru

### 1. Instalace závislostí (pokud nejsou nainstalovány)
```bash
# Instalace Dockeru
sudo apt update
sudo apt install -y docker.io docker-compose

# Spuštění a povolení Docker služby
sudo systemctl start docker
sudo systemctl enable docker

# Přidání uživatele do skupiny docker (volitelné, pro spouštění bez sudo)
sudo usermod -aG docker $USER
# Po tomto příkazu je nutné se odhlásit a znovu přihlásit
```

### 2. Klonování repozitáře
```bash
# Klonování repozitáře
git clone https://github.com/yourusername/FinanceApp.git
cd FinanceApp/v02
```

### 3. Konfigurace (volitelné)
- Upravte `docker/docker-compose.yml` pro změnu portů nebo dalších nastavení
- Upravte `docker/nginx/conf.d/app.conf` pro konfiguraci NGINX

### 4. Spuštění aplikace
```bash
# Přejděte do složky s Docker soubory
cd docker

# Spuštění aplikace
docker-compose up -d

# Zobrazení logů
docker-compose logs -f
```

Aplikace bude dostupná na:
- HTTP: http://vas-server:80
- HTTPS: https://vas-server:443 (pokud je nakonfigurován SSL)

### 5. Správa aplikace
```bash
# Zastavení aplikace
docker-compose down

# Restart aplikace
docker-compose restart

# Aktualizace aplikace (při změnách v kódu)
git pull
docker-compose up -d --build
```

### 6. Řešení problémů
```bash
# Zobrazení stavu kontejnerů
docker-compose ps

# Zobrazení logů konkrétního kontejneru
docker-compose logs app
docker-compose logs nginx

# Smazání všech dat a restart
docker-compose down -v
docker-compose up -d --build
```

## Zabezpečení
- Ujistěte se, že máte nastavený firewall a povolené pouze potřebné porty
- Pro produkční nasazení doporučujeme:
  - Nastavit SSL certifikát
  - Změnit výchozí porty
  - Nastavit silné heslo pro databázi
  - Pravidelně zálohovat data

## Data
- Všechna uživatelská data jsou uložena v Docker volume `app_data`
- Pro zálohování dat můžete použít:
```bash
docker run --rm -v app_data:/data -v $(pwd):/backup ubuntu tar czf /backup/data_backup.tar.gz /data
```

## Monitoring
Pro monitoring aplikace doporučujeme:
- Nastavit Prometheus + Grafana
- Použít Docker monitoring nástroje
- Sledovat logy pomocí ELK stacku nebo podobného řešení 