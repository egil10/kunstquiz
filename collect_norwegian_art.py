import requests
import json
import time
from datetime import datetime
import re
import os

# Expanded list of 100 Norwegian painters
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
    "Paul René Gauguin",
    "Peder Severin Krøyer",
    "Thomas Fearnley",
    "Knud Baade",
    "Joachim Frich",
    "Morten Müller",
    "Johan Fredrik Eckersberg",
    "Otto Sinding",
    "Nils Hansteen",
    "Eyolf Soot",
    "Ludvig Karsten",
    "Thorvald Erichsen",
    "Henrik Lund",
    "Henrik Sørensen",
    "Pola Gauguin",
    "Rolf Nesch",
    "Olaf Gulbransson",
    "Bjarne Ness",
    "Ludvig Eikaas",
    "Kåre Tveter",
    "Kjell Aukrust",
    "Kåre Espolin Johnson",
    "Frans Widerberg",
    "Håkon Bleken",
    "Knut Rose",
    "Knut Rumohr",
    "Kjartan Slettemark",
    "Vebjørn Sand",
    "Håkon Gullvåg",
    "Ørnulf Opdahl",
    "Kjell Pahr-Iversen",
    "Lisa Aisato",
    "Gerhard Munthe",
    "Kjell Nupen",
    "Pushwagner",
    "Bjørn Ransve",
    "Arne Ekeland",
    "Kai Fjell",
    "Reidar Aulie",
    "Arne Texnes Kavli",
    "Søren Onsager",
    "Helge Ulving",
    "Nils Gude",
    "Bernt Lund",
    "Nils Elias Kristi",
    "Oluf Wold-Torne",
    "Sigurd Dancke",
    "Alf Lundeby",
    "Thorleif Stadheim",
    "Ida Lorentzen",
    "Marianne Aulie"
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
    # Try English, Bokmål, and Nynorsk Wikipedias in order
    wikis = [
        ("en", "https://en.wikipedia.org/w/api.php"),
        ("no", "https://no.wikipedia.org/w/api.php"),
        ("nn", "https://nn.wikipedia.org/w/api.php")
    ]
    for lang, wiki_api_url in wikis:
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
            response = safe_get(wiki_api_url, params=params, headers=HEADERS)
            pages = response.json()["query"]["pages"]
            page_id = list(pages.keys())[0]
            if page_id == "-1":
                continue
            bio = pages[page_id].get("extract", "No bio available.").strip()
            bio_sentences = bio.split('.')[:3]
            bio = '. '.join(bio_sentences) + '.' if bio_sentences else bio
            if "pageprops" not in pages[page_id]:
                continue
            wikidata_id = pages[page_id]["pageprops"].get("wikibase_item")
            if not wikidata_id:
                continue
            # Get birth/death from Wikidata
            sparql_query = f"""
            SELECT ?birth ?death WHERE {{
              wd:{wikidata_id} wdt:P569 ?birth .
              OPTIONAL {{ wd:{wikidata_id} wdt:P570 ?death }}
            }}
            """
            wikidata_url = "https://query.wikidata.org/sparql"
            params2 = {"query": sparql_query, "format": "json"}
            response2 = safe_get(wikidata_url, params=params2, headers=HEADERS)
            results = response2.json()["results"]["bindings"]
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
        except Exception as e:
            print(f"  [WARN] {lang}wiki lookup failed for {artist}: {e}")
    return None

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

def get_year_only(date_str):
    if not date_str:
        return None
    import re
    match = re.search(r'\b(17|18|19|20|21)\d{2}\b', date_str)
    return match.group(0) if match else None

def get_century_from_year(year_str):
    year = get_year_only(year_str)
    if not year:
        return None
    year = int(year)
    return f"{(year - 1) // 100 + 1}00s"

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

