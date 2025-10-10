import xml.etree.ElementTree as ET
from collections import defaultdict

def get_dashboard_hierarchy(twb_path):
    tree = ET.parse(twb_path)
    root = tree.getroot()

    dashboards = defaultdict(dict)

    # Loop through dashboards
    for dashboard in root.findall(".//dashboard"):
        dash_name = (
            dashboard.attrib.get("caption")
            or dashboard.attrib.get("name")
            or "Unnamed Dashboard"
        )

        # Loop through zones (worksheets inside dashboards)
        for zone in dashboard.findall(".//zone"):
            ws_name = zone.attrib.get("name")
            if not ws_name:
                continue

            dashboards[dash_name][ws_name] = []

            # Get all worksheets with that name
            worksheets = root.findall(f".//worksheet[@name='{ws_name}']")
            for ws in worksheets:
                # Find all columns inside worksheet
                for col in ws.findall(".//column"):
                    field_info = {}
                    field_info["caption"] = col.attrib.get("caption")
                    field_info["name"] = col.attrib.get("name")

                    # Default type
                    field_info["type"] = "Unknown"

                    # Check role
                    if "role" in col.attrib:
                        if col.attrib["role"] == "dimension":
                            field_info["type"] = "Dimension"
                        elif col.attrib["role"] == "measure":
                            field_info["type"] = "Measure"

                    # Check if calculated
                    if col.find("calculation") is not None:
                        field_info["type"] = "Calculated Field"

                    # Check if parameter
                    if "param-domain-type" in col.attrib:
                        field_info["type"] = "Parameter"

                    dashboards[dash_name][ws_name].append(field_info)

    return dashboards


# Example usage
if __name__ == "__main__":
    path = "your_file.twb"
    hierarchy = get_dashboard_hierarchy(path)

    for dash, worksheets in hierarchy.items():
        print(f"📊 Dashboard: {dash}")
        for ws, fields in worksheets.items():
            print(f"   📄 Worksheet: {ws}")
            for f in fields:
                print(f"      🔹 {f['caption'] or f['name']} ({f['type']})")
