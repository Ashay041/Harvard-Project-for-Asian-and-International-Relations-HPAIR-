#!/usr/bin/env python3
"""
Urban Fire Spread Prediction System - Project Generator
Run this script to create the complete project structure with all files!

Usage:
    python create_project.py

This will create a folder 'urban-fire-prediction' with everything you need.
"""

import os
import sys

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    print(f"✓ Created: {path}")

def write_file(path, content):
    """Write content to file"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def main():
    print("=" * 60)
    print("🔥 Urban Fire Spread Prediction System")
    print("   Project Generator - Zero API Keys Required!")
    print("=" * 60)
    print()
    
    # Base directory
    base_dir = "urban-fire-prediction"
    
    # Create directory structure
    print("Creating project structure...")
    create_directory(base_dir)
    create_directory(f"{base_dir}/backend")
    create_directory(f"{base_dir}/frontend")
    create_directory(f"{base_dir}/frontend/css")
    create_directory(f"{base_dir}/frontend/js")
    create_directory(f"{base_dir}/config")
    print()
    
    # ==================== BACKEND FILES ====================
    
    print("Creating backend files...")
    
    # backend/requirements.txt
    write_file(f"{base_dir}/backend/requirements.txt", """Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
numpy==1.24.3
""")
    
    # backend/app.py
    write_file(f"{base_dir}/backend/app.py", """\"\"\"
