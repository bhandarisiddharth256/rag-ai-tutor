from PyPDF2 import PdfReader

def extract_text(file_path):
    reader = PdfReader(file_path)

    # 🔥 Handle encrypted PDF
    if reader.is_encrypted:
        reader.decrypt("")  # try empty password

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text