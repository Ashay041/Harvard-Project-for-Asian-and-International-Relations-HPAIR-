/**
 * Configuration - NO API KEYS REQUIRED
 */

const CONFIG = {
    OPENWEATHER_API_KEY: '',
    
    DEFAULT_LOCATION: {
        latitude: 34.0522,
        longitude: -118.2437,
        zoom: 13
    },
    
    API_BASE_URL: 'http://127.0.0.1:5001',
    
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

// Export for ES6 modules
if (typeof exports !== 'undefined') {
    exports.CONFIG = CONFIG;
}

// Make available globally
window.CONFIG = CONFIG;

console.log('✅ Config loaded:', CONFIG);