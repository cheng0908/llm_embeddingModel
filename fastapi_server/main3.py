# main.py
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from .database import get_db
from mysql.connector import Error
from azure.storage.blob import BlobServiceClient
import os
import datetime

app = FastAPI()

BLOB_STORAGE_CONNECTION_STRING = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(CONTAINER_NAME)

class UploadedFile:
    def __init__(self, filename, uploaded_at=None):
        self.id = None  # Assuming the database will auto-generate IDs
        self.filename = filename
        self.uploaded_at = uploaded_at or datetime.datetime.utcnow()

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), db=Depends(get_db)):

    blob_name = file.filename
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.file)

    db_file = UploadedFile(filename=blob_name)

    # Inserting data into the MySQL database
    try:
        db.execute("""
            INSERT INTO uploaded_files (filename, uploaded_at) 
            VALUES (%s, %s)
        """, (db_file.filename, db_file.uploaded_at))
        db.commit()
    except Error as e:
        print(f"Error inserting data into 'uploaded_files' table: {e}")

    return JSONResponse(content={"message": "File uploaded successfully"})
