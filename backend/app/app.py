from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Determine the correct path for loading pickled files
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the trained model and encoders
try:
    with open(os.path.join(base_dir, "food_recommendation_knn.pkl"), "rb") as model_file:
        knn_model = pickle.load(model_file)

    with open(os.path.join(base_dir, "label_encoder.pkl"), "rb") as encoder_file:
        label_encoder = pickle.load(encoder_file)
except Exception as e:
    print(f"Error loading model: {e}")
    knn_model = None
    label_encoder = None

# Define categorical options (same as training)
possible_locations = ['Baluwatar', 'Thamel', 'Kupondole', 'Dhumbarahi', 'Hariharbhawan']
possible_price_ranges = ['price_range_budget', 'price_range_moderate', 'price_range_premium', 'price_range_luxury']
possible_craving_categories = [
    'Craving_Category_Cheesy', 'Craving_Category_Comforting', 
    'Craving_Category_Heart', 'Craving_Category_Light',
    'Craving_Category_Salty', 'Craving_Category_Spicy',
    'Craving_Category_Uncategorized', 'Craving_Category_Veggie'
]

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
        # Get JSON data from request
        data = request.json
        
        # Extract inputs
        location = data.get('location')
        price_range = data.get('priceRange')
        craving = data.get('craving')
        
        # Validate user inputs
        if (location not in possible_locations or 
            price_range not in possible_price_ranges or 
            craving not in possible_craving_categories):
            return jsonify({"error": "Invalid input! Please enter valid values."}), 400
        
        # Prepare input data (similar to your original preprocessing)
        input_data = pd.DataFrame([[location, price_range, craving]], 
                                  columns=['location', 'price_range', 'craving'])
        
        # Define feature columns (you might need to adjust based on your model)
        X = [
            'Craving_Category_Cheesy', 'Craving_Category_Comforting',
            'Craving_Category_Heart', 'Craving_Category_Light',
            'Craving_Category_Salty', 'Craving_Category_Spicy',
            'Craving_Category_Uncategorized', 'Craving_Category_Veggie',
            'price_range_budget', 'price_range_moderate', 
            'price_range_premium', 'price_range_luxury', 
            'location_encoded'
        ]
        
        # Create encoded input (placeholder logic - adjust as needed)
        input_data_encoded = pd.DataFrame(0, index=input_data.index, columns=X)
        
        # Predict using the KNN model
        predicted_label = knn_model.predict(input_data_encoded)
        decoded_label = label_encoder.inverse_transform(predicted_label)
        
        return jsonify({
            "prediction": decoded_label[0],
            "inputData": {
                "location": location,
                "priceRange": price_range,
                "craving": craving
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel-specific handler
def create_app():
    return app

# For local development
if __name__ == '__main__':
    app.run(debug=True)
    