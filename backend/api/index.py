from flask import Flask, jsonify, request, Response
from flask.helpers import send_from_directory
import os
from http.server import BaseHTTPRequestHandler

# Define your variables
possible_locations = ["Location1", "Location2", "Location3"] 
possible_price_ranges = ["$", "$$", "$$$"]
possible_craving_categories = ["Italian", "Chinese", "Mexican"]

app = Flask(__name__)

@app.route('/api/options', methods=['GET'])
def get_options():
    """Provide dropdown options for frontend"""
    return jsonify({
        'locations': possible_locations,
        'priceRanges': possible_price_ranges,
        'cravingCategories': possible_craving_categories
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Process the data
        result = {"recommendation": "Restaurant Name"}  # Replace with actual logic
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(event, context):
    path = event.get('path', '')
    http_method = event.get('httpMethod', '')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Create a request context for Flask
    with app.test_request_context(
        path=path,
        method=http_method,
        headers=headers,
        data=body
    ):
        # Process the request
        response = app.full_dispatch_request()
        
    # Return the response in the format expected by Vercel
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.data.decode('utf-8')
    }

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = app.test_client().get(self.path)
        self.send_response(response.status_code)
        for header, value in response.headers:
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.data)
        
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        response = app.test_client().post(
            self.path, 
            json=json.loads(body) if body else None,
            headers=dict(self.headers)
        )
        self.send_response(response.status_code)
        for header, value in response.headers:
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.data)