# Define artist tiers
POPULAR_PAINTERS = [
    "Edvard Munch", "Johan Christian Dahl", "Christian Krohg", "Theodor Kittelsen", "Harriet Backer", "Kitty Lange Kielland", "Peter Nicolai Arbo", "Hans Gude", "Peder Balke", "Frits Thaulow", "Nikolai Astrup", "Odd Nerdrum", "Harald Sohlberg", "Erik Werenskiold", "Adolph Tidemand"
]
SEMI_POPULAR_PAINTERS = [
    "Lars Hertervig", "Oda Krohg", "Eilif Peterssen", "Hans Dahl", "Per Krohg", "August Cappelen", "Asta Nørregaard", "Amaldus Nielsen", "Christian Skredsvig", "Gunnar Berg", "Halfdan Egedius", "Thorolf Holmboe", "Jakob Weidemann", "Peder Aadnes", "Martin Aagaard"
]
MID_PAINTERS = [
    "Rolf Aamot", "Johannes Flintoe", "Rolf Groven", "Konrad Knudsen", "Wilhelm Peters", "Halvard Storm", "Jacob Gløersen", "Gustav Wentzel", "Oscar Wergeland", "Carl Sundt-Hansen", "Adelsteen Normann", "Axel Revold", "Jean Heiberg", "Olav Christopher Jenssen", "Bjarne Melgaard", "Fredrik Værslev", "Charlotte Wankel", "Inger Sitter", "Cora Sandel", "Paul René Gauguin", "Peder Severin Krøyer", "Thomas Fearnley", "Knud Baade", "Joachim Frich", "Morten Müller", "Johan Fredrik Eckersberg", "Otto Sinding", "Nils Hansteen", "Eyolf Soot", "Ludvig Karsten", "Thorvald Erichsen"
]
BOTTOM_PAINTERS = [
    "Henrik Lund", "Henrik Sørensen", "Pola Gauguin", "Rolf Nesch", "Olaf Gulbransson", "Bjarne Ness", "Ludvig Eikaas", "Kåre Tveter", "Kjell Aukrust", "Kåre Espolin Johnson", "Frans Widerberg", "Håkon Bleken", "Knut Rose", "Knut Rumohr", "Kjartan Slettemark", "Vebjørn Sand", "Håkon Gullvåg", "Ørnulf Opdahl", "Kjell Pahr-Iversen", "Lisa Aisato", "Gerhard Munthe", "Kjell Nupen", "Pushwagner", "Bjørn Ransve", "Arne Ekeland", "Kai Fjell", "Reidar Aulie", "Arne Texnes Kavli", "Søren Onsager", "Helge Ulving", "Nils Gude", "Bernt Lund", "Nils Elias Kristi", "Oluf Wold-Torne", "Sigurd Dancke", "Alf Lundeby", "Thorleif Stadheim", "Ida Lorentzen", "Marianne Aulie"
]

# Helper to fetch paintings from Wikimedia Commons
API_ENDPOINT = "https://commons.wikimedia.org/w/api.php"
def extract_metadata(metadata, key):
    return metadata.get(key, {}).get("value", "").strip()

# Helper to recursively fetch all images from a category and its subcategories (with max depth)
def fetch_images_from_category(category, limit=100, max_depth=2):
    images = set()
    visited = set()
    def recurse(cat, depth):
        if cat in visited or depth > max_depth:
            return
        visited.add(cat)
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": f"Category:{cat}",
            "cmtype": "file|subcat",
            "cmlimit": 500
        }
        r = requests.get(API_ENDPOINT, params=params, headers=HEADERS)
        if r.status_code != 200:
            return
        data = r.json()
        for member in data.get("query", {}).get("categorymembers", []):
            if member["ns"] == 6:  # File
                images.add(member["title"])
            elif member["ns"] == 14:  # Subcategory
                subcat = member["title"].replace("Category:", "")
                recurse(subcat, depth + 1)
    recurse(category, 0)
    # Now get imageinfo for each file
    entries = []
    batch = list(images)
    for i in range(0, len(batch), 50):
        titles = "|".join(batch[i:i+50])
        params = {
            "action": "query",
            "format": "json",
            "titles": titles,
            "prop": "imageinfo",
            "iiprop": "url|user|size|extmetadata"
        }
        r = requests.get(API_ENDPOINT, params=params, headers=HEADERS)
        if r.status_code != 200:
            continue
        pages = r.json().get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            info = page.get("imageinfo", [{}])[0]
            metadata = info.get("extmetadata", {})
            url = info.get("url")
            raw_title = metadata.get("ObjectName", {}).get("value", page.get("title", ""))
            title = raw_title.replace("File:", "").replace("_", " ").strip()
            entry = {
                "title": title,
                "url": url,
                "year": metadata.get("DateTimeOriginal", {}).get("value", "") or metadata.get("DateCreated", {}).get("value", ""),
                "medium": metadata.get("Medium", {}).get("value", ""),
                "dimensions": metadata.get("Dimensions", {}).get("value", ""),
                "location": metadata.get("Credit", {}).get("value", ""),
                "license": metadata.get("LicenseShortName", {}).get("value", ""),
                "source": "Wikimedia Commons"
            }
            if url:
                entries.append(entry)
    return entries[:limit]

# Helper to fetch paintings from Wikidata if Commons is sparse
def fetch_paintings_from_wikidata(artist_name, limit=100):
    # Get Wikidata ID for artist
    search_url = "https://www.wikidata.org/w/api.php"
    params = {"action": "wbsearchentities", "search": artist_name, "language": "en", "format": "json", "type": "item"}
    r = requests.get(search_url, params=params, headers=HEADERS)
    r.raise_for_status()
    results = r.json().get("search", [])
    if not results:
        return []
    qid = results[0]["id"]
    # SPARQL for paintings by this artist with Commons images
    sparql = f'''
    SELECT ?painting ?paintingLabel ?image ?inception WHERE {{
      ?painting wdt:P31 wd:Q3305213; wdt:P170 wd:{qid}; wdt:P18 ?image.
      OPTIONAL {{ ?painting wdt:P571 ?inception. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }} LIMIT {limit}
    '''
    url = "https://query.wikidata.org/sparql"
    r2 = requests.get(url, params={"query": sparql, "format": "json"}, headers=HEADERS)
    r2.raise_for_status()
    entries = []
    for item in r2.json()["results"]["bindings"]:
        entries.append({
            "title": item.get("paintingLabel", {}).get("value", ""),
            "url": item.get("image", {}).get("value", ""),
            "year": item.get("inception", {}).get("value", ""),
            "medium": "",
            "dimensions": "",
            "location": "",
            "license": "",
            "source": "Wikidata"
        })
    return entries

