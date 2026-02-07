from pathlib import Path

import pandas as pd
import clean 
from ingest import load_inventory
import table_formatter 

PROCESSED_FOLDER = Path(__file__).resolve().parents[1] / "data" / "processed"

df = load_inventory()
df_cleaned = clean.remove_first_row(df)
df_cleaned = clean.rename_inventory_columns(df_cleaned)
df_cleaned = clean.remove_status_column(df_cleaned)
df_cleaned = clean.convert_inventory_types(df_cleaned)
df_cleaned = clean.create_material_column(df_cleaned)

cable_inventory = table_formatter.format_inventory_cables(df_cleaned)
cable_inventory_clean = clean.remove_empty_values(cable_inventory)

inventory_materials = table_formatter.format_inventory_materials(df_cleaned)
inventory_materials_clean = clean.remove_empty_values(inventory_materials)



cable_inventory_clean.to_excel(PROCESSED_FOLDER /"rjo1" / "cable_inventory_clean.xlsx", index=False)
inventory_materials_clean.to_excel(PROCESSED_FOLDER /"rjo1" / "inventory_materials_clean.xlsx", index=False)


