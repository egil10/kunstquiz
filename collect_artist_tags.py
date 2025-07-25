import requests
import json
import time
import os

# List of artists (should match your main script)
artists = [
    "Edvard Munch", "Harald Sohlberg", "Christian Krohg", "Frits Thaulow", "Erik Werenskiold", "Theodor Kittelsen", "Adolph Tidemand", "Hans Gude", "Kitty Lange Kielland", "Lars Hertervig", "Nikolai Astrup", "Oda Krohg", "Thorvald Erichsen", "Rolf Nesch", "Håkon Bleken", "Johan Christian Dahl", "Peder Balke", "Eilif Peterssen", "Hans Dahl", "Per Krohg", "August Cappelen", "Asta Nørregaard", "Amaldus Nielsen", "Christian Skredsvig", "Gunnar Berg", "Halfdan Egedius", "Thorolf Holmboe", "Jakob Weidemann", "Peder Aadnes", "Martin Aagaard", "Rolf Aamot", "Johannes Flintoe", "Rolf Groven", "Konrad Knudsen", "Wilhelm Peters", "Halvard Storm", "Jacob Gløersen", "Gustav Wentzel", "Oscar Wergeland", "Carl Sundt-Hansen", "Adelsteen Normann", "Axel Revold", "Jean Heiberg", "Olav Christopher Jenssen", "Bjarne Melgaard", "Fredrik Værslev", "Charlotte Wankel", "Inger Sitter", "Cora Sandel", "Paul René Gauguin", "Peder Severin Krøyer", "Thomas Fearnley", "Knud Baade", "Joachim Frich", "Morten Müller", "Johan Fredrik Eckersberg", "Otto Sinding", "Nils Hansteen", "Eyolf Soot", "Ludvig Karsten", "Henrik Lund", "Henrik Sørensen", "Pola Gauguin", "Rolf Nesch", "Olaf Gulbransson", "Bjarne Ness", "Ludvig Eikaas", "Kåre Tveter", "Kjell Aukrust", "Kåre Espolin Johnson", "Frans Widerberg", "Knut Rose", "Knut Rumohr", "Kjartan Slettemark", "Vebjørn Sand", "Håkon Gullvåg", "Ørnulf Opdahl", "Kjell Pahr-Iversen", "Lisa Aisato", "Gerhard Munthe", "Kjell Nupen", "Pushwagner", "Bjørn Ransve", "Arne Ekeland", "Kai Fjell", "Reidar Aulie", "Arne Texnes Kavli", "Søren Onsager", "Helge Ulving", "Nils Gude", "Bernt Lund", "Nils Elias Kristi", "Oluf Wold-Torne", "Sigurd Dancke", "Alf Lundeby", "Thorleif Stadheim", "Ida Lorentzen", "Marianne Aulie"
]

HEADERS = {
    "User-Agent": "kunstquiz/1.0 (your_email@example.com) Python requests"
}

# Simple translation mapping for common Norwegian terms
TRANSLATE = {
    'Kvinne': 'Female', 'kvinne': 'Female', 'mann': 'Male', 'Mann': 'Male',
    'Impresjonisme': 'Impressionism', 'Ekspresjonisme': 'Expressionism',
    'Romantikk': 'Romanticism', 'Nasjonalromantikk': 'National Romanticism',
    'Portrett': 'Portrait', 'Landskap': 'Landscape',
    'Billedkunstner': 'Visual artist', 'Maleri': 'Painting',
    'Kunstner': 'Artist', 'Kunst': 'Art', 'Kunstmaler': 'Painter',
    'Norge': 'Norway', 'norsk': 'Norwegian', 'Norsk': 'Norwegian',
}

def translate(val):
    if not val: return val
    for k, v in TRANSLATE.items():
        if val.strip().lower() == k.lower():
            return v
    return val

