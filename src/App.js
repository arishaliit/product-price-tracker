// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [productData, setProductData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const scrapePrice = async () => {
    setLoading(true);
    setProductData(null);
    setError(null);

    try {
      // IMPORTANT: Now using a relative path! Nginx will proxy this.
      const response = await axios.get(`/api/scrape-price`, {
        params: { url: url }
      });
      setProductData(response.data);
    } catch (err) {
      console.error('Error scraping price:', err);
      if (err.response) {
        setError(err.response.data.error || 'Server error occurred.');
      } else if (err.request) {
        setError('No response from server. Check if backend is running.');
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Price Tracker</h1>
      </header>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter product URL (e.g., https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html)"
          value={url}
          onChange={handleUrlChange}
          className="url-input"
        />
        <button onClick={scrapePrice} disabled={loading || !url} className="scrape-button">
          {loading ? 'Scraping...' : 'Scrape Price'}
        </button>
      </div>

      {error && <p className="error-message">Error: {error}</p>}

      {productData && (
        <div className="product-info">
          <h2>Scraped Product Info:</h2>
          <p><strong>URL:</strong> <a href={productData.url} target="_blank" rel="noopener noreferrer">{productData.url}</a></p>
          <p><strong>Title:</strong> {productData.title}</p>
          <p><strong>Price:</strong> {productData.price}</p>
        </div>
      )}
    </div>
  );
}

export default App;
