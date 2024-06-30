import difflib
import os

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1, tofile=file2)

        print('Rozdíly mezi soubory:')
        print(''.join(diff))

def compare_dirs(dir1, dir2):
    def get_files_and_dirs(root_dir):
        all_files = {}
        for path, _, files in os.walk(root_dir):
            for file in files:
                full_path = os.path.join(path, file)
                rel_path = os.path.relpath(full_path, root_dir)  # Relativní cesta od kořenového adresáře
                all_files[rel_path] = full_path
        return all_files

    files1 = get_files_and_dirs(dir1)
    files2 = get_files_and_dirs(dir2)

    unique_to_dir1 = set(files1) - set(files2)
    unique_to_dir2 = set(files2) - set(files1)
    common_files = set(files1) & set(files2)

    if unique_to_dir1:
        print(f'Soubory pouze v {dir1}:')
        for file in unique_to_dir1:
            print(f'  {file}')

    if unique_to_dir2:
        print(f'Soubory pouze v {dir2}:')
        for file in unique_to_dir2:
            print(f'  {file}')

    for file in common_files:
        file1_path = files1[file]
        file2_path = files2[file]
        compare_files(file1_path, file2_path)

if __name__ == "__main__":
    mode = input("Chcete porovnat soubory nebo adresáře? (soubory/adresáře): ").strip().lower()
    
    if mode == "soubory":
        file1 = input("Zadejte cestu k prvnímu souboru: ").strip()
        file2 = input("Zadejte cestu k druhému souboru: ").strip()
        if os.path.isfile(file1) and os.path.isfile(file2):
            compare_files(file1, file2)
        else:
            print("Jedna nebo obě zadané cesty neodkazují na soubor.")
    
    elif mode == "adresáře":
        dir1 = input("Zadejte cestu k prvnímu adresáři: ").strip()
        dir2 = input("Zadejte cestu k druhému adresáři: ").strip()
        if os.path.isdir(dir1) and os.path.isdir(dir2):
            compare_dirs(dir1, dir2)
        else:
            print("Jedna nebo obě zadané cesty neodkazují na adresář.")

    else:
        print("Neplatná volba. Ukončuji.")
