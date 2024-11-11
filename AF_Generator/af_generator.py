import pandas as pd

pd.set_option('display.max_rows', None)
df = pd.read_excel("data.xlsx", sheet_name="main")

# potreba si nagenerovat sablony pro jednotlive kombinace
# reseni - staci danou funkcionalitu zavolat pro kazdy sheet opakovane zvlast
# potom pridat rozhodovaci logiku kdy jakou sobalonu pouzit 


fileIteration = 0

for index, row in df.iterrows():
    # columns 
    af_name = row['$AF_NAME']
    af_opt_name1 = row['$AF_OPT_NAME1']
    af_opt_name2 = row['$AF_OPT_NAME2']
    af_time_dimension = row['$TIME_DIMENSION']

    def addBusinessDimension(n):
            result = ""
            for _ in range(n):  # Přidá 'businessDimension' N-krát
                result += businessDimensions
            return result

        # Příklad použití: přidá 'businessDimension'


    def addOptionalTimeSeries(n):
            result = ""
            for _ in range(n):  # Přidá 'optionalTime Series' N-krát
                result += optionalTimeSeries
            return result

    

    # global variables - template - 1 td, 1 bd, 2 ts - tuhle cast nacitat z jineho souboru 
    static = """<?xml version="1.0" encoding="utf-8"?>
<AccessTimeseriesSet template_version="6.7" full_code="$AF_TS_FULL_CODE" soid="" xmlns:link="urn:eu:damas:metadata:link" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ObjectProperties>
    <Name culture="en-US">$AF_NAME</Name>
    <ShortName culture="en-US" />
    <Annotation culture="en-US" />
    <Parent link:full_code="$AF_PARENT_FULL_CODE" link:soid="" />
    <ObjectClass link:code="BUL" />
    <Order />
  </ObjectProperties>
  <Dimensions>"""
    timeDimension = """<TimeDimension link:dim_code="$TIME_DIMENSION" />"""
    businessDimensions = """<BusinessDimension dimension_type="CODE_TABLE" link:dim_code="$BUSINESS_DIMENSION" alias_code="">
  <AliasName culture="en-US" />
  <AliasShortName culture="en-US" />
  <Order>1</Order>
</BusinessDimension>"""
    mainTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_MAIN_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_MAIN_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_MAIN_TIME_SERIES_ALIAS</Alias>
      <Type>MAIN</Type>
      <ColName>$MAIN_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""
    optionalTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_OPT_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_OPT_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_OPT_TIME_SERIES_ALIAS</Alias>
      <Type>OPT</Type>
      <ColName>$OPT_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""
    # replace function 
    timeDimension = timeDimension.replace("$TIME_DIMENSION", af_time_dimension) 

    static = static.replace("$AF_NAME", af_name)
    optionalTimeSeries= addOptionalTimeSeries(1)
    optionalTimeSeries = optionalTimeSeries.replace("$AF_OPT_NAME", af_opt_name1)
    #optionalTimeSeries = optionalTimeSeries.replace("$AF_OPT_NAME", af_opt_name2)

    
    
    
    finalXML = static + timeDimension + businessDimensions + mainTimeSeries + optionalTimeSeries
    # generate function
    filename = f'file{fileIteration}.xml'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(finalXML)
        fileIteration += 1

        

# algoritmus description
# nacti soubor z excelu 
# zapamatuj si promene v jednotlivych sloupcich
# zjisti pocet radku 
'''
static = """<?xml version="1.0" encoding="utf-8"?>
<AccessTimeseriesSet template_version="6.7" full_code="$AF_TS_FULL_CODE" soid="" xmlns:link="urn:eu:damas:metadata:link" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ObjectProperties>
    <Name culture="en-US">$AF_NAME</Name>
    <ShortName culture="en-US" />
    <Annotation culture="en-US" />
    <Parent link:full_code="$AF_PARENT_FULL_CODE" link:soid="" />
    <ObjectClass link:code="BUL" />
    <Order />
  </ObjectProperties>
  <Dimensions>"""

timeDimension = """<TimeDimension link:dim_code="$TIME_DIMENSION" />"""

businessDimension = """<BusinessDimension dimension_type="CODE_TABLE" link:dim_code="$BUSINESS_DIMENSION" alias_code="">
  <AliasName culture="en-US" />
  <AliasShortName culture="en-US" />
  <Order>1</Order>
</BusinessDimension>"""

mainTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_MAIN_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_MAIN_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_MAIN_TIME_SERIES_ALIAS</Alias>
      <Type>MAIN</Type>
      <ColName>$MAIN_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""

optionalTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_OPT_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_OPT_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_OPT_TIME_SERIES_ALIAS</Alias>
      <Type>OPT</Type>
      <ColName>$OPT_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""

# Funkce pro přidání businessDimension N-krát



def iterate_dataframe(df, num_rows, num_columns):
    # Ensure the number of rows and columns doesn't exceed the DataFrame's dimensions
    num_rows = min(num_rows, len(df))
    num_columns = min(num_columns, len(df))
    
    # Iterate over the specified number of rows
    for i in range(num_rows):
        # Create an empty list to store values from the current row
        row_values = []
        # Iterate over the specified number of columns
        for j in range(num_columns):
            # Add the value from the current row and column to the list
            row_values.append(df.iloc[i, j])
        # Print the row index and the values from the row
        print(f'Row {i}:', row_values)
# najdi pocet optional time series + najdi pocet dimenzi
# sloz xml strukturu
# napl xml strukturu promenymi z jednoho radku
# potom cely postup opakuj 
#iterate_dataframe(df, 5000,2000)

finalXML = static + timeDimension + businessDimensions + mainTimeSeries + optionalTimeSeries

print(finalXML)

# vytvor soubor



# EXPORT LOGIC 
# Path to the Excel file
excel_file = 'data.xlsx'

# Ensure the Output directory exists
output_dir = 'Output'
os.makedirs(output_dir, exist_ok=True)

# Initialize logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Open the Excel file
wb = openpyxl.load_workbook(excel_file)
sheet = wb.active  # Assuming we are working with the first sheet

# Iterate through all rows in the first column
for i, row in enumerate(sheet.iter_rows(min_col=1, max_col=1, min_row=1, values_only=True), start=1):
    xml_content = row[0]  # Cell content
    if xml_content:  # Check if the cell is not empty
        # Create an XML file for each row
        file_path = os.path.join(output_dir, f'file_{i}.xml')
        with open(file_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_content)
        # Log that the file has been saved
        logging.info(f'File saved: {file_path}')

wb.close()  # Close the Excel file after completion

# Zipping the Output folder
zip_file_name = 'Output.zip'
with ZipFile(zip_file_name, 'w') as zipf:
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(output_dir, '..')))

# Log the completion of zipping
logging.info(f'Output folder zipped into {zip_file_name}')
'''

