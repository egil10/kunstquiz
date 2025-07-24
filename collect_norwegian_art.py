import requests
import json
import time
from datetime import datetime
import re
import os

# Expanded list of 100 Norwegian painters
artists = [
    "Edvard Munch", "Johan Christian Dahl", "Christian Krohg", "Theodor Kittelsen", "Harriet Backer", "Kitty Lange Kielland", "Peter Nicolai Arbo", "Hans Gude", "Peder Balke", "Frits Thaulow", "Nikolai Astrup", "Odd Nerdrum", "Harald Sohlberg", "Erik Werenskiold", "Adolph Tidemand", "Lars Hertervig", "Oda Krohg", "Eilif Peterssen", "Hans Dahl", "Per Krohg", "August Cappelen", "Asta Nørregaard", "Amaldus Nielsen", "Christian Skredsvig", "Gunnar Berg", "Halfdan Egedius", "Thorolf Holmboe", "Jakob Weidemann", "Peder Aadnes", "Martin Aagaard", "Rolf Aamot", "Johannes Flintoe", "Rolf Groven", "Konrad Knudsen", "Wilhelm Peters", "Halvard Storm", "Jacob Gløersen", "Gustav Wentzel", "Oscar Wergeland", "Carl Sundt-Hansen", "Adelsteen Normann", "Axel Revold", "Jean Heiberg", "Olav Christopher Jenssen", "Bjarne Melgaard", "Fredrik Værslev", "Charlotte Wankel", "Inger Sitter", "Cora Sandel", "Paul René Gauguin", "Peder Severin Krøyer", "Thomas Fearnley", "Knud Baade", "Joachim Frich", "Morten Müller", "Johan Fredrik Eckersberg", "Otto Sinding", "Nils Hansteen", "Eyolf Soot", "Ludvig Karsten", "Thorvald Erichsen", "Henrik Lund", "Henrik Sørensen", "Pola Gauguin", "Rolf Nesch", "Olaf Gulbransson", "Bjarne Ness", "Ludvig Eikaas", "Kåre Tveter", "Kjell Aukrust", "Kåre Espolin Johnson", "Frans Widerberg", "Håkon Bleken", "Knut Rose", "Knut Rumohr", "Kjartan Slettemark", "Vebjørn Sand", "Håkon Gullvåg", "Ørnulf Opdahl", "Kjell Pahr-Iversen", "Lisa Aisato", "Gerhard Munthe", "Kjell Nupen", "Pushwagner", "Bjørn Ransve", "Arne Ekeland", "Kai Fjell", "Reidar Aulie", "Arne Texnes Kavli", "Søren Onsager", "Helge Ulving", "Nils Gude", "Bernt Lund", "Nils Elias Kristi", "Oluf Wold-Torne", "Sigurd Dancke", "Alf Lundeby", "Thorleif Stadheim", "Ida Lorentzen", "Marianne Aulie"
]

# Output file
OUTPUT_FILE = "data/paintings.json"

HEADERS = {
    "User-Agent": "kunstquiz/1.0 (your_email@example.com) Python requests"
}

def safe_get(url, params=None, headers=None, max_retries=5):
    for attempt in range(max_retries):
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 429:
            print("Rate limited, sleeping 10s...")
            time.sleep(10)
            continue
        r.raise_for_status()
        return r
    raise Exception("Too many 429 errors")

# Helper to fetch artist metadata from Wikipedia/Wikidata
def fetch_artist_metadata(artist):
    wiki_api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": artist,
        "prop": "pageprops|extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1
    }
    response = safe_get(wiki_api_url, params=params, headers=HEADERS)
    pages = response.json()["query"]["pages"]
    page_id = list(pages.keys())[0]
    if page_id == "-1":
        return None
    bio = pages[page_id].get("extract", "No bio available.").strip()
    bio_sentences = bio.split('.')[:3]
    bio = '. '.join(bio_sentences) + '.' if bio_sentences else bio
    if "pageprops" not in pages[page_id]:
        return None
    wikidata_id = pages[page_id]["pageprops"]["wikibase_item"]
    # Get birth/death from Wikidata
    sparql_query = f"""
    SELECT ?birth ?death WHERE {{
      wd:{wikidata_id} wdt:P569 ?birth .
      OPTIONAL {{ wd:{wikidata_id} wdt:P570 ?death }}
    }}
    """
    wikidata_url = "https://query.wikidata.org/sparql"
    params = {"query": sparql_query, "format": "json"}
    response = safe_get(wikidata_url, params=params, headers=HEADERS)
    results = response.json()["results"]["bindings"]
    birth = death = "Unknown"
    if results:
        res = results[0]
        birth_raw = res.get("birth", {}).get("value", "Unknown")
        death_raw = res.get("death", {}).get("value", "Unknown")
        try:
            birth = datetime.fromisoformat(birth_raw.rstrip('Z')).strftime("%Y-%m-%d") if birth_raw != "Unknown" else "Unknown"
        except:
            birth = birth_raw.split('T')[0] if birth_raw != "Unknown" else "Unknown"
        try:
            death = datetime.fromisoformat(death_raw.rstrip('Z')).strftime("%Y-%m-%d") if death_raw != "Unknown" else "Unknown"
        except:
            death = death_raw.split('T')[0] if death_raw != "Unknown" else "Unknown"
    return {
        "artist": artist,
        "bio": bio,
        "birth": birth,
        "death": death,
        "wikidata_id": wikidata_id
    }

