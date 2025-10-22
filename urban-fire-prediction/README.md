# Urban Fire Spread Prediction System


A web application for simulating urban fire spread using Rothermel model.

## Quick Start (3 Steps!)

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

**That's it! No API keys needed!** 

## Features

- Interactive map with OpenStreetMap (FREE!)
- Click-to-simulate fire origin
- Real-time fire spread simulation
- Rothermel model adapted for urban environments
- Time slider for progression control
- Heat map visualization
- Weather integration (mock fallback)
- Beautiful responsive UI

## Technology Stack

- **Frontend:** Leaflet.js, OpenStreetMap, HTML/CSS/JS
- **Backend:** Python Flask, NumPy
- **Zero API keys required!**

## Usage

1. Wait for map to load (2-3 seconds)
2. Click anywhere on map to set fire origin
3. Adjust parameters (wind, density, steps)
4. Click "Run Simulation"
5. Explore results with time slider

## Troubleshooting

**Map not loading?**
- Check internet connection
- Ensure Flask server is running

**Simulation fails?**
- Make sure backend is running: `python backend/app.py`
- Check browser console for errors

## Credits

Based on HPAIR Impact Challenge Project  
Carnegie Mellon University

Uses free open-source tools:
- Leaflet.js
- OpenStreetMap
- Flask
- NumPy

## License

Educational and Research Use
