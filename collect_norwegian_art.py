import requests
import json
import time
from datetime import datetime

# List of Norwegian artists to collect data for
artists = [
    "Edvard Munch",
    "Johan Christian Dahl",
    "Hans Gude",
    "Christian Krohg",
    "Harald Sohlberg",
    "Frits Thaulow",
    "Theodor Kittelsen",
    "Adolph Tidemand",
    "Odd Nerdrum",
    "Nikolai Astrup"
]

# Output file
OUTPUT_FILE = "data/paintings.json"

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
    response = requests.get(wiki_api_url, params=params)
    response.raise_for_status()
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
    response = requests.get(wikidata_url, params=params)
    response.raise_for_status()
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
    response = requests.get(API_ENDPOINT, params=params)
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
    paintings = fetch_paintings_for_artist(artist, limit=20)
    # Attach artist metadata to each painting
    for painting in paintings:
        painting["artist_bio"] = artist_meta["bio"]
        painting["artist_birth"] = artist_meta["birth"]
        painting["artist_death"] = artist_meta["death"]
    all_paintings.extend(paintings)
    time.sleep(1)  # Be nice to the API

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