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
cd v02/docker
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
Data aplikace jsou uložena v adresáři `../data`. Pro zálohování stačí zkopírovat tento adresář.

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