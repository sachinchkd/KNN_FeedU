from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

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

@app.route('/')
def index():
    # Make sure variable name matches what's used in the template
    return render_template('index.html', 
                          locations=possible_locations, 
                          price_ranges=possible_price_ranges, 
                          craving_categories=possible_craving_categories)  # Changed from 'cravings'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user inputs
        location = request.form['location']
        price_range = request.form['price_range']
        craving = request.form['craving']
        
        # Validate user inputs
        if location not in possible_locations or price_range not in possible_price_ranges or craving not in possible_craving_categories:
            return "Invalid input! Please enter valid values."
            
        input_data = pd.DataFrame([[location, price_range, craving]], columns=['location', 'price_range', 'craving'])

# Define the list of feature columns
        X = ['Craving_Category_Cheesy', 'Craving_Category_Comforting',
            'Craving_Category_Heart', 'Craving_Category_Light',
            'Craving_Category_Salty', 'Craving_Category_Spicy',
            'Craving_Category_Uncategorized', 'Craving_Category_Veggie',
            'price_range_budget', 'price_range_moderate', 'price_range_premium',
            'price_range_luxury', 'location_encoded']

# Encode the input data based on your predefined feature columns (this will depend on how you encode 'location', 'price_range', 'craving')
# For now, I'll fill the DataFrame with zeros as placeholders
        input_data_encoded = pd.DataFrame(0, index=input_data.index, columns=X)
            
        # Predict using the KNN model
        predicted_label = knn_model.predict(input_data_encoded)
        decoded_label = label_encoder.inverse_transform(predicted_label)
            
        return render_template('result.html', prediction=decoded_label[0])
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    
    app.run(debug=True)