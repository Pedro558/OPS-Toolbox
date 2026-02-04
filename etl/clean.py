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
  df = df.dropna(how="all")
  
  """Replace 'Missing Values' with the ' - ' symbol """
  #df = df.fillna(" - ")
  return df

def convert_inventory_types(df: pd.DataFrame) -> pd.DataFrame:
  """Change inventory column types"""
  df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
  df["min_quantity"] = pd.to_numeric(df["min_quantity"], errors="coerce")
  
  #df = df.astype({
  #  "quantity": 'int64',
  #  "min_quantity": 'int64'})
  
  return df