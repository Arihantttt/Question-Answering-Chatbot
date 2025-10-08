from tableauhyperapi import HyperProcess, Connection, TableName

with HyperProcess() as hyper:
    with Connection(endpoint=hyper.endpoint, database="path/to/file.hyper") as connection:
        tables = connection.catalog.get_table_names("Extract")
        print("Tables:", tables)
        
        for table in tables:
            rows = connection.execute_query(f"SELECT * FROM {table}")
            for row in rows:
                print(row)



import xml.etree.ElementTree as ET
from tableauhyperapi import HyperProcess, Connection, Telemetry

# --- Step 1: Read .twb XML ---
tree = ET.parse("Workbook.twb")
root = tree.getroot()

filters = []
for f in root.findall(".//filter"):
    if "value" in f.attrib:
        filters.append(f.attrib["value"])
print("Filters found:", filters)

# --- Step 2: Query .hyper ---
with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(endpoint=hyper.endpoint, database="Data/Extracts/Extract.hyper") as conn:
        result = conn.execute_query("""
            SELECT SUM(Sales)
            FROM Extract.Extract1
            WHERE Region = 'East'
        """)
        print("KPI Value (Total Sales):", [r for r in result])
