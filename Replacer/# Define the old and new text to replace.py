# Define the old and new text to replace
old_text = '<ExpirationType link:code="TS_COMMON_QUATER_NOCOMPRESS" />'
new_text = '<ExpirationType link:code="TS_COMMON_INFINITY_NOCOMPRESS" />'

# Process each XML file
for file_path in extracted_files:
    if file_path.endswith(".xml"):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Replace the target element if it exists
        if old_text in content:
            content = content.replace(old_text, new_text)
            
            # Save the modified content back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

# Repackage the files into a new ZIP
with zipfile.ZipFile(modified_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(extract_path):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, extract_path))

# Provide the modified ZIP file
modified_zip_path