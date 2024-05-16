import requests
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import find_dotenv, load_dotenv

api_key = os.getenv('API_KEY')

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

cafe_fotos = []
web_adressen = []

api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

params = {
    'query' : f'Cafes in Berlin with remote work opportunity',
    'key': api_key,
    'limit': 10
}


"""response = requests.get(api_url, params=params)
places_data = response.json()

ersten_5_ergebnisse = places_data.get('results', [])[:5]

for place in places_data['results']:
    print(place.get("name"), place.get("formatted_address"))

    print("----")

    # Details-Anfrage für jedes Café durchführen, um Bilder zu erhalten
    place_id = place.get('place_id')
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        'place_id': place_id,
        'key': api_key,
        'limit': 5,
    }

    details_response = requests.get(details_url, params=details_params)
    details_data = details_response.json()

    web_adresse = details_data["result"].get("website")
    web_adressen.append(web_adresse)



    # Verarbeite die Bilder für den Ort
    photos = details_data.get('result', {}).get('photos', [])[:1]
    if photos:
        print("Bilder:")
        for photo_info in photos:
            photo_reference = photo_info.get('photo_reference')
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
            print(photo_url)
            #cafe_fotos.append(photo_url)

    else:
        print("Keine Bilder verfügbar.")
    print("----")

"""

    #api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

such_ort = "Berlin"

@app.route('/', methods=['GET', "POST"])
def start():
    global such_ort
    global cafe_fotos

    such_ort = such_ort.capitalize()

    print(f"Suchort: {such_ort}")

    params = {
        'query': f'Cafes in {such_ort} with remote work opportunity',
        'key': api_key,
        'limit': 10
    }

    response = requests.get(api_url, params=params)
    places_data = response.json()

    for place in places_data['results']:
        print(place.get("name"), place.get("formatted_address"))

        print("----")

        # Details-Anfrage für jedes Café durchführen, um Bilder zu erhalten
        place_id = place.get('place_id')
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'key': api_key,
            'limit': 10,
        }

        details_response = requests.get(details_url, params=details_params)
        details_data = details_response.json()

        web_adresse = details_data["result"].get("website")
        web_adressen.append(web_adresse)

        telefonnummer = details_data["result"].get("formatted_phone_number")
        print(f"Telefonnummer: {telefonnummer}")

        # Verarbeite die Bilder für den Ort
        photos = details_data.get('result', {}).get('photos', [])[:1]

        if photos:
            print("Bilder:")
            for photo_info in photos:
                photo_reference = photo_info.get('photo_reference')
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                print(photo_url)
                cafe_fotos.append(photo_url)

        else:
            print("Keine Bilder verfügbar.")
        print("----")

    if request.method == "POST":
        #global cafe_fotos
        such_ort = request.form.get("search_location")

        cafe_fotos = []

        return redirect(url_for("start"))


    return render_template('start.html', cafes_data = places_data['results'], web_adressen = web_adressen, cafe_fotos = cafe_fotos, such_ort = such_ort)



@app.route("/api_laden")
def api_laden():
    params = {
        'query': f'Cafes in {such_ort} with remote work opportunity',
        'key': api_key,
        'limit': 5
    }

    response = requests.get(api_url, params=params)
    places_data = response.json()

    ersten_5_ergebnisse = places_data.get('results', [])[:5]

    for place in places_data['results']:
        print(place.get("name"), place.get("formatted_address"))

        print("----")

        # Details-Anfrage für jedes Café durchführen, um Bilder zu erhalten
        place_id = place.get('place_id')
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'key': api_key,
            'limit': 5,
        }

        details_response = requests.get(details_url, params=details_params)
        details_data = details_response.json()

        web_adresse = details_data["result"].get("website")
        web_adressen.append(web_adresse)

        # Verarbeite die Bilder für den Ort
        photos = details_data.get('result', {}).get('photos', [])[:1]
        if photos:
            print("Bilder:")
            for photo_info in photos:
                photo_reference = photo_info.get('photo_reference')
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                print(photo_url)
                #cafe_fotos.append(photo_url)

        else:
            print("Keine Bilder verfügbar.")
        print("----")
    return redirect(url_for("start"))

"""@app.route('/')
def start():

    return render_template('start.html', cafes_data = data.get('results', []), cafe_fotos = cafe_fotos )
"""

if __name__ == '__main__':
    app.run(debug =True, port=5001)