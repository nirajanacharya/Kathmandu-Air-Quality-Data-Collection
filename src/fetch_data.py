import requests
import pandas as pd
from tqdm import tqdm
from config import *

def get_kathmandu_locations():
    url = f"{BASE_URL}/locations"
    headers = {"X-API-Key": API_KEY}
    
    params = {
        "coordinates": f"{LATITUDE},{LONGITUDE}",
        "radius": RADIUS,
        "limit": 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print(f"ERROR: Error fetching locations: {response.status_code}")
        return []

def get_sensors_for_parameters(locations, parameters):
    sensors = []
    
    for location in locations:
        location_sensors = location.get("sensors", [])
        
        for sensor in location_sensors:
            param_name = sensor["parameter"]["name"]
            
            if param_name in parameters:
                sensors.append({
                    "sensor_id": sensor["id"],
                    "parameter": param_name,
                    "location_name": location["name"],
                    "location_id": location["id"]
                })
    
    return sensors

def fetch_sensor_measurements(sensor_id, date_from, date_to):
    url = f"{BASE_URL}/sensors/{sensor_id}/measurements"
    headers = {"X-API-Key": API_KEY}
    
    all_data = []
    page = 1
    max_pages = 10
    
    while page <= max_pages:
        params = {
            "date_from": date_from,
            "date_to": date_to,
            "limit": LIMIT,
            "page": page
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code != 200:
                break
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                break
            
            all_data.extend(results)
            
            if len(results) < LIMIT:
                break
            
            page += 1
            
        except Exception as e:
            print(f"WARNING: Error fetching sensor {sensor_id}: {str(e)[:50]}")
            break
    
    return all_data

def fetch_all_parameters():
    print("Finding monitoring locations near Kathmandu...")
    locations = get_kathmandu_locations()
    
    if not locations:
        print("ERROR: No locations found!")
        return pd.DataFrame()
    
    print(f"Found {len(locations)} locations\n")
    
    print("Extracting sensors...")
    sensors = get_sensors_for_parameters(locations, PARAMETERS)
    
    if not sensors:
        print(f"ERROR: No sensors found for: {PARAMETERS}")
        return pd.DataFrame()
    
    params_found = sorted(set(s['parameter'] for s in sensors))
    print(f"Found {len(sensors)} sensors")
    print(f"Parameters: {', '.join(params_found)}\n")
    
    all_measurements = []
    
    for sensor_info in tqdm(sensors, desc="Fetching measurements"):
        sensor_id = sensor_info["sensor_id"]
        parameter = sensor_info["parameter"]
        location_name = sensor_info["location_name"]
        
        measurements = fetch_sensor_measurements(sensor_id, DATE_FROM, DATE_TO)
        
        for m in measurements:
            m["parameter"] = parameter
            m["location_name"] = location_name
        
        all_measurements.extend(measurements)
    
    if not all_measurements:
        print("\nERROR: No measurements fetched!")
        return pd.DataFrame()
    
    df = pd.json_normalize(all_measurements)
    
    print(f"\nSuccessfully fetched {len(df):,} measurements")
    
    return df