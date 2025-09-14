from flask import Flask, jsonify, request
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Base directory for JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'festivals.json')

# Load the JSON data
def load_festival_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# CORS decorator
def cors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response
    return decorated_function

@app.route('/')
@cors
def home():
    return jsonify({
        "message": "Indian Festival & Event Calendar API",
        "endpoints": {
            "/festivals": "Get all festivals",
            "/festivals/<name>": "Get festival by name",
            "/festivals/date/<date>": "Get festivals on a specific date (YYYY-MM-DD)",
            "/festivals/month/<month>": "Get festivals in a specific month (1-12)",
            "/festivals/region/<region>": "Get festivals by region",
            "/festivals/type/<type>": "Get festivals by type",
            "/festivals/public": "Get all public holidays",
            "/regional-events": "Get all regional events",
            "/metadata": "Get metadata about the dataset"
        }
    })

@app.route('/festivals')
@cors
def get_all_festivals():
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify(data["festivals"])

@app.route('/festivals/<name>')
@cors
def get_festival_by_name(name):
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    festival = next((f for f in data["festivals"] if f["name"].lower() == name.lower()), None)
    if festival:
        return jsonify(festival)
    else:
        return jsonify({"error": "Festival not found"}), 404

@app.route('/festivals/date/<date>')
@cors
def get_festivals_by_date(date):
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    festivals = [f for f in data["festivals"] if f["date"] == date]
    return jsonify(festivals)

@app.route('/festivals/month/<int:month>')
@cors
def get_festivals_by_month(month):
    if month < 1 or month > 12:
        return jsonify({"error": "Month must be between 1 and 12"}), 400
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    festivals = [f for f in data["festivals"] if int(f["date"].split('-')[1]) == month]
    return jsonify(festivals)

@app.route('/festivals/region/<region>')
@cors
def get_festivals_by_region(region):
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    festivals = [f for f in data["festivals"] if region.lower() in [r.lower() for r in f["regions"]]]
    return jsonify(festivals)

@app.route('/festivals/type/<festival_type>')
@cors
def get_festivals_by_type(festival_type):
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    festivals = [f for f in data["festivals"] if f["type"].lower() == festival_type.lower()]
    return jsonify(festivals)

@app.route('/festivals/public')
@cors
def get_public_holidays():
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    public_holidays = [f for f in data["festivals"] if f.get("public_holiday", False)]
    return jsonify(public_holidays)

@app.route('/regional-events')
@cors
def get_regional_events():
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify(data["regional_events"])

@app.route('/metadata')
@cors
def get_metadata():
    data = load_festival_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify(data["metadata"])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
