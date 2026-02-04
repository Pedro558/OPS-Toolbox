import pandas as pd

def validate_inventory_columns(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """Validate that the DataFrame contains all required columns"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return True