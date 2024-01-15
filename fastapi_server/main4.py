# main.py
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from .database import get_db
from mysql.connector import Error
from azure.storage.blob import BlobServiceClient
import os
import datetime
import uuid

app = FastAPI()

BLOB_STORAGE_CONNECTION_STRING = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(CONTAINER_NAME)

class UploadedFile:
    def __init__(self, uid, filename, location, uploaded_at=None):
        self.uid = uid
        self.filename = filename
        self.location = location
        self.uploaded_at = uploaded_at or datetime.datetime.utcnow()

def generate_uid():
    return str(uuid.uuid4())

def get_blob_location(blob_container_client, uid):
    blob_name = uid  # Use UID as the blob name
    blob_url = blob_container_client.url + '/' + blob_name
    return blob_url

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), db=Depends(get_db)):

    uid = generate_uid()

    # Use UID as the blob name
    blob_location = get_blob_location(blob_container_client, uid)

    blob_client = blob_container_client.get_blob_client(blob_location)
    blob_client.upload_blob(file.file)

    # Access the filename directly from the UploadFile instance
    filename = file.filename

    connection, cursor = db
    try:
        cursor.execute("""
            INSERT INTO upload_record (uid, filename, location, uploaded_at) 
            VALUES (%s, %s, %s, %s)
        """, (uid, filename, blob_location, datetime.datetime.utcnow()))
        connection.commit()
    except Error as e:
        print(f"Error inserting data into 'upload_record' table: {e}")
    finally:
        cursor.close()

    return JSONResponse(content={"message": "File uploaded successfully", "uid": uid, "location": blob_location, "filename": filename})
