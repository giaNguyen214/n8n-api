import fitz  # PyMuPDF

def check_pdf_valid(path):
    try:
        doc = fitz.open(path)
        return "True" if doc.page_count > 0 else "False"
    except Exception:
        return False