# Helper to fetch artist movement, gender, and country from Wikidata
def fetch_artist_extra_metadata(wikidata_id):
    sparql_query = f"""
    SELECT ?genderLabel ?countryLabel ?movementLabel WHERE {{
      OPTIONAL {{ wd:{wikidata_id} wdt:P21 ?gender. }}
      OPTIONAL {{ wd:{wikidata_id} wdt:P27 ?country. }}
      OPTIONAL {{ wd:{wikidata_id} wdt:P135 ?movement. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language 'en'. }}
    }}
    """
    wikidata_url = "https://query.wikidata.org/sparql"
    params = {"query": sparql_query, "format": "json"}
    response = safe_get(wikidata_url, params=params, headers=HEADERS)
    results = response.json()["results"]["bindings"]
    gender = country = movement = None
    if results:
        res = results[0]
        gender = res.get("genderLabel", {}).get("value", None)
        country = res.get("countryLabel", {}).get("value", None)
        movement = res.get("movementLabel", {}).get("value", None)
    return gender, country, movement

# Helper to guess genre from title/metadata

def guess_genre(title, medium):
    t = title.lower()
    if "portrait" in t or "self-portrait" in t:
        return "Portrait"
    if "landscape" in t or "fjord" in t or "mountain" in t or "nature" in t:
        return "Landscape"
    if "interior" in t:
        return "Interior"
    if "myth" in t or "legend" in t or "national" in t:
        return "Historical/Nationalism"
    if "still life" in t:
        return "Still Life"
    if medium and "etching" in medium.lower():
        return "Etching"
    return "Painting"

# Helper to compute century as integer (e.g., 19 for 1893)
def compute_century(year):
    if not year or not year[:4].isdigit():
        return None
    y = int(year[:4])
    return (y - 1) // 100 + 1

# Helper to clean collection/museum name from location
def extract_collection(location):
    if not location:
        return None
    # Try to extract museum/institution name from location string
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', location)
    # Look for common museum/institution keywords
    for word in ["Museum", "Gallery", "National", "Samling", "Collection", "Kunsthall", "Kunstmuseum", "Institutt", "Library"]:
        if word.lower() in text.lower():
            # Return the phrase containing the keyword
            match = re.search(r'([A-Z][^.,;\n]*' + word + '[^.,;\n]*)', text)
            if match:
                return match.group(1).strip()
    # Fallback: return first 40 chars as a guess
    return text[:40].strip()

# Top 15 popular painters (as provided)
POPULAR_PAINTERS = set([
    "Edvard Munch", "Harald Sohlberg", "Christian Krohg", "Frits Thaulow", "Erik Werenskiold", "Theodor Kittelsen", "Adolph Tidemand", "Hans Gude", "Kitty Lange Kielland", "Lars Hertervig", "Nikolai Astrup", "Oda Krohg", "Thorvald Erichsen", "Rolf Nesch", "Håkon Bleken"
])

# Helper to fetch paintings from Wikimedia Commons
API_ENDPOINT = "https://commons.wikimedia.org/w/api.php"
def extract_metadata(metadata, key):
    return metadata.get(key, {}).get("value", "").strip()

def fetch_paintings_for_artist(artist, limit=20):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f'filetype:bitmap incategory:"Paintings by {artist}"',
        "gsrlimit": limit,
        "gsrnamespace": 6,
        "prop": "imageinfo",
        "iiprop": "url|user|size|extmetadata"
    }
    response = safe_get(API_ENDPOINT, params=params, headers=HEADERS)
    if response.status_code != 200:
        return []
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    entries = []
    for page_id, page in pages.items():
        info = page.get("imageinfo", [{}])[0]
        metadata = info.get("extmetadata", {})
        url = info.get("url")
        raw_title = extract_metadata(metadata, "ObjectName") or page.get("title", "")
        title = raw_title.replace("File:", "").replace("_", " ").strip()
        entry = {
            "artist": artist,
            "title": title,
            "url": url,
            "year": extract_metadata(metadata, "DateTimeOriginal") or extract_metadata(metadata, "DateCreated"),
            "medium": extract_metadata(metadata, "Medium"),
            "dimensions": extract_metadata(metadata, "Dimensions"),
            "location": extract_metadata(metadata, "Credit"),
            "license": extract_metadata(metadata, "LicenseShortName"),
            "source": "Wikimedia Commons"
        }
        if url:
            entries.append(entry)
    return entries

