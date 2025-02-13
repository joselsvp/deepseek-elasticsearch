import os
import fitz  # PyMuPDF para PDFs
import docx
import pandas as pd
from tika import parser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_text(file_path, max_words=5000, max_summary_sentences=5, section_size=1000):
    """ Extrae contenido de archivos PDF, DOCX, TXT, CSV, etc., con límite de palabras y resúmenes. """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    try:
        text = ""
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == ".pdf":
            doc = fitz.open(file_path)
            text = "\n".join([page.get_text("text") for page in doc])
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".csv":
            df = pd.read_csv(file_path)
            text = df.to_string()
        else:
            parsed = parser.from_file(file_path)
            text = parsed["content"] if parsed["content"] else ""
        
        # 🔥 Dividir en secciones si el contenido es demasiado largo
        words = text.split()
        sections = []
        if len(words) > max_words:
            for i in range(0, len(words), section_size):
                sections.append(" ".join(words[i:i+section_size]))
            text = " ".join(words[:max_words]) + "... [Contenido truncado]"
        else:
            sections.append(text)
        
        # 🔥 Generar un resumen automático
        parser = PlaintextParser.from_string(text, Tokenizer("spanish"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, max_summary_sentences)
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
        return {
            "full_text": text if text.strip() else None,
            "sections": sections if sections else None,
            "summary": summary if summary.strip() else None
        }
    
    except Exception as e:
        print(f"❌ Error procesando {file_path}: {e}")
        return None
