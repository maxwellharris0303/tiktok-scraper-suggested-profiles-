from flask import Flask, jsonify, request
from flask_cors import CORS
import tiktok_scraper
import username_scraper

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/get-profile-usernames', methods=['POST'])
def start_bot():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data or 'username' not in data:
            return jsonify({"status": "error", "message": "Username is required"}), 400
        
        username = data['username']
        
        # Call the scraper with the provided username
        result = username_scraper.main(username)
        if len(result) == 0:
            return jsonify({"status": "success", "data": "no more suggested profiles"})
        return jsonify({"status": "success", "data": result, "total_count": len(result)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
