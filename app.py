from flask import Flask, request, jsonify, send_from_directory
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import requests
import io  # Import the io module
from io import BytesIO
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

app = Flask(__name__)

# to fetch the image form the url
def fetch_signature_image(signature_url):
    try:
        response = requests.get(signature_url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
        
def generate_pdf(html_body, filename, signature_url="http://127.0.0.1:8000/storage/company_logos/company_2_1696945005_output-onlinepngtools.png"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Download the signature image from the URL
    response = requests.get(signature_url)
    
    if response.status_code == 200:
        signature_image_data = response.content
    else:
        signature_image_data = None

    # Define a custom style for handling HTML content
    html_style = ParagraphStyle('html_style', parent=styles['Normal'])
    
    modified_string = html_body.replace("<br>", "<br></br>")

    # Create a Paragraph element from the modified HTML content
    paragraph = Paragraph(modified_string, html_style)
    
    # Add the paragraph to the story
    story.append(paragraph)
    
    # Add the signature image
    if signature_image_data:
        # pil_image = PILImage.open(BytesIO(signature_image_data))
        # width, height = pil_image.size
        image = Image(BytesIO(signature_image_data), width=150, height=50)
        
        story.append(image)
    
    doc.build(story)

# Route to generate and serve the PDF
@app.route('/generate_pdf', methods=['POST'])
def generate_and_serve_pdf():
    # Get the request data
    request_data = request.get_json()

    # Get the body text from the request data
    body = request_data.get('body')
    
    # Check if the 'contracts' directory exists, and create it if it doesn't
    if not os.path.exists('contracts'):
        os.makedirs('contracts')

    # Generate the PDF using ReportLab
    pdf_filename = os.path.join('contracts', 'contract.pdf')
    generate_pdf(body, pdf_filename)

    # Construct the download URL
    file_url = '/download/contract.pdf'

    return jsonify({'file_url': file_url})

# Route to download the PDF
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Serve the file for download
    return send_from_directory('contracts', filename)

if __name__ == '__main__':
    app.run(debug=True)
