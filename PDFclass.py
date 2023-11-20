from weasyprint import HTML, CSS
import requests
import os

class PDFclass:

    def __init__(self):
        # Check if the 'contracts' directory exists, and create it if it doesn't
        if not os.path.exists('contracts'):
            os.makedirs('contracts')

    def generate_pdf(self, html_body, pdf_file_name, html_file_name, signature_url, old_contract_html = ''):

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

        html_body = self.add_signature_to_html_body(html_body, signature_url) + '<br>' + lines
        self.create_html_file(html_body, html_file_name)

        html = HTML(string=html_body)
        css  = CSS(string=custom_css)

        html.write_pdf(pdf_file_name, stylesheets=[css])

    def create_html_file(self, html_body, file_name):
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(html_body)
        

    def add_signature_to_html_body(self, html_body, signature_path):
        if signature_path:
            html_body = html_body.replace("{signature}", f'<img src="{signature_path}" style="width: 160px; height: 50px;" />')
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

    def create(self, body, old_contract_html = ''):
        try:
            signature_url ="http://127.0.0.1:8000/storage/company_logos/company_2_1696945005_output-onlinepngtools.png"
            file = 'contract_new'
            pdf_file_name, html_file_name = os.path.join('contracts', f"{file}.pdf"), os.path.join('contracts', f"{file}.html")

            self.generate_pdf(body, pdf_file_name, html_file_name, signature_url, old_contract_html)
            return pdf_file_name, html_file_name
        except Exception as e:
            return e 

    