def fetch_tags_from_wikipedia(artist, lang='en'):
    tags = {}
    wiki_api_url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": artist,
        "prop": "pageprops|extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1
    }
    try:
        response = requests.get(wiki_api_url, params=params, headers=HEADERS)
        response.raise_for_status()
        pages = response.json()["query"]["pages"]
        page_id = list(pages.keys())[0]
        if page_id == "-1":
            return {"not_found": True}
        page = pages[page_id]
        wikidata_id = page.get("pageprops", {}).get("wikibase_item", None)
        if wikidata_id:
            sparql_query = f"""
            SELECT ?birth ?death ?movementLabel ?genreLabel ?countryLabel ?placeLabel ?genderLabel WHERE {{
              OPTIONAL {{ wd:{wikidata_id} wdt:P569 ?birth. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P570 ?death. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P135 ?movement. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P136 ?genre. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P27 ?country. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P19 ?place. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P21 ?gender. }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language '{lang},en'. }}
            }}
            """
            wikidata_url = "https://query.wikidata.org/sparql"
            params2 = {"query": sparql_query, "format": "json"}
            r2 = requests.get(wikidata_url, params=params2, headers=HEADERS)
            r2.raise_for_status()
            results = r2.json()["results"]["bindings"]
            if results:
                res = results[0]
                tags["birth"] = res.get("birth", {}).get("value", None)
                tags["death"] = res.get("death", {}).get("value", None)
                tags["movement"] = translate(res.get("movementLabel", {}).get("value", None))
                tags["genre"] = translate(res.get("genreLabel", {}).get("value", None))
                tags["country"] = translate(res.get("countryLabel", {}).get("value", None))
                tags["birthplace"] = res.get("placeLabel", {}).get("value", None)
                gender = res.get("genderLabel", {}).get("value", None)
                tags["gender"] = translate(gender)
                tags["is_female"] = (gender and gender.lower() in ["female", "kvinne"])
        tags["summary"] = page.get("extract", "")
        # Notable works (from Wikidata)
        if wikidata_id:
            sparql_query2 = f"""
            SELECT ?workLabel ?workYear WHERE {{
              wd:{wikidata_id} wdt:P800 ?work.
              OPTIONAL {{ ?work wdt:P571 ?workYear. }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language '{lang},en'. }}
            }}
            """
            params3 = {"query": sparql_query2, "format": "json"}
            r3 = requests.get(wikidata_url, params=params3, headers=HEADERS)
            r3.raise_for_status()
            works = []
            for res in r3.json()["results"]["bindings"]:
                work = res.get("workLabel", {}).get("value", None)
                year = res.get("workYear", {}).get("value", None)
                works.append({"title": work, "year": year})
            if works:
                tags["notable_works"] = works
        return tags
    except Exception as e:
        print(f"  Error fetching for {artist} ({lang}): {e}")
        return {"not_found": True}

artist_tags = {}
women_count = 0
for artist in artists:
    print(f"Fetching tags for {artist}...")
    tags_en = fetch_tags_from_wikipedia(artist, lang='en')
    tags_no = fetch_tags_from_wikipedia(artist, lang='no')
    tags = {}
    # Merge, prefer Norwegian for missing/empty fields
    for k in set(tags_en.keys()).union(tags_no.keys()):
        v_en = tags_en.get(k)
        v_no = tags_no.get(k)
        tags[k] = v_en if v_en else v_no
    # Count women
    if tags.get("is_female"): women_count += 1
    artist_tags[artist] = tags
    time.sleep(1)

output_path = "data/artist_tags.json"
appended_path = "data/artist_tags_appended.json"

# Load existing tags if present
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        try:
            existing_tags = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing tags: {e}")
            existing_tags = {}
else:
    existing_tags = {}

# Merge new tags with existing, prefer new data for updated fields
for artist, tags in artist_tags.items():
    if artist in existing_tags:
        existing_tags[artist].update(tags)
    else:
        existing_tags[artist] = tags

with open(appended_path, "w", encoding="utf-8") as f:
    json.dump(existing_tags, f, indent=2, ensure_ascii=False)

print(f"✅ Appended and saved artist tags to {appended_path}")
print(f"\nTotal women painters found: {women_count}") 