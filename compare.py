import difflib
import os

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
