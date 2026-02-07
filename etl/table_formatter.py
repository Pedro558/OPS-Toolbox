import pandas as pd

def find_last_cable_index(df: pd.DataFrame) -> pd.DataFrame:
  # Identify the last line from 'cable' material
  mask_last_cable = df["material"].astype("string").str.contains("cord", case=False, na=False)
  last_index = df[mask_last_cable].index[-1]
  
  return last_index

def format_inventory_cables(df: pd.DataFrame) -> pd.DataFrame:
  last_index = find_last_cable_index(df)

  # Find header rows
  is_header = df["quantity"].isna() & df["min_quantity"].isna() & df["cable_length"].notna()

  # Create new DF only with 'cables'
  inventory_cables = df.iloc[0:last_index]

  # Remove 'metros' from 'cable_length' column and convert to float
  cable_length_raw = inventory_cables["cable_length"].where(~is_header)
  cable_length_num = (
    cable_length_raw.astype("string")
    .str.lower()
    .str.replace('metros', '', regex=False)
    .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
  )

  inventory_cables["cable_length"] = pd.to_numeric(cable_length_num, errors="coerce")

  column_order = ['material', 'cable_length', 'quantity', 'min_quantity']
  inventory_cables = inventory_cables[column_order]

  return inventory_cables

def format_inventory_materials(df: pd.DataFrame) -> pd.DataFrame:
  last_index = find_last_cable_index(df)
    
  # Identify the last line from 'cable' material
  mask_last_cable = df["material"].astype("string").str.contains("cord", case=False, na=False)
  last_index = df[mask_last_cable].index[-1]

  # New DF with other materials
  inventory_materials = df.iloc[last_index+1:]
  inventory_materials = inventory_materials.rename(columns={
  "material": "material_group",
  "cable_length": "material"
})
  
  column_order = ['material_group', 'material', 'quantity', 'min_quantity']
  inventory_materials = inventory_materials[column_order]

  return inventory_materials