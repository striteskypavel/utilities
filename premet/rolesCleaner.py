import pandas as pd
from xml.etree import ElementTree as ET
import re

def extract_full_code(description):
    """
    Extract the 'FULL CODE' value from the 'Description of the result of validation'.
    """
    match = re.search(r"FULL CODE: (\\.+?),", description)
    if match:
        return match.group(1)
    return None

def load_errors_from_csv(csv_file):
    """
    Load the CSV file and filter rows where 'Result' and 'Category' columns are both 'Error'.
    Returns a list of 'FULL CODE' values to remove.
    """
    csv_data = pd.read_csv(csv_file, encoding="ISO-8859-1", delimiter=";")
    error_rows = csv_data[(csv_data['Result'] == 'Error') & (csv_data['Category'] == 'Error')]
    return [extract_full_code(desc) for desc in error_rows['Description of the result of validation'].dropna() if extract_full_code(desc) is not None]

def remove_objects_from_xml(input_xml, output_xml, objects_to_remove):
    """
    Remove objects from an XML file based on a list of 'FULL CODE' values.
    """
    tree = ET.parse(input_xml)
    root = tree.getroot()

    # Find and remove matching ApplicationRoleObjectBind sections
    for application_role_object_bind in root.findall(".//ApplicationRoleObjectBind"):
        object_element = application_role_object_bind.find(".//Object")
        if object_element is not None and object_element.attrib.get("link:full_code") in objects_to_remove:
            root.find("ApplicationRoleObjectBinds").remove(application_role_object_bind)

    # Save the modified XML
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)
    print(f"Updated XML file saved to: {output_xml}")

def process_files(csv_file, files_to_process):
    """
    Process multiple XML files by removing objects based on the CSV file.
    """
    # Load the list of objects to remove from the CSV
    objects_to_remove = load_errors_from_csv(csv_file)
    print(f"Objects to remove: {len(objects_to_remove)} found.")

    for input_xml, output_xml in files_to_process:
        print(f"Processing file: {input_xml}")
        remove_objects_from_xml(input_xml, output_xml, objects_to_remove)

if __name__ == "__main__":
    # Input files
    csv_file_path = "export.csv"  # Path to your CSV file

    # List of XML files to process (input, output)
    files_to_process = [
        ("BUS_ROLE_BUS_UC_BASIC.xml", "BUS_ROLE_BUS_UC_BASIC_updated.xml"),
        ("BUS_ROLE_MER_OPERATOR.xml", "BUS_ROLE_MER_OPERATOR_updated.xml"),
    ]

    # Process the files
    process_files(csv_file_path, files_to_process)
