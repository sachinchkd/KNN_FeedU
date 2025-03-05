import os
from flask import Flask, request, jsonify
import joblib
import pickle
import pandas as pd
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and encoders
with open("food_recommendation_knn.pkl", "rb") as model_file:
    knn_model = pickle.load(model_file)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Define categorical options (same as training)
possible_locations = ['Baluwatar', 'Thamel', 'Kupondole', 'Dhumbarahi', 'Hariharbhawan']
possible_price_ranges = ['price_range_budget', 'price_range_moderate', 'price_range_premium', 'price_range_luxury']
possible_craving_categories = ['Craving_Category_Cheesy', 'Craving_Category_Comforting', 'Craving_Category_Heart',
                              'Craving_Category_Light', 'Craving_Category_Salty', 'Craving_Category_Spicy',
                              'Craving_Category_Uncategorized', 'Craving_Category_Veggie']

# Get the absolute path of the model file
model_path = os.path.join(os.path.dirname(__file__), 'models', 'food_recommendation_knn.pkl')

# Load the saved model
model = joblib.load(model_path)

# Add this to debug your model's expected features
@app.route('/features', methods=['GET'])
def get_model_features():
    if hasattr(model, 'feature_names_in_'):
        return jsonify({
            'feature_names': model.feature_names_in_.tolist()
        })
    else:
        return jsonify({
            'error': 'Model does not expose feature_names_in_ attribute',
            # Try to get feature names from another source if available
            'model_type': str(type(model))
        })

# Define API route
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get input data as JSON
        location = request.get_json('location')
        price_range = request.get_json('price_range')
        craving = request.get_json('craving')
        
        data = request.get_json()
        print("Received data:", data)
        
        # Get expected feature names if available
        feature_names = None
        if hasattr(model, 'feature_names_in_'):
            feature_names = model.feature_names_in_.tolist()
            print("Expected features:", feature_names)
            
            # Ensure all expected features are present in the data
            for feature in feature_names:
                if feature not in data:
                    data[feature] = 0  # Default value
                    
            # Create DataFrame with features in the correct order
            input_df = pd.DataFrame([{feature: data.get(feature, 0) for feature in feature_names}])
        else:
            # If we can't get features names, just use the data as-is
            input_df = pd.DataFrame([data])
        
        print("Input DataFrame:", input_df)
        
        # Make prediction
        prediction = model.predict(input_df)[0]

        # Return the result
        return jsonify({'recommendation': prediction})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)