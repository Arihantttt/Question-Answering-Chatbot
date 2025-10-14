import xml.etree.ElementTree as ET
from collections import defaultdict

def get_dashboard_hierarchy(path):
    tree = ET.parse(path)
    root = tree.getroot()
    dashboards = defaultdict(dict)

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
            worksheets = root.findall(f".//worksheet[@name='{ws_name}']")

            for ws in worksheets:
                for col in ws.findall(".//column"):
                    # Extract KPI name
                    kpi_name = col.attrib.get("caption") or col.attrib.get("name")

                    # Skip blank or None
                    if not kpi_name or kpi_name.strip() == "":
                        continue

                    # Handle calculated fields: append actual formula name
                    calc = col.find("calculation")
                    if calc is not None:
                        formula = calc.attrib.get("formula")
                        if formula:
                            kpi_name = f"{kpi_name} ({formula})"

                    # Skip duplicates
                    if kpi_name not in dashboards[dash_name][ws_name]:
                        dashboards[dash_name][ws_name].append(kpi_name)

    # Convert defaultdict → normal dict
    return {dash: dict(ws) for dash, ws in dashboards.items()}