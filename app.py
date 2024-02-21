from flask import Flask, render_template, request, redirect, app
import requests

# Setze deinen Yelp API-Schlüssel hier ein
api_key = "HyO5aDah32-3lSGI23UdliF9KtVYGFHwNQ1EC-Ugv-fuvuGfZpCXer5aoIyqnPTP0IcXV0TLRdv5BN1cu2KH3JoBb6R-33lhdykXrTTrDqmYdLPfiMkoWPPB4d3UZXYx"
client_id = "FQ8z2EZtw64VHAA_RcTprg"


# Die URL des Yelp API-Endpunkts für die Geschäftssuche
api_url = "https://api.yelp.com/v3/businesses/search"

# Parameter für die Suche (z.B. nach Cafés mit WLAN)
params = {
    'term': 'cafe',
    'location': 'Berlin',  # Setze den Namen deiner Stadt hier ein
    'attributes': 'wifi',
    "limit" : 50 
}

# Setze den API-Schlüssel im Header
headers = {
    'Authorization': f'Bearer {api_key}',
}

# Sende die Anfrage an die Yelp API
response = requests.get(api_url, params=params, headers=headers)

# Überprüfe den Statuscode der Antwort
if response.status_code == 200:
    # Konvertiere die Antwort in JSON
    data = response.json()

    # Extrahiere und verarbeite die relevanten Informationen (z.B. Namen der Cafés)
    for business in data.get('businesses', []):
        print("Café Name:", business.get('name'))

        photos = business.get('photos', [])
        if photos:
            # Gib die URLs der Fotos aus
            print("Fotos:")
            for photo_url in photos:
                print(photo_url)
        else:
            print("Keine Fotos verfügbar.")
else:
    print("Fehler beim API-Aufruf. Statuscode:", response.status_code)
    print("Fehlermeldung:", response.text)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimeschluessel'

@app.route('/')
def start():
    return render_template('start.html')


if __name__ == '__main__':
    app.run(debug =True, port=5001)