import pandas as pd

def format_inventory_cables(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  
  # Identifica linhas "título do material"
  is_header = df["quantity"].isna() & df["min_quantity"].isna() & df["cable_length"].notna()

  # Cria nova coluna de 'material'
  df["material"] = df["cable_length"].where(is_header)
  df["material"] = df["material"].ffill()

  # Identificar a última linha do material 'cable'
  mask_last_cable = df["material"].astype("string").str.contains("cord", case=False, na=False)
  last_index = df[mask_last_cable].index[-1]

  # Criar novo DataFrame somente com cabos
  inventory_cables = df.iloc[0:last_index]

  # Novo DataFrame com os outros materiais

  # Remove 'metros' from 'cable_length' column and convert to float
  cable_length_raw = inventory_cables["cable_length"].where(~is_header)
  cable_length_num = (
    cable_length_raw.astype("string")
    .str.lower()
    .str.replace('metros', '', regex=False)
    .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
  )

  inventory_cables["cable_length"] = pd.to_numeric(cable_length_num, errors="coerce")

  # Nova ordem de colunas
  inventory_cables_reordered = inventory_cables.loc[:, ['material', 'cable_length', 'quantity', 'min_quantity']]


  # TO-DO
  # Excluir a linha com o header duplicado; Identificar a última linha com valores de cabo; Separar tabela de cabos e de materiais; Retirar NaN; Retirar a palavra 'metros' da coluna 'cable_length'; 

  return inventory_cables_reordered