from weasyprint import HTML, CSS
import requests
import os
from datetime import datetime

class PDFclass:

    def __init__(self):
        # Check if the 'contracts' directory exists, and create it if it doesn't
        if not os.path.exists('contracts'):
            os.makedirs('contracts')

    def generate_pdf(self, html_body, pdf_file_name, html_file_name, signature_urls, old_contract_html = ''):

        custom_css = """
        @font-face {
            font-family: 'YourFontName';
            src: url('path_to_font.ttf');
        }
        body {
            font-family: 'YourFontName', sans-serif;
        }
        """
        lines = ''
        if os.path.exists(old_contract_html):
            with open(old_contract_html, 'r') as contract:
                lines = contract.readlines() 
            lines = ''.join(lines)

        html_body = self.add_signature_to_html_body(html_body, signature_urls) + '<br>' + lines
        self.create_html_file(html_body, html_file_name)

        html = HTML(string=html_body)
        css  = CSS(string=custom_css)

        html.write_pdf(pdf_file_name, stylesheets=[css])

    def create_html_file(self, html_body, file_name):
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(html_body)
        

    def add_signature_to_html_body(self, html_body, signature_urls):
        for signature_token, signature_path in signature_urls.items():  # Use .items() for dictionary iteration
            html_body = html_body.replace(f"{{{signature_token}}}", f'<img src="{signature_path}" style="width: 160px; height: 50px;" />')
        return html_body

    def fetch_signature_image(self, signature_url):
        try:
            response = requests.get(signature_url)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except Exception as e:
            return e 

    def create(self, body, old_contract_html = '', employee_signature = '', employer_signature = ''):
        try:
            signature_urls = {
                'employee_signature': employee_signature or "https://upload.wikimedia.org/wikipedia/commons/a/aa/Henry_Oaminal_Signature.png",
                'employer_signature': employer_signature or "https://upload.wikimedia.org/wikipedia/commons/a/aa/Henry_Oaminal_Signature.png",
            }

            timestamp      = datetime.now().strftime("%Y%m%d%H%M%S")
            file_prefix    = 'contract_attached_' if old_contract_html else 'contract_'
            file           = f'{file_prefix}{timestamp}'
            pdf_file_name  = os.path.join('contracts', f"{file}.pdf")
            html_file_name = os.path.join('contracts', f"{file}.html")
            self.generate_pdf(body, pdf_file_name, html_file_name, signature_urls, old_contract_html)
            return pdf_file_name, html_file_name, file
        except Exception as e:
            return e

    
