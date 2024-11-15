import json
import re
import os
import zipfile
import xml

# Načtení JSON dat
with open("variables_list.json", "r", encoding="utf-8") as json_file:
    data_list = json.load(json_file)

# XML šablona jako string
xml_template = """<?xml version="1.0" encoding="utf-8"?>
<AccessTimeseriesSet template_version="7.0" full_code="$AF_TS_FULL_CODE" soid="" xmlns:link="urn:eu:damas:metadata:link" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ObjectProperties>
    <Name culture="en-US">$AF_NAME</Name>
    <ShortName culture="en-US" />
    <Annotation culture="en-US" />
    <Parent link:full_code="$AF_PARENT_FULL_CODE" link:soid="" />
    <ObjectClass link:code="BUL" />
    <Order />
  </ObjectProperties>
  <Dimensions>
    <TimeDimension link:dim_code="$AF_TIME_DIMENSION" />
    <BusinessDimension dimension_type="CODE_TABLE" link:dim_code="$BUSINESS_DIMENSION_1" alias_code="">
      <AliasName culture="en-US" />
      <AliasShortName culture="en-US" />
      <Order>0</Order>
    </BusinessDimension>
  </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_DB_VIEW_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_MAIN_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_MAIN_TIME_SERIES_ALIAS</Alias>
      <Type>MAIN</Type>
      <ColName>$AF_MAIN_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>
  </TimeseriesList>
</AccessTimeseriesSet>
"""

# Funkce pro nahrazení proměnných v XML šabloně
def replace_variables(template, variables):
    for key, value in variables.items():
        template = template.replace(key, value)
    return template

# Vytvoření složky pro výstupní XML soubory
output_folder = "output_xml_files"
os.makedirs(output_folder, exist_ok=True)

# Vygenerování XML souborů na základě dat v JSON
for idx, data in enumerate(data_list, start=1):
    xml_content = replace_variables(xml_template, data)
    output_file_path = os.path.join(output_folder, f"output_{idx}.xml")
    with open(output_file_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)

# Zazipování všech souborů ve složce output_xml_files do import.zip
zip_file_name = "import.zip"
with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, output_folder))

print(f"Všechny soubory byly úspěšně vygenerovány a zazipovány do '{zip_file_name}'")
