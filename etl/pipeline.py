from pathlib import Path
from . import clean 
from .ingest import load_inventory
from . import table_formatter as formatter

PROCESSED_FOLDER = Path(__file__).resolve().parents[1] / "data" / "processed"
OUT_DIR = PROCESSED_FOLDER / "rjo1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def run()-> None:
  df = load_inventory()
  df_cleaned = clean.rename_inventory_columns(df)
  df_cleaned = clean.remove_status_column(df_cleaned)
  df_cleaned = clean.convert_inventory_types(df_cleaned)
  df_cleaned = clean.create_material_column(df_cleaned)

  cable_inventory = formatter.format_inventory_cables(df_cleaned)
  cable_inventory_clean = clean.remove_empty_values(cable_inventory)

  inventory_materials = formatter.format_inventory_materials(df_cleaned)
  inventory_materials_clean = clean.remove_empty_values(inventory_materials)

  cables_path = OUT_DIR / "cable_inventory_clean.xlsx"
  materials_path = OUT_DIR / "inventory_materials_clean.xlsx"

  cable_inventory_clean.to_excel(cables_path, index=False)
  inventory_materials_clean.to_excel(materials_path, index=False)

  return cables_path, materials_path


if __name__ == "__main__":
    run()

# Command to execute this folder: python -m etl.pipeline




