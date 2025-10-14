import xml.etree.ElementTree as ET
from collections import defaultdict

def get_dashboard_hierarchy_with_fields(path):
    tree = ET.parse(path)
    root = tree.getroot()

    dashboards = defaultdict(dict)
    worksheets = defaultdict(set)

    # --- Step 1: Extract dashboards and worksheets ---
    for dashboard in root.findall(".//dashboard"):
        dash_name = (
            dashboard.attrib.get("caption")
            or dashboard.attrib.get("name")
            or "Unnamed Dashboard"
        )

        for zone in dashboard.findall(".//zone"):
            ws_name = zone.attrib.get("name")
            if not ws_name:
                continue
            dashboards[dash_name][ws_name] = []

    # --- Step 2: Extract worksheet field dependencies ---
    for worksheet in root.findall(".//worksheet"):
        ws_name = worksheet.attrib.get("name")
        if not ws_name:
            continue

        for field in worksheet.findall(".//column"):
            field_name = field.attrib.get("name")
            if field_name:
                worksheets[ws_name].add(field_name)

    # --- Step 3: Compute common and unique fields ---
    if worksheets:
        common_fields = set.intersection(*worksheets.values())
    else:
        common_fields = set()

    unique_fields = {}
    for ws, fields in worksheets.items():
        unique_fields[ws] = fields - common_fields

    # --- Step 4: Return everything ---
    return {
        "dashboards": dict(dashboards),
        "worksheets_fields": dict(worksheets),
        "common_fields": common_fields,
        "unique_fields": unique_fields
    }