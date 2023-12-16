from flask import Flask, request, jsonify, send_from_directory
from PDFclass import PDFclass
import os
import requests  # Add this line to import the requests module
import subprocess
import fitz  # PyMuPDF
import tempfile
from middleware import log_request, log_response
from database import db
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('constants.py')  # Load configuration from constants.py
db.init_app(app)
migrate = Migrate(app, db)

app.before_request(log_request)
app.after_request(log_response)


@app.route('/attach_contract', methods=['POST'])
def attach_contract():
    # Get the request data
    request_data = request.get_json()
    body         = request_data.get('body')
    old_contract = request_data.get('old_contract_html_path')
    pdf          = PDFclass()
    pdf_file_path, html_file_path = pdf.create(body, old_contract)
    return jsonify({
        'pdf_file_path': pdf_file_path, 
        'html_file_path': html_file_path, 
        })

@app.route('/create_contract', methods=['POST'])
def create_contract():
    # Get the request data
    request_data = request.get_json()
    body         = request_data.get('body')
    pdf          = PDFclass()
    pdf_file_path, html_file_path = pdf.create(body)

    return jsonify({
        'pdf_file_path': pdf_file_path, 
        'html_file_path': html_file_path, 
        })

# Route to download the PDF
@app.route('/contracts/<filename>', methods=['GET'])
def download_file(filename):
    # Serve the file for download
    return send_from_directory('contracts', filename)

@app.route('/convert-pdf-to-html', methods=['GET'])
def convert_pdf_to_html():
    try:
        # Check if the request contains a file
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No file provided in the request'}), 400

        pdf_file = request.files['pdf_file']

        # Check if the file is a PDF
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Use pdf2htmlEX to convert PDF to HTML
            pdf2html_command = ['pdf2htmlEX', '-', '-']

            # Open a subprocess, pass the PDF content, and capture the output
            process = subprocess.Popen(pdf2html_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=pdf_file.read())

            # Check if there was any error during the conversion
            if process.returncode != 0:
                return jsonify({'error': f'PDF to HTML conversion failed. Error: {stderr.decode("utf-8")}'})
            
            # Return the HTML data
            return jsonify({'html_data': stdout.decode("utf-8")})

        else:
            return jsonify({'error': 'Invalid file format. Please provide a PDF file'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
