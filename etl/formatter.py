import pandas as pd

def format_inventory_cables(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  
  
  #1) Identifica linhas "título do material"
  is_header = df["quantity"].isna() & df["min_quantity"].isna() & df["cable_length"].notna()

  #2) Identificar a última linha com 'metros' no material
  #mask_metros = df["material"].astype("string").str.contains("metros", case=False, na=False)
  #last_index = df[mask_metros].index[-1]

  #3) Criar novo DataFrame somente com cabos
  #inventory_cables = df.iloc[0:last_index]

  #4) Cria nova coluna de grupo
  df["material"] = df["cable_length"].where(is_header)
  df["material"] = df["material"].ffill()

  #5) Nova ordem de colunas
  df_reordered = df.loc[:, ['material', 'cable_length', 'quantity', 'min_quantity']]

  # TO-DO
  # Excluir a linha com o header duplicado; Identificar a última linha com valores de cabo; Separar tabela de cabos e de materiais; Retirar NaN; Retirar a palavra 'metros' da coluna 'cable_length'; 

  return df_reordered