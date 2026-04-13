from fastapi import APIRouter, UploadFile, File
import os
import uuid
from services.pdf_service import extract_text
from services.rag_service import chunk_text, store_embeddings

router = APIRouter()

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # ✅ Validate file type
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files allowed"}

    # ✅ Unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ✅ Extract text
    text = extract_text(file_path)

    print("----- Extracted Text -----")
    print(text[:500])
    print("TEXT LENGTH:", len(text))
    chunks = chunk_text(text)
    store_embeddings(chunks)

    print("Chunks stored:", len(chunks))
    # ✅ Handle empty text
    if not text.strip():
        return {"message": "PDF uploaded but no readable text found"}

    return {
        "message": "File uploaded & processed",
        "filename": unique_name
    }