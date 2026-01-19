# backend/utils.py
import pdfplumber
import docx2txt
from fastapi import UploadFile

def extract_text_from_file(file: UploadFile) -> str:
    """Extracts text from PDF, DOCX, or TXT files."""
    text = ""
    filename = file.filename.lower()
    
    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
        elif filename.endswith(".docx") or filename.endswith(".doc"):
            text = docx2txt.process(file.file)
        elif filename.endswith(".txt"):
            text = file.file.read().decode("utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
    
    return text.strip()