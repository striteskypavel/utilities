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