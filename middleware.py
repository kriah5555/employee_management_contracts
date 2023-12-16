from flask import request
from database import db
from models import APIRequestLog
import json  
from urllib.parse import urlparse

def get_domain_from_request():
    # Extract the domain from the request URL
    parsed_url = urlparse(request.url)
    return parsed_url.netloc

def log_request():
    try:
        if request.method == 'POST':
            request_data = request.get_json()
            request_body = json.dumps(request_data) if request_data else request.data.decode()
        else:
            request_body = None

        log_entry = APIRequestLog(
            method       = request.method,
            endpoint     = request.path,
            request_data = json.dumps(request_data) if request_data else None,
            request_body = request_body,
            domain       = get_domain_from_request(),
        )

        db.session.add(log_entry)
        db.session.commit()

    except Exception as e:
        print(f"Error logging request: {str(e)}")

def log_response(response):
    try:
        log_entry = APIRequestLog(
            status_code   = response.status_code,
            response_data = json.dumps(response.get_json()) if response.get_json() else None,
            response_body = response.data.decode(),
            domain        = get_domain_from_request(),
        )

        db.session.add(log_entry)
        db.session.commit()

    except Exception as e:
        print(f"Error logging response: {str(e)}")

    return response
