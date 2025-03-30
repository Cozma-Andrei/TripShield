from flask import Flask, request, jsonify
import os
import pandas as pd
import asyncio
import redisSetup
import sentiment.news
from datetime import datetime, timedelta
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
from fuzzywuzzy import process

app = Flask(__name__)
load_dotenv()
r = redisSetup.setup()
geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))

# --- Load dataset ---
dataset_path = "."
csv_file = [f for f in os.listdir(dataset_path) if f.endswith(".csv")][0]
df = pd.read_csv(os.path.join(dataset_path, csv_file))

# --- Extract City and Country ---
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

# Ensure coordinate columns exist
if 'Latitude' not in df.columns:
    df['Latitude'] = None
if 'Longitude' not in df.columns:
    df['Longitude'] = None

# --- Coordinate caching ---
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
        query = f"{city}, {country}" if country else city
        results = geocoder.geocode(query)
        if results and len(results):
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            r.set(cache_key, f"{lat},{lon}")
            return lat, lon
    except Exception as e:
        print(f"Eroare la geocodare pentru {query}: {e}")

    return None, None

# --- Fuzzy Matching ---
def fuzzy_match_city(input_city):
    choices = df['CityName_lower'].unique()
    match, score = process.extractOne(input_city.lower(), choices)
    return match if score >= 70 else None

def fuzzy_match_country(input_country):
    choices = df['Country_lower'].unique()
    match, score = process.extractOne(input_country.lower(), choices)
    return match if score >= 70 else None

# --- Routes ---
@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/crime_by_city")
def crime_by_city():
    city = request.args.get("city", "").strip().lower()
    matched_city = fuzzy_match_city(city)

    # Dacă găsim orașul (inclusiv fuzzy), returnăm ca înainte
    if matched_city:
        result = df[df['CityName_lower'] == matched_city]
        enriched = []
        for _, row in result.iterrows():
            lat, lon = get_coordinates(row['CityName'], row['Country'])
            enriched.append({
                "Original Input": city,
                "Matched City": row['City'],
                "Crime Index": row['Crime Index'],
                "Safety Index": row['Safety Index'],
                "Latitude": lat,
                "Longitude": lon
            })
        return jsonify(enriched)

    # Dacă nu găsim orașul, încercăm să obținem coordonatele
    lat, lon = get_coordinates(city, "")
    if lat is None or lon is None:
        return jsonify({"error": "City not found and no coordinates available."}), 404

    # Facem reverse geocoding → obținem țara
    try:
        results = geocoder.reverse_geocode(lat, lon)
        if not results:
            raise Exception("No reverse geocode results.")
        country = results[0]['components'].get('country')
        if not country:
            raise Exception("No country in reverse geocode.")
    except Exception as e:
        return jsonify({"error": f"City not found. Couldn't determine country from coordinates: {e}"}), 404

    # Fuzzy match country in dataset
    matched_country = fuzzy_match_country(country)
    if not matched_country:
        return jsonify({"error": f"City '{city}' is in '{country}', but that country is not in dataset."}), 404

    # Returnăm media pe țară
    result = df[df['Country_lower'] == matched_country]
    avg_crime = result['Crime Index'].mean()
    avg_safety = result['Safety Index'].mean()

    return jsonify({
        "Original Input": city,
        "Detected Country": country,
        "Matched Country": result.iloc[0]['Country'],
        "Note": f"City not found. Returning country-level index for '{country}'.",
        "average_crime_index": round(avg_crime, 2),
        "average_safety_index": round(avg_safety, 2),
        "city_count": len(result)
    })

@app.route("/crime_by_country")
def crime_by_country():
    country = request.args.get("country", "").strip().lower()
    matched_country = fuzzy_match_country(country)
    if not matched_country:
        return jsonify({"error": "The country was not found, even after correction."}), 404

    result = df[df['Country_lower'] == matched_country]
    enriched = []
    for _, row in result.iterrows():
        lat, lon = get_coordinates(row['CityName'], row['Country'])
        enriched.append({
            "Original Input": country,
            "Matched Country": row['Country'],
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
    matched_country = fuzzy_match_country(country)
    if not matched_country:
        return jsonify({"error": "The country was not found, even after correction."}), 404

    result = df[df['Country_lower'] == matched_country]
    avg_crime = result['Crime Index'].mean()
    avg_safety = result['Safety Index'].mean()
    return jsonify({
        "Original Input": country,
        "Matched Country": result.iloc[0]['Country'],
        "average_crime_index": round(avg_crime, 2),
        "average_safety_index": round(avg_safety, 2),
        "city_count": len(result)
    })

@app.route("/all_cities_by_country")
def all_cities_by_country():
    country = request.args.get("country", "").strip().lower()
    matched_country = fuzzy_match_country(country)
    if not matched_country:
        return jsonify({"error": "The country was not found, even after correction."}), 404

    result = df[df['Country_lower'] == matched_country]
    enriched = []
    for _, row in result.iterrows():
        lat, lon = get_coordinates(row['CityName'], row['Country'])
        enriched.append({
            "Original Input": country,
            "Matched Country": row['Country'],
            "CityName": row['CityName'],
            "Crime Index": row['Crime Index'],
            "Safety Index": row['Safety Index'],
            "Latitude": lat,
            "Longitude": lon
        })
    return jsonify({"country": result.iloc[0]['Country'], "cities": enriched})

@app.route("/average_by_all_countries")
def average_by_all_countries():
    grouped = df.groupby("Country_lower").agg({
        "Crime Index": "mean",
        "Safety Index": "mean",
        "City": "count"
    }).reset_index()

    # Match original country name for display
    country_map = df.drop_duplicates(subset=["Country_lower"])[["Country_lower", "Country"]].set_index("Country_lower")["Country"].to_dict()

    result = []
    for _, row in grouped.iterrows():
        result.append({
            "country": country_map.get(row["Country_lower"], row["Country_lower"]).title(),
            "average_crime_index": round(row["Crime Index"], 2),
            "average_safety_index": round(row["Safety Index"], 2),
            "city_count": int(row["City"])
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
