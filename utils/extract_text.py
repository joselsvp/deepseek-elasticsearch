import os
import fitz  # PyMuPDF para PDFs
import docx
import pandas as pd
from tika import parser

def extract_text(file_path):
    """ Extrae contenido de archivos PDF, DOCX, TXT, CSV, etc. """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        elif ext == ".docx":
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".csv":
            df = pd.read_csv(file_path)
            return df.to_string()
        else:
            parsed = parser.from_file(file_path)
            return parsed["content"]
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return None