# Main collection and merge logic
all_paintings = []
# Load artist bios for aliases
with open('data/artist_bios.json', 'r', encoding='utf-8') as f:
    artist_bios = json.load(f)
artist_alias_map = {b['name']: [b['name']] + b.get('aliases', []) for b in artist_bios}

# Load existing paintings for appending
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        try:
            existing_paintings = json.load(f)
            for p in existing_paintings:
                key = (p["artist"], p["title"], p["url"])
                existing_keys.add(key)
                all_paintings.append(p)
        except Exception as e:
            print(f"Warning: Could not load existing paintings: {e}")

# Build a set of unique keys for fast lookup
# existing_keys = set((p['artist'], p['title'], p['url']) for p in existing_paintings) # This line is now redundant as keys are added directly

# Fetch up to 100 paintings per artist
for artist in artists:
    # Tiered limits
    if artist in POPULAR_PAINTERS:
        limit = 100
        tier = "Popular"
    elif artist in SEMI_POPULAR_PAINTERS:
        limit = 50
        tier = "Semi-Popular"
    elif artist in MID_PAINTERS:
        limit = 30
        tier = "Mid"
    else:
        limit = 15
        tier = "Bottom"
    print(f"Processing {artist} [{tier}, limit={limit}]...")
    artist_meta = fetch_artist_metadata(artist)
    if not artist_meta:
        print(f"  Skipping {artist}: No metadata found.")
        continue
    # Fetch extra metadata
    gender, country, movement = fetch_artist_extra_metadata(artist_meta["wikidata_id"])
    # Use aliases for search
    aliases = artist_alias_map.get(artist, [artist])
    found_paintings = []
    for alias in aliases:
        print(f"  Searching for paintings by alias: {alias}")
        commons_patterns = [
            f"Paintings by {alias}",
            f"Art by {alias}",
            f"Works by {alias}",
            f"{alias}"
        ]
        alias_paintings = []
        for cat_name in commons_patterns:
            print(f"    Trying Commons category: {cat_name}")
            paintings = fetch_images_from_category(cat_name, limit=limit, max_depth=2)
            alias_paintings += paintings
        # Always supplement with Wikidata for this alias
        print(f"    Supplementing with Wikidata for {alias}...")
        alias_paintings += fetch_paintings_from_wikidata(alias, limit=limit-len(alias_paintings))
        for p in alias_paintings:
            p['artist'] = artist  # Always use canonical name
        found_paintings += alias_paintings
    # Deduplicate by url within this artist
    seen_urls = set()
    unique_paintings = []
    for p in found_paintings:
        if p["url"] and p["url"] not in seen_urls:
            unique_paintings.append(p)
            seen_urls.add(p["url"])
    paintings = unique_paintings
    print(f"  Found {len(paintings)} paintings for {artist}.")
    if len(paintings) < limit:
        print(f"  WARNING: Only {len(paintings)} paintings found for {artist}!")
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
        # Compute century from actual painting year
        painting["century"] = get_century_from_year(painting.get("year", ""))
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
            categories.append(painting["century"])
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

# After main loop, fetch 5 more paintings for every painter (not just popular ones)
for artist in artists:
    aliases = artist_alias_map.get(artist, [artist])
    for alias in aliases:
        print(f"[EXTRA] Fetching 5 more paintings for {alias}")
        commons_patterns = [
            f"Paintings by {alias}",
            f"Art by {alias}",
            f"Works by {alias}",
            f"{alias}"
        ]
        extra_paintings = []
        for cat_name in commons_patterns:
            print(f"    Trying Commons category: {cat_name}")
            paintings = fetch_images_from_category(cat_name, limit=5, max_depth=2)
            extra_paintings += paintings
        print(f"    Supplementing with Wikidata for {alias}...")
        extra_paintings += fetch_paintings_from_wikidata(alias, limit=5-len(extra_paintings))
        for p in extra_paintings:
            p['artist'] = artist
        # Deduplicate and append
        seen_urls = set()
        unique_paintings = []
        for p in extra_paintings:
            if p["url"] and p["url"] not in seen_urls:
                unique_paintings.append(p)
                seen_urls.add(p["url"])
        for painting in unique_paintings:
            key = (painting['artist'], painting['title'], painting['url'])
            if key not in existing_keys:
                all_paintings.append(painting)
                existing_keys.add(key)

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

# Save to a new file for safety
output_appended = OUTPUT_FILE.replace('.json', '_appended.json')
with open(output_appended, "w", encoding="utf-8") as f:
    json.dump(final_paintings, f, indent=2, ensure_ascii=False)
print(f"✅ Appended and saved {len(final_paintings)} paintings to {output_appended}") 