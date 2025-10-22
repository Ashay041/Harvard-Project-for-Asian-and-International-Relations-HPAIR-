/**
 * Fire Simulation - Simplified
 */

console.log('🔥 Fire simulation script loading...');

let currentSimulation = null;

async function runSimulation() {
    console.log('🎯 Running simulation...');
    
    // Get fire origin
    const fireOrigin = window.fireOrigin;
    
    if (!fireOrigin || !fireOrigin.lat || !fireOrigin.lon) {
        console.error('❌ No fire origin set!');
        alert('Please click on the map to set a fire origin point first!');
        return;
    }
    
    console.log('✅ Fire origin:', fireOrigin);
    
    // Get parameters
    const windSpeed = parseFloat(document.getElementById('windSpeed').value);
    const buildingDensity = parseFloat(document.getElementById('buildingDensity').value);
    const timeSteps = parseInt(document.getElementById('timeSteps').value);
    
    console.log('📊 Parameters:', { windSpeed, buildingDensity, timeSteps });
    
    // Show loading
    showLoading(true);
    
    try {
        const config = window.CONFIG || { API_BASE_URL: 'http://127.0.0.1:5001' };
        const url = `${config.API_BASE_URL}/api/simulate`;
        
        const requestBody = {
            lat: fireOrigin.lat,
            lon: fireOrigin.lon,
            windSpeed: windSpeed,
            buildingDensity: buildingDensity,
            timeSteps: timeSteps
        };
        
        console.log('📡 Sending to:', url);
        console.log('📦 Request:', requestBody);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        
        console.log('📨 Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Backend error:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const result = await response.json();
        console.log('✅ Simulation result:', result);
        
        if (result.success) {
            currentSimulation = result.data;
            displaySimulationResults(result.data);
            visualizeFireSpread(result.data);
            console.log('🎉 Simulation completed!');
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('❌ Simulation failed:', error);
        alert(`Failed to run simulation:\n\n${error.message}\n\nMake sure backend is running on port 5001`);
    } finally {
        showLoading(false);
    }
}

function displaySimulationResults(data) {
    console.log('📊 Displaying results...');
    
    const { parameters, summary } = data;
    
    document.getElementById('resultUrbanWind').textContent = `${parameters.urbanWind.toFixed(1)} km/h`;
    document.getElementById('resultSpreadRate').textContent = `${parameters.spreadRate.toFixed(2)} m/min`;
    document.getElementById('resultMaxDistance').textContent = `${summary.maxDistance.toFixed(0)} m`;
    document.getElementById('resultTotalTime').textContent = `${summary.totalTime} min`;
    
    // Show time slider
    const sliderSection = document.getElementById('timeSliderSection');
    const timeSlider = document.getElementById('timeSlider');
    const timeDisplay = document.getElementById('timeDisplay');
    
    if (sliderSection && timeSlider && timeDisplay) {
        sliderSection.style.display = 'block';
        timeSlider.max = parameters.timeSteps;
        timeSlider.value = parameters.timeSteps;
        timeDisplay.textContent = `${summary.totalTime} minutes`;
        
        timeSlider.oninput = function() {
            const step = parseInt(this.value);
            const time = step * parameters.timeInterval;
            timeDisplay.textContent = step === 0 ? 'Origin' : `${time} minutes`;
            
            if (window.mapModule && window.mapModule.updateVisibleZones) {
                window.mapModule.updateVisibleZones(step);
            }
        };
    }
    
    console.log('✅ Results displayed');
}

function visualizeFireSpread(data) {
    console.log('🗺️ Visualizing fire spread...');
    
    if (window.mapModule && window.mapModule.addFireZones) {
        window.mapModule.addFireZones(data.zones);
        console.log('✅ Fire zones added to map');
    } else {
        console.error('❌ mapModule not available');
    }
}

function clearSimulation() {
    console.log('🗑️ Clearing simulation...');
    
    currentSimulation = null;
    
    if (window.mapModule && window.mapModule.clearFireGraphics) {
        window.mapModule.clearFireGraphics();
    }
    
    document.getElementById('resultUrbanWind').textContent = '--';
    document.getElementById('resultSpreadRate').textContent = '--';
    document.getElementById('resultMaxDistance').textContent = '--';
    document.getElementById('resultTotalTime').textContent = '--';
    
    const sliderSection = document.getElementById('timeSliderSection');
    if (sliderSection) {
        sliderSection.style.display = 'none';
    }
    
    console.log('✅ Simulation cleared');
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
    }
}

// Make functions globally available
window.runSimulation = runSimulation;
window.clearSimulation = clearSimulation;

console.log('✅ Fire simulation module loaded');