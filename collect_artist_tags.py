import requests
import json
import time

# List of artists (should match your main script)
artists = [
    "Edvard Munch", "Harald Sohlberg", "Christian Krohg", "Frits Thaulow", "Erik Werenskiold", "Theodor Kittelsen", "Adolph Tidemand", "Hans Gude", "Kitty Lange Kielland", "Lars Hertervig", "Nikolai Astrup", "Oda Krohg", "Thorvald Erichsen", "Rolf Nesch", "Håkon Bleken", "Johan Christian Dahl", "Peder Balke", "Eilif Peterssen", "Hans Dahl", "Per Krohg", "August Cappelen", "Asta Nørregaard", "Amaldus Nielsen", "Christian Skredsvig", "Gunnar Berg", "Halfdan Egedius", "Thorolf Holmboe", "Jakob Weidemann", "Peder Aadnes", "Martin Aagaard", "Rolf Aamot", "Johannes Flintoe", "Rolf Groven", "Konrad Knudsen", "Wilhelm Peters", "Halvard Storm", "Jacob Gløersen", "Gustav Wentzel", "Oscar Wergeland", "Carl Sundt-Hansen", "Adelsteen Normann", "Axel Revold", "Jean Heiberg", "Olav Christopher Jenssen", "Bjarne Melgaard", "Fredrik Værslev", "Charlotte Wankel", "Inger Sitter", "Cora Sandel", "Paul René Gauguin", "Peder Severin Krøyer", "Thomas Fearnley", "Knud Baade", "Joachim Frich", "Morten Müller", "Johan Fredrik Eckersberg", "Otto Sinding", "Nils Hansteen", "Eyolf Soot", "Ludvig Karsten", "Henrik Lund", "Henrik Sørensen", "Pola Gauguin", "Rolf Nesch", "Olaf Gulbransson", "Bjarne Ness", "Ludvig Eikaas", "Kåre Tveter", "Kjell Aukrust", "Kåre Espolin Johnson", "Frans Widerberg", "Knut Rose", "Knut Rumohr", "Kjartan Slettemark", "Vebjørn Sand", "Håkon Gullvåg", "Ørnulf Opdahl", "Kjell Pahr-Iversen", "Lisa Aisato", "Gerhard Munthe", "Kjell Nupen", "Pushwagner", "Bjørn Ransve", "Arne Ekeland", "Kai Fjell", "Reidar Aulie", "Arne Texnes Kavli", "Søren Onsager", "Helge Ulving", "Nils Gude", "Bernt Lund", "Nils Elias Kristi", "Oluf Wold-Torne", "Sigurd Dancke", "Alf Lundeby", "Thorleif Stadheim", "Ida Lorentzen", "Marianne Aulie"
]

HEADERS = {
    "User-Agent": "kunstquiz/1.0 (your_email@example.com) Python requests"
}

artist_tags = {}
for artist in artists:
    print(f"Fetching tags for {artist}...")
    tags = {}
    # Step 1: Get Wikipedia page
    wiki_api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": artist,
        "prop": "pageprops|extracts|revisions|categories|info|links|langlinks|templates|images|extlinks|iwlinks|coordinates|pageimages|pageterms|description|categories|revisions",
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
            print(f"  Skipping {artist}: Wikipedia page not found.")
            continue
        page = pages[page_id]
        # Extract birth/death from Wikidata if available
        wikidata_id = page.get("pageprops", {}).get("wikibase_item", None)
        if wikidata_id:
            sparql_query = f"""
            SELECT ?birth ?death ?movementLabel ?genreLabel ?countryLabel ?placeLabel WHERE {{
              OPTIONAL {{ wd:{wikidata_id} wdt:P569 ?birth. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P570 ?death. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P135 ?movement. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P136 ?genre. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P27 ?country. }}
              OPTIONAL {{ wd:{wikidata_id} wdt:P19 ?place. }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language 'en'. }}
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
                tags["movement"] = res.get("movementLabel", {}).get("value", None)
                tags["genre"] = res.get("genreLabel", {}).get("value", None)
                tags["country"] = res.get("countryLabel", {}).get("value", None)
                tags["birthplace"] = res.get("placeLabel", {}).get("value", None)
        # Extract summary/description
        tags["summary"] = page.get("extract", "")
        # Notable works (from Wikidata)
        if wikidata_id:
            sparql_query2 = f"""
            SELECT ?workLabel ?workYear WHERE {{
              wd:{wikidata_id} wdt:P800 ?work.
              OPTIONAL {{ ?work wdt:P571 ?workYear. }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language 'en'. }}
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
        artist_tags[artist] = tags
    except Exception as e:
        print(f"  Error fetching for {artist}: {e}")
    time.sleep(1)

output_path = "data/artist_tags.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(artist_tags, f, indent=2, ensure_ascii=False)

print(f"✅ Saved artist tags to {output_path}") 