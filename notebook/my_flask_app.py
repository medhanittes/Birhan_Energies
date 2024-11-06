from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data():
    df = pd.read_csv('data/oil_prices.csv')  # Adjust the path as necessary
    df['date'] = pd.to_datetime(df['date'])  # Ensure the date column is in datetime format
    return df

@app.route('/api/oil-prices', methods=['GET'])
def get_oil_prices():
    logging.info("Received a request for oil prices")
    try:
        df = load_data()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if filtered_df.empty:
            return jsonify({"error": "No data found for the specified date range"}), 404
        
        return jsonify(filtered_df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)