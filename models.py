from database import db

class APIRequestLog(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    timestamp     = db.Column(db.DateTime, server_default=db.func.now())
    method        = db.Column(db.String(10))
    endpoint      = db.Column(db.String(255))
    status_code   = db.Column(db.Integer)
    request_data  = db.Column(db.Text)
    response_data = db.Column(db.Text)
    request_body  = db.Column(db.Text)       
    response_body = db.Column(db.Text) 
    domain        = db.Column(db.String(255))  # New column for domain name
    