from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import uuid
import os

app = Flask(__name__)

def is_scanned_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        scanned_pages = sum(1 for i in range(len(doc)) if not doc[i].get_text().strip())
        total_pages = len(doc)
        doc.close()
        return scanned_pages == total_pages
    except Exception as e:
        print(f"Error checking PDF: {e}")
        return False

@app.route('/check-pdf-type', methods=['POST'])
def check_pdf_type():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    temp_pdf_path = f"temp_{uuid.uuid4().hex}.pdf"
    file.save(temp_pdf_path)

    try:
        is_scanned = is_scanned_pdf(temp_pdf_path)
        os.remove(temp_pdf_path)
        return jsonify({'type': 'scanned' if is_scanned else 'text'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

