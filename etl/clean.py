import pandas as pd

def remove_first_row(df: pd.DataFrame) -> pd.DataFrame:
  """Remove the first row of the DataFrame"""
  return df.iloc[1:]

def rename_inventory_columns(df: pd.DataFrame) -> pd.DataFrame:
  """Rename inventory's Dataframe columns to standard names"""
  df = df.rename(columns={
    "MATERIAIS": "cable_length",
    "QNTD. EM ESTOQUE": "quantity",
    "ESTOQUE MÍNIMO": "min_quantity",
    "STATUS": "status"
  })
  return df

def remove_status_column(df: pd.DataFrame) -> pd.DataFrame:
  df = df.drop(columns=['status'])
  return df

def remove_empty_values(df: pd.DataFrame) -> pd.DataFrame:
  """Remove all rows with empty values in all columns"""
  df = df.dropna()
  return df

def convert_inventory_types(df: pd.DataFrame) -> pd.DataFrame:
  """Change inventory column types"""
  df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
  df["min_quantity"] = pd.to_numeric(df["min_quantity"], errors="coerce")

  for col in ["quantity", "min_quantity"]:
    if col in df.columns:
    # Se todas as partes decimais forem .0, converte para inteiro nullable
      if (df[col].dropna() % 1 == 0).all():
        df[col] = df[col].astype("Int64")

  return df

def create_material_column(df: pd.DataFrame) -> pd.DataFrame:
  """Create a new 'material' column based on the 'cable_length' values"""
  df = df.copy()
  
  is_header = df["quantity"].isna() & df["min_quantity"].isna() & df["cable_length"].notna()

  df["material"] = df["cable_length"].where(is_header)
  df["material"] = df["material"].ffill()

  return df