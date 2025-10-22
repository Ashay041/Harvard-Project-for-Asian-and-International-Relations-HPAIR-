/**
 * UI Controls - Simplified
 */

console.log('🎛️ UI Controls loading...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎛️ Initializing controls...');
    initializeControls();
    loadWeather();
});

function initializeControls() {
    // Wind speed slider
    const windSpeed = document.getElementById('windSpeed');
    const windSpeedValue = document.getElementById('windSpeedValue');
    if (windSpeed && windSpeedValue) {
        windSpeed.addEventListener('input', function() {
            windSpeedValue.textContent = this.value;
        });
    }
    
    // Building density slider
    const buildingDensity = document.getElementById('buildingDensity');
    const buildingDensityValue = document.getElementById('buildingDensityValue');
    if (buildingDensity && buildingDensityValue) {
        buildingDensity.addEventListener('input', function() {
            buildingDensityValue.textContent = this.value;
        });
    }
    
    // Time steps slider
    const timeSteps = document.getElementById('timeSteps');
    const timeStepsValue = document.getElementById('timeStepsValue');
    if (timeSteps && timeStepsValue) {
        timeSteps.addEventListener('input', function() {
            timeStepsValue.textContent = this.value;
        });
    }
    
    // Disable simulation button initially
    const runBtn = document.getElementById('runSimulation');
    if (runBtn) {
        runBtn.disabled = true;
    }
    
    console.log('✅ Controls initialized');
}

async function loadWeather() {
    const weatherInfo = document.getElementById('weatherInfo');
    if (!weatherInfo) return;
    
    weatherInfo.innerHTML = '<div class="weather-loading">Loading weather...</div>';
    
    try {
        const config = window.CONFIG || { 
            API_BASE_URL: 'http://127.0.0.1:5001',
            DEFAULT_LOCATION: { latitude: 34.0522, longitude: -118.2437 }
        };
        
        const url = `${config.API_BASE_URL}/api/weather?lat=${config.DEFAULT_LOCATION.latitude}&lon=${config.DEFAULT_LOCATION.longitude}`;
        console.log('📡 Fetching weather from:', url);
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Weather data:', result);
        
        if (result.success) {
            displayWeather(result.data);
            
            // Update wind speed control
            const windSpeedControl = document.getElementById('windSpeed');
            const windSpeedValue = document.getElementById('windSpeedValue');
            if (windSpeedControl && windSpeedValue) {
                const windSpeed = Math.round(result.data.windSpeed);
                windSpeedControl.value = windSpeed;
                windSpeedValue.textContent = windSpeed;
            }
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('❌ Weather error:', error);
        weatherInfo.innerHTML = `
            <div style="padding: 10px; color: #dc3545; font-size: 12px;">
                <b>Status:</b> Unable to load<br>
                <small>${error.message}</small>
            </div>
        `;
    }
}

function displayWeather(data) {
    const weatherInfo = document.getElementById('weatherInfo');
    if (!weatherInfo) return;
    
    weatherInfo.innerHTML = `
        <div class="weather-grid">
            <div class="weather-item">
                <label>🌡️ Temperature</label>
                <span>${data.temperature}°C</span>
            </div>
            <div class="weather-item">
                <label>💨 Wind Speed</label>
                <span>${data.windSpeed} km/h</span>
            </div>
            <div class="weather-item">
                <label>🧭 Direction</label>
                <span>${data.windDirection}°</span>
            </div>
            <div class="weather-item">
                <label>💧 Humidity</label>
                <span>${data.humidity}%</span>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #666; text-align: center;">
            ${data.description} • ${data.location}
        </div>
        <div style="margin-top: 5px; font-size: 10px; color: #999; text-align: center;">
            ${data.source}
        </div>
    `;
}

window.refreshWeather = function() {
    console.log('🔄 Refreshing weather...');
    loadWeather();
};

console.log('✅ UI controls module loaded');