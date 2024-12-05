from xmlschema import XMLSchema

def generate_xsd_from_xml(xml_file, xsd_file):
    """
    Vygeneruje základní XSD schéma z XML souboru.
    """
    try:
        schema = XMLSchema.create_from(xml_file)
        with open(xsd_file, 'w') as file:
            file.write(schema.to_xml())
        print(f"XSD schéma bylo vygenerováno: {xsd_file}")
    except Exception as e:
        print(f"Chyba při generování XSD: {e}")

# Cesty k souborům
input_xml_path = "BUS_ROLE_BUS_UC_BASIC.xml"  # Nahraďte svou cestou k XML
xsd_file_path = "BUS_ROLE_BUS_UC_BASIC.xsd"  # Cesta pro uložení XSD

# Generování XSD
generate_xsd_from_xml(input_xml_path, xsd_file_path)
