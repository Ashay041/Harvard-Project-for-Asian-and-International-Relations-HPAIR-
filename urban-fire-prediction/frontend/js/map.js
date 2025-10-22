/**
 * Simplified Leaflet Map - Guaranteed to Load
 */

// Wait for everything to load
console.log('🗺️ Map script loading...');

// Global storage
window.fireOrigin = null;
window.fireOriginMarker = null;
window.allFireLayers = [];
window.map = null;

// Initialize map when DOM is ready
function initMap() {
    console.log('🗺️ Initializing map...');
    
    try {
        // Create map
        window.map = L.map('map', {
            center: [34.0522, -118.2437],
            zoom: 13
        });
        
        console.log('✅ Map object created');
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(window.map);
        
        console.log('✅ Map tiles added');
        
        // Add scale control
        L.control.scale().addTo(window.map);
        
        // Click handler
        window.map.on('click', function(e) {
            console.log('🖱️ Map clicked:', e.latlng);
            setFireOrigin(e.latlng.lat, e.latlng.lng);
        });
        
        console.log('✅ Map initialized successfully!');
        
        // Hide instructions after 3 seconds
        setTimeout(() => {
            const instructions = document.getElementById('mapInstructions');
            if (instructions) {
                instructions.style.transition = 'opacity 0.3s';
                instructions.style.opacity = '0';
                setTimeout(() => instructions.style.display = 'none', 300);
            }
        }, 3000);
        
    } catch (error) {
        console.error('❌ Map initialization error:', error);
    }
}

function setFireOrigin(lat, lon) {
    console.log('🔥 Setting fire origin:', lat, lon);
    
    // Store globally
    window.fireOrigin = { lat: lat, lon: lon };
    
    // Update UI coordinates
    document.getElementById('originCoords').innerHTML = `
        <span>Lat: ${lat.toFixed(4)}</span>
        <span>Lon: ${lon.toFixed(4)}</span>
    `;
    
    // Remove old marker
    if (window.fireOriginMarker) {
        window.map.removeLayer(window.fireOriginMarker);
    }
    
    // Clear old fire zones
    clearFireZones();
    
    // Create fire icon
    const fireIcon = L.divIcon({
        className: 'fire-origin-marker',
        html: `<div style="
            background: #ff0000;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 0 20px rgba(255,0,0,0.8);
            animation: pulse 2s infinite;
        "></div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });
    
    // Add marker
    window.fireOriginMarker = L.marker([lat, lon], {
        icon: fireIcon
    }).addTo(window.map);
    
    // Add popup
    window.fireOriginMarker.bindPopup(`
        <b>🔥 Fire Origin</b><br>
        Lat: ${lat.toFixed(4)}<br>
        Lon: ${lon.toFixed(4)}
    `).openPopup();
    
    // Enable simulation button
    const runBtn = document.getElementById('runSimulation');
    if (runBtn) {
        runBtn.disabled = false;
        console.log('✅ Simulation button enabled');
    }
    
    console.log('✅ Fire origin set successfully');
}

function addFireZones(zones) {
    console.log('🔥 Adding fire zones:', zones.length);
    
    clearFireZones();
    
    zones.forEach((zone, index) => {
        // Create polygon coordinates
        const latLngs = zone.perimeter.map(p => [p.lat, p.lon]);
        
        // Calculate color
        const intensity = zone.intensity;
        const hue = intensity * 60; // 0 = red, 60 = yellow
        const color = `hsl(${hue}, 100%, 50%)`;
        const fillOpacity = 0.3 + (intensity * 0.3);
        
        // Create polygon
        const polygon = L.polygon(latLngs, {
            color: color,
            fillColor: color,
            fillOpacity: fillOpacity,
            weight: 2,
            opacity: 0.8,
            zoneStep: zone.step
        }).addTo(window.map);
        
        // Add popup
        polygon.bindPopup(`
            <b>Fire Spread Zone ${zone.step}</b><br>
            <b>Time:</b> ${zone.time} minutes<br>
            <b>Distance:</b> ${zone.distance.toFixed(0)} meters<br>
            <b>Intensity:</b> ${(zone.intensity * 100).toFixed(0)}%
        `);
        
        window.allFireLayers.push(polygon);
    });
    
    // Add heat layer
    if (zones.length > 0 && typeof L.heatLayer !== 'undefined') {
        const heatPoints = [];
        zones.forEach(zone => {
            zone.perimeter.forEach(p => {
                heatPoints.push([p.lat, p.lon, zone.intensity]);
            });
        });
        
        const heatLayer = L.heatLayer(heatPoints, {
            radius: 25,
            blur: 35,
            maxZoom: 17,
            max: 1.0,
            gradient: {
                0.0: 'yellow',
                0.5: 'orange',
                1.0: 'red'
            }
        }).addTo(window.map);
        
        window.allFireLayers.push(heatLayer);
    }
    
    // Fit map to bounds
    if (zones.length > 0) {
        const allPoints = zones[zones.length - 1].perimeter.map(p => [p.lat, p.lon]);
        const bounds = L.latLngBounds(allPoints);
        window.map.fitBounds(bounds, { padding: [50, 50] });
    }
    
    console.log('✅ Fire zones added');
}

function clearFireZones() {
    window.allFireLayers.forEach(layer => {
        window.map.removeLayer(layer);
    });
    window.allFireLayers = [];
}

function clearFireGraphics() {
    console.log('🗑️ Clearing fire graphics');
    
    clearFireZones();
    
    if (window.fireOriginMarker) {
        window.map.removeLayer(window.fireOriginMarker);
        window.fireOriginMarker = null;
    }
    
    window.fireOrigin = null;
    
    document.getElementById('originCoords').innerHTML = `
        <span>Lat: --</span>
        <span>Lon: --</span>
    `;
    
    document.getElementById('runSimulation').disabled = true;
}

function updateVisibleZones(maxStep) {
    window.allFireLayers.forEach(layer => {
        if (layer.options && typeof layer.options.zoneStep !== 'undefined') {
            if (layer.options.zoneStep <= maxStep) {
                if (!window.map.hasLayer(layer)) {
                    window.map.addLayer(layer);
                }
            } else {
                if (window.map.hasLayer(layer)) {
                    window.map.removeLayer(layer);
                }
            }
        }
    });
}

// Add pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
`;
document.head.appendChild(style);

// Initialize when ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('📄 DOM loaded, initializing map...');
        setTimeout(initMap, 100);
    });
} else {
    console.log('📄 DOM already loaded, initializing map...');
    setTimeout(initMap, 100);
}

// Export functions
window.mapModule = {
    setFireOrigin,
    addFireZones,
    clearFireGraphics,
    updateVisibleZones,
    getFireOrigin: () => window.fireOrigin,
    getMap: () => window.map
};

console.log('✅ Map module script loaded');