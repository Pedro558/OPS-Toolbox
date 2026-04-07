import pandas as pd
import numpy as np

def find_last_cable_position(df: pd.DataFrame) -> int:
  """Identify the last line from 'cable' material"""
  mask_last_cable = df["material"].astype("string").str.contains("cord", case=False, na=False)

  positions = np.flatnonzero(mask_last_cable)
  if len(positions) > 0:
    last_position = positions[-1]
  else: 
    last_position = None
    raise ValueError("No 'cable' materials found in the DataFrame.")
  
  return last_position

def format_inventory_cables(df: pd.DataFrame) -> pd.DataFrame:
  """Format inventory DataFrame to only include 'cable' materials with standardized columns and types"""
  last_position = find_last_cable_position(df)

  is_header = df["quantity"].isna() & df["min_quantity"].isna() & df["cable_length"].notna()

  inventory_cables = df.iloc[:last_position + 1].copy()

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
  """Format inventory DataFrame to only include 'non-cable' materials with standardized columns and types"""
  last_position = find_last_cable_position(df)

  inventory_materials = df.iloc[last_position + 1:].copy()
  inventory_materials = inventory_materials.rename(columns={
  "material": "material_group",
  "cable_length": "material"
})
  
  column_order = ['material_group', 'material', 'quantity', 'min_quantity']
  inventory_materials = inventory_materials[column_order]

  return inventory_materials