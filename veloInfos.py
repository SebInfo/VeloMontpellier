import requests
import json

# URL de l'API des stations VéloMagg
API_URL = "https://portail-api-data.montpellier3m.fr/bikestation"
response = requests.get(API_URL, headers={"Accept": "application/json"})

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()  # Convertir la réponse en JSON
    # Afficher le JSON complet pour voir toutes les informations
    print(json.dumps(data, indent=4))
else:
    print(f"Erreur {response.status_code}: Impossible de récupérer les données.")
