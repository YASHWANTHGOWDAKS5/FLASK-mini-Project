import pandas as pd
import requests
from datetime import datetime

# Load your crop dataset
crop_file = r"D:\Downloads\35985678-0d79-46b4-9ed6-6f13308a1d24_d5e53de4e40bc3bf9b47091e499c9dfb.csv"
crop_df = pd.read_csv(crop_file)

# Convert Arrival_Date to datetime
crop_df['Arrival_Date'] = pd.to_datetime(crop_df['Arrival_Date'], format="%d/%m/%Y")

# Coordinates for Mandya
latitude = 12.5
longitude = 76.9

# Function to get weather for a given date
def get_weather(date):
    date_str = date.strftime("%Y%m%d")  # API needs YYYYMMDD format
    
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,RH2M,PS,PRECTOTCORR,WS2M",  # temp, humidity, pressure, rain, wind
        "start": date_str,
        "end": date_str,
        "latitude": latitude,
        "longitude": longitude,
        "community": "AG",
        "format": "JSON"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        values = {
            "Temp": data['properties']['parameter']['T2M'][date_str],
            "Humidity": data['properties']['parameter']['RH2M'][date_str],
            "Pressure": data['properties']['parameter']['PS'][date_str],
            "Rain": data['properties']['parameter']['PRECTOTCORR'][date_str],
            "Wind": data['properties']['parameter']['WS2M'][date_str],
        }
        return values
    except Exception as e:
        print(f"Error fetching {date_str}: {e}")
        return {"Temp": None, "Humidity": None, "Pressure": None, "Rain": None, "Wind": None}

# Create empty lists for weather data
temps, hums, press, rains, winds = [], [], [], [], []

# Loop through crop dataset and fetch weather for each date
for date in crop_df['Arrival_Date']:
    weather = get_weather(date)
    temps.append(weather["Temp"])
    hums.append(weather["Humidity"])
    press.append(weather["Pressure"])
    rains.append(weather["Rain"])
    winds.append(weather["Wind"])

# Add weather data to dataframe
crop_df['Temp'] = temps
crop_df['Humidity'] = hums
crop_df['Pressure'] = press
crop_df['Rain'] = rains
crop_df['Wind'] = winds

# Save final dataset
crop_df.to_csv("GreenChilly.csv", index=False)

print("✅ Done! File saved as crop_with_weather.csv")