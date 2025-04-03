#!/bin/bash

# Vytvoření adresáře pro zálohy
mkdir -p backups

# Získání aktuálního data pro název zálohy
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

# Zálohování dat z fly.io
echo "Zálohování dat z fly.io..."
fly ssh console -C "tar -czf /tmp/data_backup.tar.gz /app/data" || {
    echo "Chyba při vytváření zálohy na serveru"
    exit 1
}

# Stažení zálohy lokálně
echo "Stahování zálohy..."
fly ssh sftp get /tmp/data_backup.tar.gz "./backups/backup_${BACKUP_DATE}.tar.gz" || {
    echo "Chyba při stahování zálohy"
    exit 1
}

echo "Záloha byla úspěšně vytvořena: ./backups/backup_${BACKUP_DATE}.tar.gz" 