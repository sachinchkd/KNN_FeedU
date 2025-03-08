import React, { useEffect, useState } from 'react';

const FoodRecommendation = () => {
  // State for form inputs and options
  const [locations, setLocations] = useState([]);
  const [priceRanges, setPriceRanges] = useState([]);
  const [cravingCategories, setCravingCategories] = useState([]);
  
  // Form state
  const [location, setLocation] = useState('');
  const [priceRange, setPriceRange] = useState('');
  const [craving, setCraving] = useState('');
  
  // Result state
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  // Backend API base URL (replace with your actual backend URL)
  const API_BASE_URL = 'http://localhost:5000'; // Or your Vercel/deployment URL

  // Fetch dropdown options on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/options`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch options');
        }
        
        const data = await response.json();
        const { locations, priceRanges, cravingCategories } = data;
        
        setLocations(locations);
        setPriceRanges(priceRanges);
        setCravingCategories(cravingCategories);
      } catch (err) {
        console.error('Error fetching options:', err);
        setError('Could not load form options');
      }
    };

    fetchOptions();
  }, []);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          location,
          priceRange,
          craving
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Prediction failed');
      }

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.message || 'Prediction failed');
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Food Recommendation</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Location Dropdown */}
        <div>
          <label className="block mb-2">Location</label>
          <select 
            value={location} 
            onChange={(e) => setLocation(e.target.value)}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Location</option>
            {locations.map((loc) => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
        </div>

        {/* Price Range Dropdown */}
        <div>
          <label className="block mb-2">Price Range</label>
          <select 
            value={priceRange} 
            onChange={(e) => setPriceRange(e.target.value)}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Price Range</option>
            {priceRanges.map((range) => (
              <option key={range} value={range}>{range.replace('price_range_', '')}</option>
            ))}
          </select>
        </div>

        {/* Craving Dropdown */}
        <div>
          <label className="block mb-2">Craving Category</label>
          <select 
            value={craving} 
            onChange={(e) => setCraving(e.target.value)}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Craving</option>
            {cravingCategories.map((cat) => (
              <option key={cat} value={cat}>{cat.replace('Craving_Category_', '')}</option>
            ))}
          </select>
        </div>

        {/* Submit Button */}
        <button 
          type="submit" 
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Get Recommendation
        </button>
      </form>

      {/* Results Section */}
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {prediction && (
        <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
          <h3 className="font-bold">Recommendation:</h3>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
};

export default FoodRecommendation;