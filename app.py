from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/read_excel', methods=['POST'])
def read_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    excel_file = BytesIO(file.read())

    xls = pd.read_excel(excel_file, sheet_name=None)

    result = []
    for sheet_name, df in xls.items():
        result.append({
            "sheetName": sheet_name,
            "data": df.to_dict(orient='records')
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
