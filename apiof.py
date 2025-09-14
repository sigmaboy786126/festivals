from flask import Flask, jsonify
import os
from functools import wraps

app = Flask(__name__)

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
        "message": "Indian Festival API - Test Endpoint",
        "status": "Working"
    })

@app.route('/test')
@cors
def test():
    return jsonify({"message": "Test endpoint is working"})

@app.route('/festivals/sample')
@cors
def sample_festival():
    # Return a hardcoded sample instead of reading from file
    return jsonify([{
        "name": "Diwali",
        "type": "Religious Festival",
        "description": "Festival of lights",
        "date": "2024-10-31",
        "regions": ["All India"],
        "public_holiday": true
    }])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
