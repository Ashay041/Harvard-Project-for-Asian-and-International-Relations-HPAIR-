"""
Flask Backend for Urban Fire Spread Prediction
Serves static files and provides API endpoints
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from fire_model import UrbanFireModel
from weather_api import WeatherAPI

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize components
fire_model = UrbanFireModel()
weather_api = WeatherAPI()

@app.route('/')
def index():
    """Serve main HTML page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    """Serve CSS files"""
    return send_from_directory('../frontend/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    """Serve JavaScript files"""
    return send_from_directory('../frontend/js', path)

@app.route('/config/<path:path>')
def send_config(path):
    """Serve config files"""
    return send_from_directory('../config', path)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get current weather data for location"""
    try:
        lat = float(request.args.get('lat', 34.0522))
        lon = float(request.args.get('lon', -118.2437))
        
        weather_data = weather_api.get_weather(lat, lon)
        return jsonify({
            'success': True,
            'data': weather_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/simulate', methods=['POST'])
def simulate_fire():
    """Simulate fire spread from origin point"""
    try:
        data = request.json
        lat = data.get('lat')
        lon = data.get('lon')
        wind_speed = data.get('windSpeed', 15)
        building_density = data.get('buildingDensity', 40)
        time_steps = data.get('timeSteps', 10)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing lat or lon'
            }), 400
        
        result = fire_model.simulate(
            origin_lat=lat,
            origin_lon=lon,
            wind_speed=wind_speed,
            building_density=building_density,
            time_steps=time_steps
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Urban Fire Prediction API'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Urban Fire Spread Prediction System")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("📍 URL: http://localhost:5001")
    print("\n✨ Server ready! Open browser to http://localhost:5001\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)