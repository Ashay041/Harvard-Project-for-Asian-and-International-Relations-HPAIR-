"""
Urban Fire Spread Model
Implements refined Rothermel model for urban environments
"""

import numpy as np
import math

class UrbanFireModel:
    """Fire spread model adapted for urban environments"""
    
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
        """Calculate wind speed in urban street canyon"""
        aspect_ratio = building_height / street_width
        urban_wind = base_wind_speed * (1 + self.CFD_CONSTANT * aspect_ratio)
        return round(urban_wind, 2)
    
    def calculate_spread_rate(self, wind_speed, building_density):
        """Calculate fire spread rate using Rothermel model"""
        wind_ms = wind_speed / 3.6
        
        numerator = (self.FUEL_ENERGY * self.PACKING_RATIO * 
                    (1 + (self.WIND_COEFFICIENT * wind_ms ** self.WIND_EXPONENT)))
        denominator = (self.FUEL_MOISTURE * self.FUEL_DEPTH * self.FUEL_DENSITY)
        
        density_factor = 1 - (building_density / 100)
        spread_rate = (numerator / denominator) * density_factor
        return round(spread_rate, 3)
    
    def calculate_spread_direction(self, origin_lat, origin_lon, angle_deg, distance_m):
        """Calculate new coordinates given origin, angle, and distance"""
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
        """Run complete fire spread simulation"""
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
