from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# URL de l'API des stations de vélos
API_URL = "https://portail-api-data.montpellier3m.fr/bikestation"

@app.route("/stations")
def get_bike_stations():
    # Récupérer les données de l'API
    response = requests.get(API_URL, headers={"Accept": "application/json"})

    if response.status_code == 200:
        data = response.json()

        # Extraction des informations utiles
        stations = []
        for station in data:
            stations.append({
                "adresse": station["address"]["value"]["streetAddress"],
                "places_disponibles": station["availableBikeNumber"]["value"]
            })

        return jsonify(stations)  # Retourne un JSON avec les stations

    return jsonify({"error": "Impossible de récupérer les données"}), 500

@app.route("/")
def home():
    return render_template("index.html")  # Affiche une page HTML

if __name__ == "__main__":
    app.run(debug=True)
