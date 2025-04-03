#!/bin/bash

# Kontrola, zda byl zadán argument s cestou k záloze
if [ "$#" -ne 1 ]; then
    echo "Použití: $0 cesta_k_zaloze.tar.gz"
    exit 1
fi

BACKUP_FILE=$1

# Kontrola existence záložního souboru
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Záložní soubor $BACKUP_FILE neexistuje"
    exit 1
fi

# Nahrání zálohy na server
echo "Nahrávání zálohy na server..."
fly ssh sftp -a finance-app-bitter-morning-9768 put "$BACKUP_FILE" /tmp/data_restore.tar.gz || {
    echo "Chyba při nahrávání zálohy"
    exit 1
}

# Obnovení dat na serveru
echo "Obnovování dat..."
fly ssh console -a finance-app-bitter-morning-9768 -C "cd /app && tar -xzf /tmp/data_restore.tar.gz" || {
    echo "Chyba při obnovování dat"
    exit 1
}

echo "Data byla úspěšně obnovena" 