from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from .database import SessionLocal, engine, UploadedFile
from sqlalchemy.orm import Session
from azure.storage.blob import BlobServiceClient
import os
import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

BLOB_STORAGE_CONNECTION_STRING = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.get("/")
async def root():
    return {"message": "This is resume enhancement system"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    blob_name = file.filename
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.file)

    db_file = UploadedFile(filename=blob_name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return JSONResponse(content={"message": "File uploaded successfully", "file_id": db_file.id})
