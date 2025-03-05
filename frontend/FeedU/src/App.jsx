import React, { useState } from 'react';
import './index.css';

const FoodRecommendationForm = () => {
  // State for form inputs
  const [formData, setFormData] = useState({
    craving_sweet: false,
    craving_savory: false,
    craving_spicy: false,
    craving_healthy: false,
    craving_comfort: false,
    craving_fastfood: false,
    price_range: 'price_range_medium',
    location: '0'
  });
  
  // State for displaying result
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle checkbox changes
  const handleCheckboxChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.checked
    });
  };

  // Handle select changes
  const handleSelectChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Map encoded restaurant category to readable name
  const decodeRestaurantCategory = (encodedValue) => {
    // Replace with your actual mapping
    const categoryMap = {
      0: 'Fast Food',
      1: 'Casual Dining',
      2: 'Fine Dining',
      3: 'Cafe',
      4: 'Ethnic Restaurant',
      5: 'Health Food',
      6: 'Food Truck',
      7: 'Buffet',
      8: 'Bakery',
      9: 'Pizza Place'
    };
    
    return categoryMap[encodedValue] || `Category ${encodedValue}`;
  };

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    // Create data object for API request
    const requestData = {
      craving_sweet: formData.craving_sweet ? 1 : 0,
      craving_savory: formData.craving_savory ? 1 : 0,
      craving_spicy: formData.craving_spicy ? 1 : 0,
      craving_healthy: formData.craving_healthy ? 1 : 0,
      craving_comfort: formData.craving_comfort ? 1 : 0,
      craving_fastfood: formData.craving_fastfood ? 1 : 0,
      price_range_low: formData.price_range === 'price_range_low' ? 1 : 0,
      price_range_medium: formData.price_range === 'price_range_medium' ? 1 : 0,
      price_range_high: formData.price_range === 'price_range_high' ? 1 : 0,
      location_encoded: parseInt(formData.location)
    };
    
    try {
      const response = await fetch('http://localhost:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });
      
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data.recommendation);
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Food Recommendation System</h1>
      
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6">
        {/* Cravings Section */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-3 text-gray-700">What are you craving?</h2>
          <div className="grid grid-cols-2 gap-4">
            {['sweet', 'savory', 'spicy', 'healthy', 'comfort', 'fastfood'].map((craving) => (
              <div key={craving} className="flex items-center">
                <input
                  type="checkbox"
                  id={`craving_${craving}`}
                  name={`craving_${craving}`}
                  checked={formData[`craving_${craving}`]}
                  onChange={handleCheckboxChange}
                  className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                />
                <label htmlFor={`craving_${craving}`} className="ml-2 text-gray-700 capitalize">
                  {craving === 'fastfood' ? 'Fast Food' : craving}
                </label>
              </div>
            ))}
          </div>
        </div>
        
        {/* Price Range */}
        <div className="mb-6">
          <label htmlFor="price_range" className="block text-gray-700 font-semibold mb-2">
            Price Range:
          </label>
          <select
            id="price_range"
            name="price_range"
            value={formData.price_range}
            onChange={handleSelectChange}
            className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="price_range_low">Low ($)</option>
            <option value="price_range_medium">Medium ($$)</option>
            <option value="price_range_high">High ($$$)</option>
          </select>
        </div>
        
        {/* Location */}
        <div className="mb-6">
          <label htmlFor="location" className="block text-gray-700 font-semibold mb-2">
            Location:
          </label>
          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleSelectChange}
            className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="0">Downtown</option>
            <option value="1">Uptown</option>
            <option value="2">Suburbs</option>
            <option value="3">Business District</option>
            <option value="4">Shopping Area</option>
          </select>
        </div>
        
        {/* Submit Button */}
        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
        >
          {loading ? 'Getting Recommendation...' : 'Get Recommendation'}
        </button>
      </form>
      
      {/* Results Section */}
      {(result !== null || error) && (
        <div className="mt-8 p-6 bg-white shadow-md rounded-lg">
          {error ? (
            <div className="text-red-600">
              <h2 className="text-xl font-bold mb-2">Error</h2>
              <p>{error}</p>
            </div>
          ) : (
            <>
              <h2 className="text-xl font-bold mb-2 text-gray-800">Recommended Restaurant Type:</h2>
              <p className="text-2xl text-blue-600 font-semibold">{decodeRestaurantCategory(result)}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
};

// App component
const App = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <FoodRecommendationForm />
    </div>
  );
};

export default App;