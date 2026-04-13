from PyPDF2 import PdfReader

def extract_text(file_path):
    try:
        reader = PdfReader(file_path)

        if reader.is_encrypted:
            reader.decrypt("")

        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        return text

    except Exception as e:
        print("PDF extraction error:", e)
        return ""