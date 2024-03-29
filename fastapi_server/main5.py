# main.py
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Body
from fastapi.responses import StreamingResponse
from .database import get_db
from azure.storage.blob import BlobServiceClient
import os
import datetime
import uuid
from mysql.connector import Error

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

class Conversation:
    def __init__(self, uid, content, created_date=None, updated_date=None):
        self.uid = uid
        self.content = content
        self.created_date = created_date or datetime.datetime.utcnow()
        self.updated_date = updated_date or datetime.datetime.utcnow()

def generate_uid():
    return str(uuid.uuid4())

def get_blob_location(container_name, uid):
    blob_name = uid  # Use UID as the blob name
    return f"{container_name}/{blob_name}"

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), db=Depends(get_db)):
    uid = generate_uid()

    # Use UID as the blob name
    blob_location = get_blob_location(CONTAINER_NAME, uid)

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

    return {"message": "File uploaded successfully", "uid": uid, "location": blob_location, "filename": filename}

@app.get("/get_file/{uid}")
async def get_file_by_uid(uid: str, db=Depends(get_db)):
    # Retrieve the blob location for the given UID from the database
    cursor = db[1]
    cursor.execute("SELECT location FROM upload_record WHERE uid = %s", (uid,))
    result = cursor.fetchone()

    if result:
        blob_location = result["location"]

        # Assuming you have the appropriate Azure Blob Storage SDK to download the blob
        blob_client = blob_container_client.get_blob_client(blob_location)
        content = blob_client.download_blob().readall()

        # For demonstration purposes, let's assume content is a bytes-like object
        return StreamingResponse(iter([content]), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={uid}"})
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/save_conversation/")
async def save_conversation(conversation_uid: str = Body(...), chat_content_result: str = Body(...), db=Depends(get_db)):
    # Check if the conversation UID already exists
    cursor = db[1]
    cursor.execute("SELECT * FROM conversations WHERE uid = %s", (conversation_uid,))
    existing_conversation = cursor.fetchone()

    if existing_conversation:
        # Update existing conversation
        cursor.execute("""
            UPDATE conversations 
            SET content = %s, updated_date = %s
            WHERE uid = %s
        """, (chat_content_result, datetime.datetime.utcnow(), conversation_uid))
    else:
        # Create a new conversation
        cursor.execute("""
            INSERT INTO conversations (uid, content, created_date, updated_date) 
            VALUES (%s, %s, %s, %s)
        """, (conversation_uid, chat_content_result, datetime.datetime.utcnow(), datetime.datetime.utcnow()))

    # Commit changes to the database
    db[0].commit()

    return {"message": "Conversation saved successfully"}

@app.get("/get_conversation/{uid}")
async def get_conversation_by_uid(uid: str, db=Depends(get_db)):
    # Retrieve the conversation content for the given UID from the database
    cursor = db[1]
    cursor.execute("SELECT content FROM conversations WHERE uid = %s", (uid,))
    result = cursor.fetchone()

    if result:
        conversation_content = result["content"]
        return {"uid": uid, "content": conversation_content}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")