df = pd.read_excel("data.xlsx", sheet_name="1BD2TS")

for index, row in df.iterrows():
    # columns 
    af_name = row['$AF_NAME']
    af_opt_name1 = row['$AF_OPT_NAME1']
    af_opt_name2 = row['$AF_OPT_NAME2']
    af_time_dimension = row['$TIME_DIMENSION']

    def addBusinessDimension(n):
            result = ""
            for _ in range(n):  # Přidá 'businessDimension' N-krát
                result += businessDimensions
            return result

        # Příklad použití: přidá 'businessDimension'


    def addOptionalTimeSeries(n):
            result = ""
            for _ in range(n):  # Přidá 'optionalTime Series' N-krát
                result += optionalTimeSeries
            return result

    

    # global variables
    static = """<?xml version="1.0" encoding="utf-8"?>
<AccessTimeseriesSet template_version="6.7" full_code="$AF_TS_FULL_CODE" soid="" xmlns:link="urn:eu:damas:metadata:link" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ObjectProperties>
    <Name culture="en-US">$AF_NAME</Name>
    <ShortName culture="en-US" />
    <Annotation culture="en-US" />
    <Parent link:full_code="$AF_PARENT_FULL_CODE" link:soid="" />
    <ObjectClass link:code="BUL" />
    <Order />
  </ObjectProperties>
  <Dimensions>"""
    timeDimension = """<TimeDimension link:dim_code="$TIME_DIMENSION" />"""
    businessDimensions = """<BusinessDimension dimension_type="CODE_TABLE" link:dim_code="$BUSINESS_DIMENSION" alias_code="">
  <AliasName culture="en-US" />
  <AliasShortName culture="en-US" />
  <Order>1</Order>
</BusinessDimension>"""
    mainTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_MAIN_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_MAIN_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_MAIN_TIME_SERIES_ALIAS</Alias>
      <Type>MAIN</Type>
      <ColName>$MAIN_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""
    optionalTimeSeries = """ </Dimensions>
  <Permissions>
    <DefaultAccessMode link:full_code="\\SS_SYS\\SS_SYS_PERMISSIONS\\INTERNAL_LOCAL_WRITE_ACTIVE_READ" link:soid="" />
  </Permissions>
  <DBViewName>$AF_OPT_NAME</DBViewName>
  <TimeseriesList>
    <Timeseries link:full_code="$AF_OPT_TIME_SERIES_CODE" link:soid="">
      <Alias>$AF_OPT_TIME_SERIES_ALIAS</Alias>
      <Type>OPT</Type>
      <ColName>$OPT_COLUMN_NAME</ColName>
      <ShowValueState>true</ShowValueState>
      <ShowValueCorrection>false</ShowValueCorrection>
      <FilterDeleted>false</FilterDeleted>
      <ShowModificationInformation>false</ShowModificationInformation>
      <DimensionsMapping>
        <MappingType link:code="AUTOMATIC" />
      </DimensionsMapping>
    </Timeseries>"""
    # replace function 
    timeDimension = timeDimension.replace("$TIME_DIMENSION", af_time_dimension) 

    static = static.replace("$AF_NAME", af_name)
    ### tady se lisi inkrement podle poctu casovych rad a dimenzi - NE takhle to nepujde, bude potreba použít opravdu jiné šablony

    # mozna bude lepsi nacitat obsah sablony (xml) a do neho pak doplnovat promene 
    optionalTimeSeries= addOptionalTimeSeries(1)
    optionalTimeSeries = optionalTimeSeries.replace("$AF_OPT_NAME", af_opt_name1)
    #optionalTimeSeries = optionalTimeSeries.replace("$AF_OPT_NAME", af_opt_name2)

    
    
    
    finalXML = static + timeDimension + businessDimensions + mainTimeSeries + optionalTimeSeries
    # generate function
    filename = f'file{fileIteration}.xml'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(finalXML)
        fileIteration += 1