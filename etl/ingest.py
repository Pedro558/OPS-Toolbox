from pathlib import Path
import pandas as pd

# Adjust as needed to point to project root
BASE_DIR = Path(__file__).resolve().parents[1]  
DEFAULT_INVENTORY_PATH = BASE_DIR / "data" / "raw" / "inventory_rjo1.xlsx"

def load_inventory(path: str | Path = DEFAULT_INVENTORY_PATH) -> pd.DataFrame:
    
    """Load inventory data from an Excel file"""
    return pd.read_excel(path)