Flask Backend for Urban Fire Spread Prediction
Serves static files and provides API endpoints
\"\"\"

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
    \"\"\"Serve main HTML page\"\"\"
    return send_from_directory('../frontend', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    \"\"\"Serve CSS files\"\"\"
    return send_from_directory('../frontend/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    \"\"\"Serve JavaScript files\"\"\"
    return send_from_directory('../frontend/js', path)

@app.route('/config/<path:path>')
def send_config(path):
    \"\"\"Serve config files\"\"\"
    return send_from_directory('../config', path)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    \"\"\"Get current weather data for location\"\"\"
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
    \"\"\"Simulate fire spread from origin point\"\"\"
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
    \"\"\"Health check endpoint\"\"\"
    return jsonify({
        'status': 'healthy',
        'service': 'Urban Fire Prediction API'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Urban Fire Spread Prediction System")
    print("=" * 60)
    print("\\n🚀 Starting server...")
    print("📍 URL: http://localhost:5000")
    print("\\n✨ Server ready! Open browser to http://localhost:5000\\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
""")
    
    # backend/fire_model.py
    write_file(f"{base_dir}/backend/fire_model.py", """\"\"\"
Urban Fire Spread Model
Implements refined Rothermel model for urban environments
\"\"\"

import numpy as np
import math

class UrbanFireModel:
    \"\"\"Fire spread model adapted for urban environments\"\"\"
    
    def __init__(self):
        self.CFD_CONSTANT = 0.22
        self.FUEL_ENERGY = 3000
        self.PACKING_RATIO = 0.8
        self.WIND_COEFFICIENT = 0.4
        self.WIND_EXPONENT = 0.02526
        self.FUEL_MOISTURE = 0.035
        self.FUEL_DENSITY = 780
        self.FUEL_DEPTH = 2
        
    def calculate_urban_wind(self, base_wind_speed, building_height=20, street_width=15):
        \"\"\"Calculate wind speed in urban street canyon\"\"\"
        aspect_ratio = building_height / street_width
        urban_wind = base_wind_speed * (1 + self.CFD_CONSTANT * aspect_ratio)
        return round(urban_wind, 2)
    
    def calculate_spread_rate(self, wind_speed, building_density):
        \"\"\"Calculate fire spread rate using Rothermel model\"\"\"
        wind_ms = wind_speed / 3.6
        
        numerator = (self.FUEL_ENERGY * self.PACKING_RATIO * 
                    (1 + (self.WIND_COEFFICIENT * wind_ms ** self.WIND_EXPONENT)))
        denominator = (self.FUEL_MOISTURE * self.FUEL_DEPTH * self.FUEL_DENSITY)
        
        density_factor = 1 - (building_density / 100)
        spread_rate = (numerator / denominator) * density_factor
        return round(spread_rate, 3)
    
    def calculate_spread_direction(self, origin_lat, origin_lon, angle_deg, distance_m):
        \"\"\"Calculate new coordinates given origin, angle, and distance\"\"\"
        R = 6371000
        
        lat1 = math.radians(origin_lat)
        lon1 = math.radians(origin_lon)
        angle_rad = math.radians(angle_deg)
        
        lat2 = math.asin(
            math.sin(lat1) * math.cos(distance_m / R) +
            math.cos(lat1) * math.sin(distance_m / R) * math.cos(angle_rad)
        )
        
        lon2 = lon1 + math.atan2(
            math.sin(angle_rad) * math.sin(distance_m / R) * math.cos(lat1),
            math.cos(distance_m / R) - math.sin(lat1) * math.sin(lat2)
        )
        
        return math.degrees(lat2), math.degrees(lon2)
    
    def simulate(self, origin_lat, origin_lon, wind_speed=15, 
                 building_density=40, time_steps=10, time_interval=5):
        \"\"\"Run complete fire spread simulation\"\"\"
        urban_wind = self.calculate_urban_wind(wind_speed)
        spread_rate = self.calculate_spread_rate(urban_wind, building_density)
        
        fire_zones = []
        
        for step in range(1, time_steps + 1):
            distance_m = spread_rate * time_interval * step
            intensity = 1.0 - (step / time_steps) * 0.5
            
            perimeter_points = []
            num_directions = 16
            
            for i in range(num_directions):
                angle = (360 / num_directions) * i
                new_lat, new_lon = self.calculate_spread_direction(
                    origin_lat, origin_lon, angle, distance_m
                )
                perimeter_points.append({
                    'lat': new_lat,
                    'lon': new_lon
                })
            
            fire_zones.append({
                'step': step,
                'time': step * time_interval,
                'distance': round(distance_m, 2),
                'intensity': round(intensity, 3),
                'perimeter': perimeter_points
            })
        
        return {
            'origin': {
                'lat': origin_lat,
                'lon': origin_lon
            },
            'parameters': {
                'baseWind': wind_speed,
                'urbanWind': urban_wind,
                'spreadRate': spread_rate,
                'buildingDensity': building_density,
                'timeSteps': time_steps,
                'timeInterval': time_interval
            },
            'zones': fire_zones,
            'summary': {
                'totalTime': time_steps * time_interval,
                'maxDistance': round(spread_rate * time_interval * time_steps, 2),
                'affectedArea': round(math.pi * (spread_rate * time_interval * time_steps) ** 2, 2)
            }
        }
""")
    
    # backend/weather_api.py
    write_file(f"{base_dir}/backend/weather_api.py", """\"\"\"
Weather API Integration
Fetches real-time weather data from OpenWeatherMap
\"\"\"

import requests
import os
from datetime import datetime

class WeatherAPI:
    \"\"\"OpenWeatherMap API wrapper for weather data\"\"\"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY', '')
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        
    def get_weather(self, lat, lon):
        \"\"\"Get current weather data for location\"\"\"
        if not self.api_key or self.api_key == 'YOUR_OPENWEATHER_KEY_HERE':
            return self._get_mock_weather(lat, lon)
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'windSpeed': round(data['wind']['speed'] * 3.6, 1),
                'windDirection': data['wind'].get('deg', 0),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'pressure': data['main']['pressure'],
                'location': data['name'],
                'timestamp': datetime.now().isoformat(),
                'source': 'OpenWeatherMap API'
            }
            
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather(lat, lon)
    
    def _get_mock_weather(self, lat, lon):
        \"\"\"Generate mock weather data for testing\"\"\"
        import random
        
        return {
            'temperature': round(random.uniform(15, 30), 1),
            'humidity': random.randint(30, 70),
            'windSpeed': round(random.uniform(10, 25), 1),
            'windDirection': random.randint(0, 360),
            'description': 'clear sky',
            'icon': '01d',
            'pressure': random.randint(1000, 1020),
            'location': 'Los Angeles',
            'timestamp': datetime.now().isoformat(),
            'source': 'Mock Data (Add API key for real data)'
        }
""")
    
    print()
    
    # ==================== CONFIG FILES ====================
    
    print("Creating config files...")
    
    # config/config.js
    write_file(f"{base_dir}/config/config.js", """/**
 * Configuration file - NO API KEYS REQUIRED!
 */

export const CONFIG = {
    // OpenWeatherMap is optional - app works without it
    OPENWEATHER_API_KEY: '',
    
    DEFAULT_LOCATION: {
        latitude: 34.0522,
        longitude: -118.2437,
        zoom: 13
    },
    
    API_BASE_URL: 'http://localhost:5000',
    
    SIMULATION: {
        windSpeed: 15,
        buildingDensity: 40,
        timeSteps: 10,
        timeInterval: 5
    },
    
    MAP: {
        tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }
};
""")
    
    print()
    
    # ==================== FRONTEND FILES ====================
    
    print("Creating frontend files...")
    
    # frontend/index.html
    write_file(f"{base_dir}/frontend/index.html", """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urban Fire Spread Prediction System</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header class="app-header">
        <div class="header-content">
            <h1>🔥 Urban Fire Spread Prediction</h1>
            <p>AI-Driven Risk Modeling | Zero API Keys Required</p>
        </div>
    </header>

    <div class="app-container">
        <div class="control-panel">
            <div class="panel-section">
                <h3>📍 Fire Origin</h3>
                <div class="info-group">
                    <label>Click on map to set fire origin</label>
                    <div class="coordinates" id="originCoords">
                        <span>Lat: --</span>
                        <span>Lon: --</span>
                    </div>
                </div>
            </div>

            <div class="panel-section">
                <h3>🌤️ Weather Conditions</h3>
                <div class="weather-info" id="weatherInfo">
                    <div class="weather-loading">Loading...</div>
                </div>
                <button class="btn btn-secondary" onclick="refreshWeather()">Refresh Weather</button>
            </div>

            <div class="panel-section">
                <h3>⚙️ Simulation Parameters</h3>
                <div class="input-group">
                    <label for="windSpeed">Wind Speed (km/h)</label>
                    <input type="range" id="windSpeed" min="5" max="50" value="15" step="1">
                    <span class="input-value" id="windSpeedValue">15</span>
                </div>
                <div class="input-group">
                    <label for="buildingDensity">Building Density (%)</label>
                    <input type="range" id="buildingDensity" min="0" max="100" value="40" step="5">
                    <span class="input-value" id="buildingDensityValue">40</span>
                </div>
                <div class="input-group">
                    <label for="timeSteps">Simulation Steps</label>
                    <input type="range" id="timeSteps" min="5" max="20" value="10" step="1">
                    <span class="input-value" id="timeStepsValue">10</span>
                </div>
            </div>

            <div class="panel-section">
                <button class="btn btn-primary" id="runSimulation" onclick="runSimulation()">▶️ Run Simulation</button>
                <button class="btn btn-danger" id="clearSimulation" onclick="clearSimulation()">🗑️ Clear</button>
            </div>

            <div class="panel-section">
                <h3>📊 Results</h3>
                <div class="results">
                    <div class="result-item"><span>Urban Wind:</span><span id="resultUrbanWind">--</span></div>
                    <div class="result-item"><span>Spread Rate:</span><span id="resultSpreadRate">--</span></div>
                    <div class="result-item"><span>Max Distance:</span><span id="resultMaxDistance">--</span></div>
                    <div class="result-item"><span>Total Time:</span><span id="resultTotalTime">--</span></div>
                </div>
            </div>

            <div class="panel-section" id="timeSliderSection" style="display: none;">
                <h3>⏱️ Time Progression</h3>
                <div class="time-slider-container">
                    <input type="range" id="timeSlider" min="0" max="10" value="10" step="1">
                    <div class="time-display" id="timeDisplay">50 minutes</div>
                </div>
            </div>
        </div>

        <div class="map-container">
            <div id="map"></div>
            <div class="map-instructions" id="mapInstructions">
                <div class="instruction-content">
                    <h3>🎯 Getting Started</h3>
                    <ol>
                        <li>Click anywhere on the map to set fire origin</li>
                        <li>Adjust simulation parameters on the left</li>
                        <li>Click "Run Simulation" to see fire spread</li>
                        <li>Use time slider to control visualization</li>
                    </ol>
                </div>
            </div>
            <div class="loading-overlay" id="loadingOverlay" style="display: none;">
                <div class="spinner"></div>
                <p>Running simulation...</p>
            </div>
        </div>
    </div>

    <footer class="app-footer">
        <p>Urban Fire Spread Prediction | Rothermel Model | HPAIR | 🆓 Zero API Keys</p>
    </footer>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
    <script type="module" src="config/config.js"></script>
    <script type="module" src="js/map.js"></script>
    <script type="module" src="js/fire-simulation.js"></script>
    <script type="module" src="js/ui-controls.js"></script>
</body>
</html>
""")
    
    # Continue in next part due to length...
    
    # frontend/css/style.css
    css_content = """/* Global Styles */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; overflow: hidden; }

/* Header */
.app-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.header-content h1 { font-size: 28px; margin-bottom: 5px; }
.header-content p { font-size: 14px; opacity: 0.9; }

/* Container */
.app-container { display: flex; height: calc(100vh - 140px); gap: 0; }

/* Control Panel */
.control-panel { width: 350px; background: white; overflow-y: auto; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1000; }
.panel-section { padding: 20px; border-bottom: 1px solid #e0e0e0; }
.panel-section h3 { font-size: 16px; margin-bottom: 15px; color: #667eea; }

/* Info Groups */
.info-group label { display: block; font-size: 12px; color: #666; margin-bottom: 8px; }
.coordinates { display: flex; gap: 15px; font-family: monospace; font-size: 13px; background: #f8f9fa; padding: 10px; border-radius: 4px; }

/* Weather Info */
.weather-info { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.weather-loading { text-align: center; color: #999; padding: 10px; }
.weather-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.weather-item { display: flex; flex-direction: column; }
.weather-item label { font-size: 11px; color: #666; margin-bottom: 3px; }
.weather-item span { font-size: 14px; font-weight: 600; color: #333; }

/* Input Groups */
.input-group { margin-bottom: 20px; }
.input-group label { display: block; font-size: 13px; margin-bottom: 8px; color: #555; }
.input-group input[type="range"] { width: 100%; height: 6px; background: #ddd; border-radius: 3px; outline: none; -webkit-appearance: none; }
.input-group input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; background: #667eea; border-radius: 50%; cursor: pointer; }
.input-value { display: inline-block; margin-left: 10px; font-weight: 600; color: #667eea; min-width: 40px; }

/* Buttons */
.btn { width: 100%; padding: 12px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; margin-bottom: 10px; }
.btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.btn-secondary { background: #6c757d; color: white; }
.btn-secondary:hover { background: #5a6268; }
.btn-danger { background: #dc3545; color: white; }
.btn-danger:hover { background: #c82333; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Results */
.results { background: #f8f9fa; padding: 15px; border-radius: 8px; }
.result-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e0e0e0; }
.result-item:last-child { border-bottom: none; }
.result-item span:first-child { font-size: 13px; color: #666; }
.result-item span:last-child { font-weight: 600; color: #667eea; font-size: 14px; }

/* Time Slider */
.time-slider-container { margin-top: 10px; }
.time-slider-container input[type="range"] { width: 100%; }
.time-display { text-align: center; font-size: 16px; font-weight: 600; color: #667eea; margin-top: 10px; }

/* Map Container */
.map-container { flex: 1; position: relative; background: #e0e0e0; }
#map { width: 100%; height: 100%; }

/* Map Instructions */
.map-instructions { position: absolute; top: 20px; right: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); max-width: 300px; z-index: 100; }
.instruction-content h3 { font-size: 16px; margin-bottom: 10px; color: #667eea; }
.instruction-content ol { margin-left: 20px; font-size: 13px; line-height: 1.6; }

/* Loading Overlay */
.loading-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 255, 255, 0.9); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 1000; }
.spinner { width: 50px; height: 50px; border: 5px solid #f3f3f3; border-top: 5px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.loading-overlay p { margin-top: 20px; font-size: 16px; color: #667eea; font-weight: 600; }

/* Footer */
.app-footer { background: #2c3e50; color: white; text-align: center; padding: 15px; font-size: 12px; }

/* Scrollbar */
.control-panel::-webkit-scrollbar { width: 8px; }
.control-panel::-webkit-scrollbar-track { background: #f1f1f1; }
.control-panel::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; }

/* Animations */
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 0.8; } }
.fire-origin-marker { z-index: 1000 !important; }
.leaflet-popup-content-wrapper { border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
"""
    write_file(f"{base_dir}/frontend/css/style.css", css_content)
    
    # frontend/js/map.js - Split into manageable parts
    map_js_part1 = """/**
 * Leaflet Map - NO API KEYS REQUIRED!
 */

import { CONFIG } from '../config/config.js';

export let map;
export let fireOrigin = null;
export let fireOriginMarker = null;
export let fireZones = [];
export let allFireLayers = [];

function initMap() {
    map = L.map('map').setView(
        [CONFIG.DEFAULT_LOCATION.latitude, CONFIG.DEFAULT_LOCATION.longitude],
        CONFIG.DEFAULT_LOCATION.zoom
    );
    
    L.tileLayer(CONFIG.MAP.tileLayer, {
        attribution: CONFIG.MAP.attribution,
        maxZoom: CONFIG.MAP.maxZoom
    }).addTo(map);
    
    L.control.scale().addTo(map);
    map.on('click', function(e) { setFireOrigin(e.latlng.lat, e.latlng.lng); });
    console.log('✅ Map initialized (FREE - No API keys!)');
    setTimeout(hideMapInstructions, 3000);
}

export function setFireOrigin(lat, lon) {
    fireOrigin = { lat, lon };
    document.getElementById('originCoords').innerHTML = `
        <span>Lat: ${lat.toFixed(4)}</span>
        <span>Lon: ${lon.toFixed(4)}</span>
    `;
    if (fireOriginMarker) map.removeLayer(fireOriginMarker);
    clearFireGraphics();
    
    const fireIcon = L.divIcon({
        className: 'fire-origin-marker',
        html: '<div style="background: #ff0000; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 20px rgba(255,0,0,0.8); animation: pulse 2s infinite;"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });
    
    fireOriginMarker = L.marker([lat, lon], { icon: fireIcon, title: 'Fire Origin' }).addTo(map);
    fireOriginMarker.bindPopup(`<b>🔥 Fire Origin</b><br>Lat: ${lat.toFixed(4)}<br>Lon: ${lon.toFixed(4)}`).openPopup();
    document.getElementById('runSimulation').disabled = false;
    console.log(`🔥 Fire origin set: ${lat.toFixed(4)}, ${lon.toFixed(4)}`);
}

export function addFireZones(zones) {
    clearFireZones();
    fireZones = zones;
    
    zones.forEach((zone, index) => {
        const latLngs = zone.perimeter.map(p => [p.lat, p.lon]);
        const intensity = zone.intensity;
        const hue = intensity * 60;
        const color = `hsl(${hue}, 100%, 50%)`;
        const fillOpacity = 0.3 + (intensity * 0.3);
        
        const polygon = L.polygon(latLngs, {
            color: color,
            fillColor: color,
            fillOpacity: fillOpacity,
            weight: 2,
            opacity: 0.8,
            zoneStep: zone.step
        }).addTo(map);
        
        polygon.bindPopup(`<b>Fire Zone ${zone.step}</b><br><b>Time:</b> ${zone.time} min<br><b>Distance:</b> ${zone.distance.toFixed(0)} m<br><b>Intensity:</b> ${(zone.intensity * 100).toFixed(0)}%`);
        allFireLayers.push(polygon);
    });
    
    if (zones.length > 0) {
        const heatPoints = [];
        zones.forEach(zone => {
            zone.perimeter.forEach(p => { heatPoints.push([p.lat, p.lon, zone.intensity]); });
        });
        const heatLayer = L.heatLayer(heatPoints, {
            radius: 25, blur: 35, maxZoom: 17, max: 1.0,
            gradient: { 0.0: 'yellow', 0.5: 'orange', 1.0: 'red' }
        }).addTo(map);
        allFireLayers.push(heatLayer);
        
        const allPoints = zones[zones.length - 1].perimeter.map(p => [p.lat, p.lon]);
        const bounds = L.latLngBounds(allPoints);
        map.fitBounds(bounds, { padding: [50, 50] });
    }
    console.log(`🔥 Added ${zones.length} fire zones`);
}

function clearFireZones() {
    allFireLayers.forEach(layer => { map.removeLayer(layer); });
    allFireLayers = [];
    fireZones = [];
}

export function clearFireGraphics() {
    clearFireZones();
    if (fireOriginMarker) { map.removeLayer(fireOriginMarker); fireOriginMarker = null; }
    fireOrigin = null;
    document.getElementById('originCoords').innerHTML = `<span>Lat: --</span><span>Lon: --</span>`;
    document.getElementById('runSimulation').disabled = true;
    console.log('🗑️ Cleared');
}

export function updateVisibleZones(maxStep) {
    allFireLayers.forEach(layer => {
        if (layer.options && layer.options.zoneStep !== undefined) {
            if (layer.options.zoneStep <= maxStep) {
                if (!map.hasLayer(layer)) map.addLayer(layer);
            } else {
                if (map.hasLayer(layer)) map.removeLayer(layer);
            }
        }
    });
}

function hideMapInstructions() {
    const instructions = document.getElementById('mapInstructions');
    if (instructions) {
        instructions.style.opacity = '0';
        setTimeout(() => { instructions.style.display = 'none'; }, 300);
    }
}

const style = document.createElement('style');
style.textContent = `@keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 0.8; } }`;
document.head.appendChild(style);

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
} else {
    initMap();
}

window.mapModule = { setFireOrigin, addFireZones, clearFireGraphics, updateVisibleZones, getFireOrigin: () => fireOrigin, getMap: () => map };
console.log('🗺️ Map loaded (Leaflet + OSM - FREE!)');
"""
    write_file(f"{base_dir}/frontend/js/map.js", map_js_part1)
    
    # frontend/js/fire-simulation.js
    write_file(f"{base_dir}/frontend/js/fire-simulation.js", """/**
 * Fire Simulation Logic
 */

import { CONFIG } from '../config/config.js';

let currentSimulation = null;

export async function runSimulation() {
    const fireOrigin = window.mapModule.getFireOrigin();
    if (!fireOrigin) { alert('Click map to set fire origin'); return; }
    
    const windSpeed = parseFloat(document.getElementById('windSpeed').value);
    const buildingDensity = parseFloat(document.getElementById('buildingDensity').value);
    const timeSteps = parseInt(document.getElementById('timeSteps').value);
    
    showLoading(true);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/simulate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lat: fireOrigin.lat, lon: fireOrigin.lon, windSpeed, buildingDensity, timeSteps })
        });
        
        if (!response.ok) throw new Error('Simulation failed');
        const result = await response.json();
        
        if (result.success) {
            currentSimulation = result.data;
            displaySimulationResults(result.data);
            visualizeFireSpread(result.data);
            console.log('✅ Simulation completed');
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Simulation error:', error);
        alert('Failed to run simulation. Make sure backend is running.');
    } finally {
        showLoading(false);
    }
}

function displaySimulationResults(data) {
    const { parameters, summary } = data;
    document.getElementById('resultUrbanWind').textContent = `${parameters.urbanWind.toFixed(1)} km/h`;
    document.getElementById('resultSpreadRate').textContent = `${parameters.spreadRate.toFixed(2)} m/min`;
    document.getElementById('resultMaxDistance').textContent = `${summary.maxDistance.toFixed(0)} m`;
    document.getElementById('resultTotalTime').textContent = `${summary.totalTime} min`;
    
    const sliderSection = document.getElementById('timeSliderSection');
    const timeSlider = document.getElementById('timeSlider');
    const timeDisplay = document.getElementById('timeDisplay');
    
    sliderSection.style.display = 'block';
    timeSlider.max = parameters.timeSteps;
    timeSlider.value = parameters.timeSteps;
    timeDisplay.textContent = `${summary.totalTime} minutes`;
    
    timeSlider.oninput = function() {
        const step = parseInt(this.value);
        const time = step * parameters.timeInterval;
        timeDisplay.textContent = step === 0 ? 'Origin' : `${time} minutes`;
        window.mapModule.updateVisibleZones(step);
    };
}

function visualizeFireSpread(data) {
    window.mapModule.addFireZones(data.zones);
}

export function clearSimulation() {
    currentSimulation = null;
    window.mapModule.clearFireGraphics();
    document.getElementById('resultUrbanWind').textContent = '--';
    document.getElementById('resultSpreadRate').textContent = '--';
    document.getElementById('resultMaxDistance').textContent = '--';
    document.getElementById('resultTotalTime').textContent = '--';
    document.getElementById('timeSliderSection').style.display = 'none';
    console.log('🗑️ Simulation cleared');
}

function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

window.runSimulation = runSimulation;
window.clearSimulation = clearSimulation;
console.log('🔥 Fire simulation module loaded');
""")
    
    # frontend/js/ui-controls.js
    write_file(f"{base_dir}/frontend/js/ui-controls.js", """/**
 * UI Controls
 */

import { CONFIG } from '../config/config.js';

document.addEventListener('DOMContentLoaded', function() {
    initializeControls();
    loadWeather();
    console.log('🎛️ UI controls initialized');
});

function initializeControls() {
    const windSpeed = document.getElementById('windSpeed');
    const windSpeedValue = document.getElementById('windSpeedValue');
    windSpeed.addEventListener('input', function() { windSpeedValue.textContent = this.value; });
    
    const buildingDensity = document.getElementById('buildingDensity');
    const buildingDensityValue = document.getElementById('buildingDensityValue');
    buildingDensity.addEventListener('input', function() { buildingDensityValue.textContent = this.value; });
    
    const timeSteps = document.getElementById('timeSteps');
    const timeStepsValue = document.getElementById('timeStepsValue');
    timeSteps.addEventListener('input', function() { timeStepsValue.textContent = this.value; });
    
    document.getElementById('runSimulation').disabled = true;
}

async function loadWeather() {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = '<div class="weather-loading">Loading weather...</div>';
    
    try {
        const { latitude, longitude } = CONFIG.DEFAULT_LOCATION;
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/weather?lat=${latitude}&lon=${longitude}`);
        if (!response.ok) throw new Error('Weather API failed');
        const result = await response.json();
        if (result.success) {
            displayWeather(result.data);
            const windSpeedControl = document.getElementById('windSpeed');
            const windSpeedValue = document.getElementById('windSpeedValue');
            windSpeedControl.value = Math.round(result.data.windSpeed);
            windSpeedValue.textContent = Math.round(result.data.windSpeed);
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Weather error:', error);
        weatherInfo.innerHTML = `<div class="weather-item"><label>Status</label><span style="color: #dc3545;">Unable to load</span></div>`;
    }
}

function displayWeather(data) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `
        <div class="weather-grid">
            <div class="weather-item"><label>🌡️ Temperature</label><span>${data.temperature}°C</span></div>
            <div class="weather-item"><label>💨 Wind Speed</label><span>${data.windSpeed} km/h</span></div>
            <div class="weather-item"><label>🧭 Direction</label><span>${data.windDirection}°</span></div>
            <div class="weather-item"><label>💧 Humidity</label><span>${data.humidity}%</span></div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #666; text-align: center;">${data.description} • ${data.location}</div>
        <div style="margin-top: 5px; font-size: 10px; color: #999; text-align: center;">${data.source}</div>
    `;
}

window.refreshWeather = function() { loadWeather(); };
console.log('🎛️ UI controls module loaded');
""")
    
    print()
    
    # ==================== README ====================
    
    print("Creating documentation...")
    
    readme_content = """# 🔥 Urban Fire Spread Prediction System

## 🎉 ZERO API KEYS REQUIRED!

A production-ready web application for simulating urban fire spread using Rothermel model.

## 🚀 Quick Start (3 Steps!)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Server
```bash
python app.py
```

### 3. Open Browser
```
http://localhost:5000
```

**That's it! No API keys needed!** ✅

## ✨ Features

- ✅ Interactive map with OpenStreetMap (FREE!)
- ✅ Click-to-simulate fire origin
- ✅ Real-time fire spread simulation
- ✅ Rothermel model adapted for urban environments
- ✅ Time slider for progression control
- ✅ Heat map visualization
- ✅ Weather integration (mock fallback)
- ✅ Beautiful responsive UI

## 🛠️ Technology Stack

- **Frontend:** Leaflet.js, OpenStreetMap, HTML/CSS/JS
- **Backend:** Python Flask, NumPy
- **Zero API keys required!**

## 📖 Usage

1. Wait for map to load (2-3 seconds)
2. Click anywhere on map to set fire origin
3. Adjust parameters (wind, density, steps)
4. Click "Run Simulation"
5. Explore results with time slider

## 🐛 Troubleshooting

**Map not loading?**
- Check internet connection
- Ensure Flask server is running

**Simulation fails?**
- Make sure backend is running: `python backend/app.py`
- Check browser console for errors

## 🎓 Credits

Based on HPAIR Impact Challenge Project  
Carnegie Mellon University

Uses free open-source tools:
- Leaflet.js
- OpenStreetMap
- Flask
- NumPy

## 📄 License

Educational and Research Use
"""
    write_file(f"{base_dir}/README.md", readme_content)
    
    print()
    print("=" * 60)
    print("✅ PROJECT CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print(f"📁 Project location: ./{base_dir}/")
    print()
    print("🚀 Next steps:")
    print()
    print("1. Install dependencies:")
    print(f"   cd {base_dir}/backend")
    print("   pip install -r requirements.txt")
    print()
    print("2. Start the server:")
    print("   python app.py")
    print()
    print("3. Open browser:")
    print("   http://localhost:5000")
    print()
    print("=" * 60)
    print("🎉 NO API KEYS REQUIRED - Just run and go!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)