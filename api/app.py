from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

class HealthCheckResponse(BaseModel):
  message: str

@app.get("/health", response_model=HealthCheckResponse)
async def root():
  return HealthCheckResponse(message='Service running')

class CheckProcessedFiles(BaseModel):
  files_count: int
  files: list[dict[str, str | int]]

@app.get("/checkProcessedFiles", response_model=CheckProcessedFiles)
async def check_processed_files():
  processed_dir = PROCESSED_DIR
  
  if not processed_dir.exists():
    return CheckProcessedFiles(files_count=0, files=[])
  
  files=[{
    "file_name": f.name,
    "file_size": f.stat().st_size
  } for f in processed_dir.iterdir() if f.is_file()]

  return CheckProcessedFiles(files_count=len(files), files=[f for f in files])
