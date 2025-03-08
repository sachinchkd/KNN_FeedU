from http.server import BaseHTTPRequestHandler
import json

# Define your variables
possible_locations = ["Location1", "Location2", "Location3"] 
possible_price_ranges = ["$", "$$", "$$$"]
possible_craving_categories = ["Italian", "Chinese", "Mexican"]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'locations': possible_locations,
            'priceRanges': possible_price_ranges,
            'cravingCategories': possible_craving_categories
        }
        
        self.wfile.write(json.dumps(response).encode())
        return