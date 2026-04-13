from fastapi import APIRouter, UploadFile, File
import os
from services.pdf_service import extract_text

router = APIRouter()

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 🔥 NEW: extract text
    text = extract_text(file_path)

    print("----- Extracted Text -----")
    print(text[:500])  # print first 500 chars

    return {
        "message": "File uploaded & processed",
        "filename": file.filename
    }