import os
import zipfile
import shutil
import filecmp
import stat
import platform
import json
from pathlib import Path
import argparse

def load_config(config_path):
    """Načte konfiguraci ze souboru JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        required_keys = ['dev_zip', 'test_zip', 'output_zip']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"V konfiguračním souboru chybí povinný klíč: {key}")
        
        # Převod relativních cest na absolutní
        config['dev_zip'] = os.path.abspath(os.path.expanduser(config['dev_zip']))
        config['test_zip'] = os.path.abspath(os.path.expanduser(config['test_zip']))
        config['output_zip'] = os.path.abspath(os.path.expanduser(config['output_zip']))
        
        # Volitelné parametry s výchozími hodnotami
        config['work_dir'] = os.path.abspath(os.path.expanduser(
            config.get('work_dir', os.path.join(os.getcwd(), 'temp'))
        ))
        config['keep_temp'] = config.get('keep_temp', False)
        config['ignore_patterns'] = config.get('ignore_patterns', [])
        
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Chyba při čtení JSON konfigurace: {str(e)}")
    except Exception as e:
        raise Exception(f"Chyba při načítání konfigurace: {str(e)}")

def should_ignore_file(filename, custom_patterns=None):
    """Kontroluje, zda by měl být soubor ignorován."""
    default_patterns = {
        '.DS_Store',  # macOS system file
        '._.DS_Store',  # macOS system file
        '__MACOSX',  # macOS directory in ZIP files
        '.AppleDouble',  # macOS resource fork
        '.LSOverride',  # macOS resource fork
        'Thumbs.db',  # Windows thumbnail cache
        'desktop.ini'  # Windows system file
    }
    
    # Přidání vlastních vzorů k výchozím
    if custom_patterns:
        default_patterns.update(set(custom_patterns))
    
    return any(pattern in filename for pattern in default_patterns)

def preserve_permissions(src, dst):
    """Zachová oprávnění souboru při kopírování."""
    if platform.system() in ['Darwin', 'Linux']:
        st = os.stat(src)
        os.chmod(dst, stat.S_IMODE(st.st_mode))

def unzip_folder(zip_path, extract_path, ignore_patterns=None):
    """Rozbalí ZIP archiv do cílové složky."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        files_to_extract = [f for f in zip_ref.namelist() 
                          if not should_ignore_file(f, ignore_patterns) and 
                          not f.startswith('__MACOSX/')]
        for file in files_to_extract:
            zip_ref.extract(file, extract_path)

def compare_and_copy_files(source_path, target_path, diff_path, ignore_patterns=None):
    """Porovná soubory mezi zdrojovou a cílovou složkou a zkopíruje rozdílné do diff složky."""
    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if not should_ignore_file(d, ignore_patterns)]
        
        rel_path = os.path.relpath(root, source_path)
        target_dir = os.path.join(target_path, rel_path)
        diff_dir = os.path.join(diff_path, rel_path)

        os.makedirs(diff_dir, exist_ok=True)

        for file in files:
            if should_ignore_file(file, ignore_patterns):
                continue

            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)
            diff_file = os.path.join(diff_dir, file)

            if not os.path.exists(target_file) or not filecmp.cmp(source_file, target_file, shallow=False):
                shutil.copy2(source_file, diff_file)
                preserve_permissions(source_file, diff_file)

def create_zip(source_path, zip_path, ignore_patterns=None):
    """Vytvoří ZIP archiv ze složky."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            dirs[:] = [d for d in dirs if not should_ignore_file(d, ignore_patterns)]
            
            for file in files:
                if should_ignore_file(file, ignore_patterns):
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_path)
                zipf.write(file_path, arcname)

def parse_arguments():
    """Zpracuje argumenty příkazové řádky."""
    parser = argparse.ArgumentParser(description='Porovná dva ZIP soubory a vytvoří rozdílový ZIP.')
    parser.add_argument('--config', required=True, help='Cesta ke konfiguračnímu souboru JSON')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        print(f"Načítám konfiguraci z {args.config}...")
        config = load_config(args.config)
        
        dev_zip = config['dev_zip']
        test_zip = config['test_zip']
        diff_zip = config['output_zip']
        work_dir = config['work_dir']
        ignore_patterns = config['ignore_patterns']

        # Vytvoření pracovních složek
        dev_extract = os.path.join(work_dir, "DEV_extracted")
        test_extract = os.path.join(work_dir, "TEST_extracted")
        diff_path = os.path.join(work_dir, "DIFF")

        # Kontrola existence vstupních souborů
        if not os.path.exists(dev_zip):
            raise FileNotFoundError(f"DEV ZIP soubor nebyl nalezen: {dev_zip}")
        if not os.path.exists(test_zip):
            raise FileNotFoundError(f"TEST ZIP soubor nebyl nalezen: {test_zip}")

        # Vytvoření pracovních složek
        os.makedirs(work_dir, exist_ok=True)
        for path in [dev_extract, test_extract, diff_path]:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

        # Vytvoření složky pro výstupní ZIP
        os.makedirs(os.path.dirname(diff_zip), exist_ok=True)

        print(f"Rozbaluji {os.path.basename(dev_zip)}...")
        unzip_folder(dev_zip, dev_extract, ignore_patterns)
        print(f"Rozbaluji {os.path.basename(test_zip)}...")
        unzip_folder(test_zip, test_extract, ignore_patterns)

        print("Porovnávám složky a kopíruji rozdílné soubory...")
        compare_and_copy_files(dev_extract, test_extract, diff_path, ignore_patterns)

        print(f"Vytvářím výsledný ZIP archiv: {os.path.basename(diff_zip)}...")
        create_zip(diff_path, diff_zip, ignore_patterns)

        print("Hotovo! Výsledný diff je v souboru:", diff_zip)

    except Exception as e:
        print(f"Chyba: {str(e)}")
        raise

    finally:
        if not config.get('keep_temp', False):
            print("Uklízím pracovní složky...")
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)

if __name__ == "__main__":
    main()