from flask import request, jsonify
import os
import pandas as pd

# Încarcă datele o singură dată
dataset_path = "."
csv_file = [f for f in os.listdir(dataset_path) if f.endswith(".csv")][0]
df = pd.read_csv(os.path.join(dataset_path, csv_file))

# Separă orașele de țări
if ',' in df.loc[0, 'City']:
    df[['CityName', 'Country']] = df['City'].str.split(',', expand=True)
    df['CityName'] = df['CityName'].str.strip()
    df['Country'] = df['Country'].str.strip()
else:
    df['CityName'] = df['City']
    df['Country'] = ''

# Adaugă coloane lowercase pentru căutare
df['CityName_lower'] = df['CityName'].str.lower()
df['Country_lower'] = df['Country'].str.lower()


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/crime_by_city")
def crime_by_city():
    city = request.args.get("city", "").strip().lower()
    result = df[df['CityName_lower'] == city]

    if result.empty:
        return jsonify({"error": "Orașul nu a fost găsit."}), 404

    data = result[['City', 'Crime Index', 'Safety Index']].to_dict(orient="records")
    return jsonify(data)


@app.route("/crime_by_country")
def crime_by_country():
    country = request.args.get("country", "").strip().lower()
    result = df[df['Country_lower'] == country]

    if result.empty:
        return jsonify({"error": "Țara nu a fost găsită sau nu are orașe înregistrate."}), 404

    data = result[['City', 'Crime Index', 'Safety Index']].to_dict(orient="records")
    return jsonify(data)


@app.route("/average_by_country")
def average_by_country():
    country = request.args.get("country", "").strip().lower()
    result = df[df['Country_lower'] == country]

    if result.empty:
        return jsonify({"error": "Țara nu a fost găsită sau nu are orașe înregistrate."}), 404

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
        return jsonify({"error": "Țara nu a fost găsită sau nu are orașe înregistrate."}), 404

    cities = result[['CityName', 'Crime Index', 'Safety Index']].to_dict(orient="records")
    return jsonify({"country": country.title(), "cities": cities})
