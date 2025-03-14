from flask import Flask, render_template
import requests
import folium

app = Flask(__name__)

# URL de l'API VéloMagg
API_URL = "https://portail-api-data.montpellier3m.fr/bikestation"


def generer_carte():
    # 📡 Récupération des données
    response = requests.get(API_URL, headers={"Accept": "application/json"})

    if response.status_code == 200:
        data = response.json()

        # Création de la carte centrée sur Montpellier
        map_montpellier = folium.Map(location=[43.610769, 3.876716], zoom_start=14)

        # Ajouter chaque station sur la carte
        for station in data:
            try:
                latitude = station["location"]["value"]["coordinates"][1]
                longitude = station["location"]["value"]["coordinates"][0]
                nom_station = station.get("id", "Station inconnue").replace("urn:ngsi-ld:", "")
                adresse = station["address"]["value"]["streetAddress"]
                velos_disponibles = station["availableBikeNumber"]["value"]

                # Personnalisation des marqueurs
                couleur = "green" if velos_disponibles > 5 else "red"
                popup_text = f"<br>Adresse: {adresse}<br>Dispo: {velos_disponibles}"

                folium.Marker(
                    location=[latitude, longitude],
                    popup=popup_text,
                    tooltip=nom_station,
                    icon=folium.Icon(color=couleur, icon="bicycle", prefix="fa")
                ).add_to(map_montpellier)

            except KeyError:
                print(f"Erreur avec la station {nom_station}, données manquantes.")

        return map_montpellier._repr_html_()  # Renvoie le HTML de la carte Folium

    return "<p>Erreur : Impossible de récupérer les données.</p>"


@app.route("/")
def home():
    return render_template("indexCarte.html", carte=generer_carte())  # 🔥 Intégrer la carte dans la page HTML


if __name__ == "__main__":
    app.run(debug=True)
