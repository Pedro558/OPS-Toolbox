# OPS Toolbox
OPS Toolbox is a lightweight Python project that ingests raw Excel inventory exports, applies a set of cleaning and formatting helpers, and exposes a FastAPI service to inspect the processed output.

## Key pieces
- `data/raw`: source inventories (currently `inventory_rjo1.xlsx`), intended as the single canonical upload.
- `etl`: helper modules (`ingest`, `clean`, `formatter`, `validate`) to read the workbook, normalize column names, drop redundant rows, and reshape the cable inventory before writing to `data/processed`.
- `api.app`: FastAPI application with `/health` and `/checkProcessedFiles` endpoints for quick operational checks.

## Getting started
1. Create and activate a virtual environment (`python -m venv .venv && .venv\\Scripts\\activate` on Windows).
2. Install Python dependencies: `pip install -r requirements.txt`.
3. Place any new inventory exports under `data/raw` following the naming convention so helpers can locate them.

### Running the API
- Direct: `uvicorn api.app:app --reload --port 8000`
- Via npm script (Node/npm already installed): `npm run start:api` (uses the same `uvicorn` command).

### Working with the ETL helpers
```python
from etl.ingest import load_inventory
from etl import clean, formatter

df = load_inventory()
df = clean.remove_first_row(df)
df = clean.rename_inventory_columns(df)
df = clean.remove_empty_values(df)
df = formatter.format_inventory_cables(df)
```

Pair the formatter with additional cleaning/validation functions before writing back to `data/processed` for API visibility.

## API contract
| Endpoint | Description |
| -------- | ----------- |
| `GET /health` | Returns `{"message": "Service running"}` when the service is up. |
| `GET /checkProcessedFiles` | Lists files and sizes inside `data/processed`; returns an empty list if the directory does not exist. |

## Next steps
- Implement a dedicated pipeline runner that sequences the ETL helpers and writes to `data/processed`.
- Add automated tests for the ETL helpers and API.
