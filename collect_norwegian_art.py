import requests
import json
import time
from datetime import datetime

# List of Norwegian artists to collect data for
artists = [
    "Edvard Munch",
    "Johan Christian Dahl",
    "Christian Krohg",
    "Theodor Kittelsen",
    "Harriet Backer",
    "Kitty Lange Kielland",
    "Peter Nicolai Arbo",
    "Hans Gude",
    "Peder Balke",
    "Frits Thaulow",
    "Nikolai Astrup",
    "Odd Nerdrum",
    "Harald Sohlberg",
    "Erik Werenskiold",
    "Adolph Tidemand",
    "Lars Hertervig",
    "Oda Krohg",
    "Eilif Peterssen",
    "Hans Dahl",
    "Per Krohg",
    "August Cappelen",
    "Asta Nørregaard",
    "Amaldus Nielsen",
    "Christian Skredsvig",
    "Gunnar Berg",
    "Halfdan Egedius",
    "Thorolf Holmboe",
    "Jakob Weidemann",
    "Peder Aadnes",
    "Martin Aagaard",
    "Rolf Aamot",
    "Johannes Flintoe",
    "Rolf Groven",
    "Konrad Knudsen",
    "Wilhelm Peters",
    "Halvard Storm",
    "Jacob Gløersen",
    "Gustav Wentzel",
    "Oscar Wergeland",
    "Carl Sundt-Hansen",
    "Adelsteen Normann",
    "Axel Revold",
    "Jean Heiberg",
    "Olav Christopher Jenssen",
    "Bjarne Melgaard",
    "Fredrik Værslev",
    "Charlotte Wankel",
    "Inger Sitter",
    "Cora Sandel",
    "Paul René Gauguin"
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

# Helper to fetch artist gender and country from Wikidata (skip movement and image for speed)
def fetch_artist_extra_metadata(wikidata_id):
    sparql_query = f"""
    SELECT ?genderLabel ?countryLabel WHERE {{
      OPTIONAL {{ wd:{wikidata_id} wdt:P21 ?gender. }}
      OPTIONAL {{ wd:{wikidata_id} wdt:P27 ?country. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language 'en'. }}
    }}
    """
    wikidata_url = "https://query.wikidata.org/sparql"
    params = {"query": sparql_query, "format": "json"}
    response = safe_get(wikidata_url, params=params, headers=HEADERS)
    results = response.json()["results"]["bindings"]
    gender = country = None
    if results:
        res = results[0]
        gender = res.get("genderLabel", {}).get("value", None)
        country = res.get("countryLabel", {}).get("value", None)
    return gender, country

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

# Helper to guess century from year

def guess_century(year):
    if not year or not year[:4].isdigit():
        return None
    y = int(year[:4])
    if 1700 <= y < 1800:
        return "1700s"
    if 1800 <= y < 1900:
        return "1800s"
    if 1900 <= y < 2000:
        return "1900s"
    if 2000 <= y < 2100:
        return "2000s"
    return None

# Popular painters (top 10 by your list)
POPULAR_PAINTERS = set([
    "Edvard Munch", "Johan Christian Dahl", "Christian Krohg", "Theodor Kittelsen", "Harriet Backer",
    "Kitty Lange Kielland", "Peter Nicolai Arbo", "Hans Gude", "Peder Balke", "Frits Thaulow"
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
for artist in artists:
    print(f"Processing {artist}...")
    artist_meta = fetch_artist_metadata(artist)
    if not artist_meta:
        print(f"  Skipping {artist}: No metadata found.")
        continue
    # Fetch extra metadata
    gender, country = fetch_artist_extra_metadata(artist_meta["wikidata_id"])
    paintings = fetch_paintings_for_artist(artist, limit=20)
    # Attach artist metadata to each painting
    for painting in paintings:
        painting["artist_bio"] = artist_meta["bio"]
        painting["artist_birth"] = artist_meta["birth"]
        painting["artist_death"] = artist_meta["death"]
        painting["country_of_origin"] = country or "Norway"
        painting["artist_gender"] = gender or "unknown"
        # Guess genre
        painting["genre"] = guess_genre(painting["title"], painting.get("medium", ""))
        # Guess century
        century = guess_century(painting.get("year", ""))
        # Assign categories
        categories = []
        if artist in POPULAR_PAINTERS:
            categories.append("Popular painters")
        if painting["genre"] == "Landscape":
            categories.append("Landscapes")
        if painting["genre"] == "Portrait":
            categories.append("Portraits")
        if painting["genre"] == "Historical/Nationalism" or (country and "Norway" in country):
            categories.append("Historical/Nationalism")
        if century:
            categories.append(century)
        if painting.get("location", "").lower().find("national museum") != -1:
            categories.append("National Museum of Norway")
        if gender and gender.lower() == "female":
            categories.append("Women painters")
        painting["categories"] = categories
    all_paintings.extend(paintings)
    time.sleep(2)  # Be nice to the API

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