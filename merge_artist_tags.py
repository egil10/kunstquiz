import json
import os

# Load paintings
with open('data/paintings.json', 'r', encoding='utf-8') as f:
    paintings = json.load(f)

# Load artist tags
try:
    with open('data/artist_tags.json', 'r', encoding='utf-8') as f:
        artist_tags = json.load(f)
except FileNotFoundError:
    print('ERROR: data/artist_tags.json not found. Please run collect_artist_tags.py first.')
    exit(1)

# Helper: add tags from artist to painting if missing
for painting in paintings:
    artist = painting.get('artist')
    tags = artist_tags.get(artist, {})
    # Merge metadata fields if missing or empty
    for field in ['movement', 'genre', 'country_of_origin', 'artist_birth', 'artist_death', 'artist_gender', 'artist_bio', 'artist_summary', 'birthplace']:
        if not painting.get(field) and tags.get(field):
            painting[field] = tags[field]
    # Add notable works if not present
    if 'notable_works' not in painting and 'notable_works' in tags:
        painting['notable_works'] = tags['notable_works']
    # Expand categories using artist tags
    categories = set(painting.get('categories', []))
    # Add movement, genre, country, etc. as categories if not already present
    for key in ['movement', 'genre', 'country_of_origin', 'artist_gender', 'birthplace']:
        val = painting.get(key) or tags.get(key)
        if val and isinstance(val, str):
            categories.add(val)
    # Add a category for each notable work title (optional, for filtering by famous works)
    if 'notable_works' in tags:
        for work in tags['notable_works']:
            if work.get('title'):
                categories.add(work['title'])
    # Remove empty/None categories
    categories = {c for c in categories if c and c != 'Unknown'}
    painting['categories'] = sorted(categories)

# Output merged file
with open('data/paintings_merged.json', 'w', encoding='utf-8') as f:
    json.dump(paintings, f, indent=2, ensure_ascii=False)

print('✅ Merged artist tags into data/paintings_merged.json') 