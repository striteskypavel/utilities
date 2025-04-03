# Proces nasazení aplikace

Tento dokument popisuje proces nasazení nové verze aplikace se zachováním uživatelských dat.

## Příprava

1. Ujistěte se, že máte nainstalovaný fly.io CLI nástroj
2. Přihlaste se k fly.io pomocí `fly auth login`
3. Přejděte do složky s deployment skripty:
   ```bash
   cd deployment
   ```
4. Nastavte správné oprávnění pro skripty:
   ```bash
   chmod +x backup_data.sh restore_data.sh
   ```

## Postup nasazení

### 1. Zálohování dat

Před nasazením nové verze vždy zálohujte data:

```bash
./backup_data.sh
```

Záloha bude uložena v adresáři `backups` s časovým razítkem.

### 2. Nasazení nové verze

Přejděte do kořenové složky aplikace a nasaďte novou verzi:

```bash
cd ..
fly deploy
```

### 3. Kontrola nasazení

Zkontrolujte, že aplikace běží:

```bash
fly status
```

### 4. Obnovení dat (pokud je potřeba)

Pokud je potřeba obnovit data ze zálohy:

```bash
cd deployment
./restore_data.sh ./backups/nazev_zalohy.tar.gz
```

## Řešení problémů

### Ztráta dat

Pokud dojde ke ztrátě dat během nasazení:

1. Zastavte aplikaci: `fly scale count 0`
2. Obnovte data ze zálohy pomocí `restore_data.sh`
3. Spusťte aplikaci: `fly scale count 1`

### Problémy s volumes

Pokud máte problémy s volumes:

1. Zkontrolujte stav volumes: `fly volumes list`
2. Ujistěte se, že volume je připojen k aplikaci
3. V případě potřeby vytvořte nový volume: `fly volumes create finance_data --size 1`

## Důležité poznámky

- Vždy vytvořte zálohu před nasazením nové verze
- Udržujte historii záloh pro případ potřeby obnovení starší verze dat
- Pravidelně kontrolujte stav volumes a jejich využití
- Při problémech s přístupem k datům zkuste restartovat aplikaci 