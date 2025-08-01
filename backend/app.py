# backend/app.py
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import re # For cleaning price string
import os # To get port from environment variable
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes - IMPORTANT for frontend to talk to backend

# --- UPDATED: Use the confirmed working selectors ---
PRODUCT_TITLE_SELECTOR = '#content_inner > article > div.row > div.col-sm-6.product_main > h1'
PRODUCT_PRICE_SELECTOR = '#content_inner > article > div.row > div.col-sm-6.product_main > p.price_color' 
# ---------------------------------------------------

@app.route('/api/scrape-price', methods=['GET'])
def scrape_price():
    product_url = request.args.get('url')

    print(f"DEBUG: Received request for URL: {product_url}") # DEBUG LOG

    if not product_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        # Simple validation for demonstration. Improve for production.
        if not (product_url.startswith('http://') or product_url.startswith('https://')):
            return jsonify({"error": "Invalid URL format. Must start with http:// or https://"}), 400

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(product_url, headers=headers, timeout=15)
        
        print(f"DEBUG: HTTP Status Code from target URL: {response.status_code}") # DEBUG LOG
        print(f"DEBUG: First 500 chars of fetched HTML: {response.text}") # DEBUG LOG

        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find product title
        title_element = soup.select_one(PRODUCT_TITLE_SELECTOR)
        product_title = title_element.get_text(strip=True) if title_element else 'N/A'

        # Find product price
        price_element = soup.select_one(PRODUCT_PRICE_SELECTOR)
        product_price = price_element.get_text(strip=True) if price_element else 'N/A'

        # Clean up price string (remove currency symbols, extra spaces, etc.)
        if product_price != 'N/A':
            # Remove any non-digit, non-dot, non-comma characters, then remove commas for consistent float conversion
            product_price = re.sub(r'[^\d.,]+', '', product_price)
            product_price = product_price.replace(',', '') # Remove thousands separator if present
            
            # Extract only the numeric part before the dot for whole numbers
            match = re.search(r'(\d+\.?\d*)', product_price)
            if match:
                product_price = match.group(1)
            else:
                product_price = 'N/A' # Fallback if no numeric part found after cleaning

        print(f"DEBUG: Scraped Title (before sending): {product_title}") # DEBUG LOG
        print(f"DEBUG: Scraped Price (before sending): {product_price}") # DEBUG LOG

        return jsonify({
            "url": product_url,
            "title": product_title,
            "price": "£" + product_price
        })

    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Network or HTTP error during scrape: {e}") # DEBUG LOG
        return jsonify({"error": f"Network or HTTP error: {e}"}), 500
    except Exception as e:
        print(f"DEBUG: An unexpected error occurred during scrape: {e}") # DEBUG LOG
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