# Main collection and merge logic
all_paintings = []
# Read existing paintings.json if it exists
existing_paintings = []
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        try:
            existing_paintings = json.load(f)
        except Exception:
            existing_paintings = []

# Build a set of unique keys for fast lookup
existing_keys = set((p['artist'], p['title'], p['url']) for p in existing_paintings)

# Fetch up to 100 paintings per artist
for artist in artists:
    print(f"Processing {artist}...")
    artist_meta = fetch_artist_metadata(artist)
    if not artist_meta:
        print(f"  Skipping {artist}: No metadata found.")
        continue
    # Fetch extra metadata
    gender, country, movement = fetch_artist_extra_metadata(artist_meta["wikidata_id"])
    paintings = fetch_paintings_for_artist(artist, limit=100)  # Increased to 100
    # Note: Filtering out images that are photos of paintings (with frames, etc.) is not reliably possible with current Wikimedia metadata. Most images are direct scans or photos of the artwork, but some may include frames or gallery context. Manual curation or advanced image analysis would be needed for perfect filtering.
    # Attach artist metadata to each painting
    for painting in paintings:
        key = (painting['artist'], painting['title'], painting['url'])
        if key in existing_keys:
            continue  # skip duplicates
        painting["artist_bio"] = artist_meta["bio"]
        painting["artist_birth"] = artist_meta["birth"]
        painting["artist_death"] = artist_meta["death"]
        painting["country_of_origin"] = country or "Norway"
        painting["artist_gender"] = gender or "unknown"
        painting["movement"] = movement or ""
        # Guess genre
        painting["genre"] = guess_genre(painting["title"], painting.get("medium", ""))
        # Compute century
        painting["century"] = compute_century(painting.get("year", ""))
        # Clean collection
        painting["collection"] = extract_collection(painting.get("location", ""))
        # Assign categories (improved logic)
        categories = []
        if artist in POPULAR_PAINTERS:
            categories.append("Popular painters")
        if painting["genre"] == "Landscape" or (painting["title"] and any(word in painting["title"].lower() for word in ["landscape", "fjord", "mountain", "nature", "skog", "natt", "vann", "elv", "river", "lake", "forest", "fjell", "hav", "sea", "coast", "øy", "island"])):
            categories.append("Landscapes")
        if painting["genre"] == "Portrait" or (painting["title"] and any(word in painting["title"].lower() for word in ["portrait", "self-portrait", "portrett", "kvinne", "mann", "barn", "girl", "boy", "woman", "man", "child"])):
            categories.append("Portraits")
        if movement and movement in ["Romanticism", "Neo-Romanticism", "Romantic Nationalism"]:
            categories.append("Romanticism")
        if movement and "Expressionism" in movement:
            categories.append("Expressionism")
        if movement and "Impressionism" in movement:
            categories.append("Impressionism")
        if painting["genre"] == "Historical/Nationalism" or (movement and "National" in movement) or (painting["title"] and any(word in painting["title"].lower() for word in ["myth", "legend", "national", "event", "history", "historisk", "nasjonal", "saga", "eventyr", "folk"])):
            categories.append("Historical/Nationalism")
        if painting["century"]:
            categories.append(f"{painting['century']}00s")
        collection = painting.get("collection") or ""
        if "national museum" in collection.lower():
            categories.append("National Museum of Norway")
        if gender and gender.lower() == "female":
            categories.append("Women painters")
        # Fallback: tag as 'Other' if no categories
        if not categories:
            categories.append("Other")
            print(f"  WARNING: Painting '{painting['title']}' by {artist} has no categories!")
        painting["categories"] = categories
        # Remove unnecessary fields
        for k in list(painting.keys()):
            if k.startswith("imageinfo") or k in ["user", "size", "extmetadata", "geocoordinates", "filemetadata"]:
                del painting[k]
        all_paintings.append(painting)
        existing_keys.add(key)
    time.sleep(2)  # Be nice to the API

# At the end, print a summary of paintings per category
from collections import Counter
cat_counter = Counter()
for p in all_paintings:
    for cat in p.get('categories', []):
        cat_counter[cat] += 1
print("\nPaintings per category:")
for cat, count in cat_counter.most_common():
    print(f"  {cat}: {count}")

# After category summary, print warnings for underrepresented categories
print("\nCategories with fewer than 5 paintings:")
for cat, count in cat_counter.items():
    if count < 5:
        print(f"  WARNING: {cat} only has {count} paintings!")

# Remove duplicates by (artist, title, url)
unique = {}
for p in all_paintings:
    key = (p["artist"], p["title"], p["url"])
    if key not in unique:
        unique[key] = p

final_paintings = list(unique.values())

# Save to JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_paintings, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(final_paintings)} paintings to {OUTPUT_FILE}") 