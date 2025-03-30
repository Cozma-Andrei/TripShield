from flask import Flask, request, jsonify
import os
import pandas as pd
import asyncio
import redisSetup
import sentiment.news
from datetime import datetime, timedelta
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

app = Flask(__name__)
load_dotenv()
r = redisSetup.setup()
geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))

dataset_path = "."
csv_file = [f for f in os.listdir(dataset_path) if f.endswith(".csv")][0]
df = pd.read_csv(os.path.join(dataset_path, csv_file))

def extract_city_country(full_city_str):
    parts = [part.strip() for part in full_city_str.split(',')]
    if len(parts) >= 2:
        country = parts[-1]
        city = ', '.join(parts[:-1])
        return pd.Series([city, country])
    else:
        return pd.Series([full_city_str.strip(), ""])

df[['CityName', 'Country']] = df['City'].apply(extract_city_country)
df['CityName_lower'] = df['CityName'].str.lower()
df['Country_lower'] = df['Country'].str.lower()

def get_coordinates(city, country):
    cache_key = f"coords:{city.lower()}:{country.lower()}"
    cached = r.get(cache_key)
    if cached:
        try:
            lat, lon = map(float, cached.decode().split(","))
            return lat, lon
        except:
            pass

    try:
        query = f"{city}, {country}"
        results = geocoder.geocode(query)
        if results and len(results):
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            r.set(cache_key, f"{lat},{lon}")
            return lat, lon
    except Exception as e:
        print(f"Eroare la geocodare pentru {query}: {e}")

    return None, None

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/crime_by_city")
def crime_by_city():
    city = request.args.get("city", "").strip().lower()
    result = df[df['CityName_lower'] == city]
    if result.empty:
        return jsonify({"error": "The city was not found."}), 404

    enriched = []
    for _, row in result.iterrows():
        lat, lon = get_coordinates(row['CityName'], row['Country'])
        enriched.append({
            "City": row['City'],
            "Crime Index": row['Crime Index'],
            "Safety Index": row['Safety Index'],
            "Latitude": lat,
            "Longitude": lon
        })
    return jsonify(enriched)

@app.route("/crime_by_country")
def crime_by_country():
    country = request.args.get("country", "").strip().lower()
    result = df[df['Country_lower'] == country]
    if result.empty:
        return jsonify({"error": "The country was not found."}), 404

    enriched = []
    for _, row in result.iterrows():
        lat, lon = get_coordinates(row['CityName'], row['Country'])
        enriched.append({
            "City": row['City'],
            "Crime Index": row['Crime Index'],
            "Safety Index": row['Safety Index'],
            "Latitude": lat,
            "Longitude": lon
        })
    return jsonify(enriched)

@app.route("/average_by_country")
def average_by_country():
    country = request.args.get("country", "").strip().lower()
    result = df[df['Country_lower'] == country]
    if result.empty:
        return jsonify({"error": "The country was not found."}), 404

    avg_crime = result['Crime Index'].mean()
    avg_safety = result['Safety Index'].mean()
    return jsonify({
        "country": country.title(),
        "average_crime_index": round(avg_crime, 2),
        "average_safety_index": round(avg_safety, 2),
        "city_count": len(result)
    })

@app.route("/all_cities_by_country")
def all_cities_by_country():
    country = request.args.get("country", "").strip().lower()
    result = df[df['Country_lower'] == country]
    if result.empty:
        return jsonify({"error": "The country was not found."}), 404

    enriched = []
    for _, row in result.iterrows():
        lat, lon = get_coordinates(row['CityName'], row['Country'])
        enriched.append({
            "CityName": row['CityName'],
            "Crime Index": row['Crime Index'],
            "Safety Index": row['Safety Index'],
            "Latitude": lat,
            "Longitude": lon
        })
    return jsonify({"country": country.title(), "cities": enriched})

if __name__ == "__main__":
    app.run(debug=True)
