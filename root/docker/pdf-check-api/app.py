from flask import Flask, request, jsonify
import fitz
import sys
import os
sys.path.append('/shared')
from check_pdf import check_pdf_valid

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

@app.route("/", methods=["GET"])
def home():
    return {"message": "PDF check API is running"}

@app.route("/check", methods=["POST"])
def check_pdf():
    data = request.get_json()
    if not data or 'pdf_path' not in data:
        return jsonify({'error': 'Missing pdf_path'}), 400

    pdf_path = data['pdf_path']
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'File does not exist'}), 404

    # return jsonify({'message': f'File {pdf_path} exists'})
    try:
        is_scanned = is_scanned_pdf(pdf_path)
        return jsonify({'type': 'scanned' if is_scanned else 'text'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
