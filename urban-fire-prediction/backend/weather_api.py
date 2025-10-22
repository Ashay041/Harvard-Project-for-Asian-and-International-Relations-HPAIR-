"""
Weather API Integration
Fetches real-time weather data from OpenWeatherMap
"""

import requests
import os
from datetime import datetime

class WeatherAPI:
    """OpenWeatherMap API wrapper for weather data"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY', '')
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        
    def get_weather(self, lat, lon):
        """Get current weather data for location"""
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
        """Generate mock weather data for testing"""
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
