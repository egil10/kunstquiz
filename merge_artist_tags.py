import json
import os

# Load paintings (now from paintings_appended.json)
with open('data/paintings_appended.json', 'r', encoding='utf-8') as f:
    paintings = json.load(f)

# Load artist tags
try:
    with open('data/artist_tags.json', 'r', encoding='utf-8') as f:
        artist_tags = json.load(f)
except FileNotFoundError:
    print('ERROR: data/artist_tags.json not found. Please run collect_artist_tags.py first.')
    exit(1)

# Load artist bios
try:
    with open('data/artist_bios.json', 'r', encoding='utf-8') as f:
        artist_bios_list = json.load(f)
        artist_bios = {b['name']: b for b in artist_bios_list}
except FileNotFoundError:
    print('ERROR: data/artist_bios.json not found. Please provide artist bios.')
    artist_bios = {}

# Helper: add tags and bios from artist to painting if missing or to enrich
for painting in paintings:
    artist = painting.get('artist')
    
    # Fix museum-specific artist names (e.g., "Nikolai Astrup in Sogn og Fjordane Kunstmuseum" -> "Nikolai Astrup")
    if artist and ' in ' in artist:
        original_artist = artist
        artist = artist.split(' in ')[0]
        painting['artist'] = artist
        print(f"Fixed artist name: '{original_artist}' -> '{artist}'")
    
    tags = artist_tags.get(artist, {})
    bio = artist_bios.get(artist, {})
    # Merge metadata fields, prefer bios > tags > painting
    for field, bio_field in [
        ('artist_bio', 'bio'),
        ('artist_birth', 'birth_year'),
        ('artist_death', 'death_year'),
        ('artist_birthplace', 'birthplace'),
        ('artist_deathplace', 'deathplace'),
        ('artist_movement', 'movement'),
        ('artist_genre', 'genre'),
        ('artist_awards', 'awards'),
        ('artist_self_portrait_url', 'self_portrait_url'),
        ('artist_aliases', 'aliases')
    ]:
        val = bio.get(bio_field)
        if val is not None:
            # Ensure movement/genre/awards/aliases are always arrays
            if field in ['artist_movement', 'artist_genre', 'artist_awards', 'artist_aliases']:
                if isinstance(val, str):
                    painting[field] = [val]
                elif isinstance(val, list):
                    painting[field] = val
                else:
                    painting[field] = []
            else:
                painting[field] = val
        elif tags.get(bio_field):
            painting[field] = tags[bio_field]
    # Merge tags fields if not present
    for field in ['movement', 'genre', 'country_of_origin', 'artist_gender', 'artist_summary', 'birthplace']:
        if not painting.get(field) and tags.get(field):
            val = tags[field]
            # Ensure movement/genre are always arrays
            if field in ['movement', 'genre']:
                if isinstance(val, str):
                    painting[field] = [val]
                elif isinstance(val, list):
                    painting[field] = val
                else:
                    painting[field] = []
            else:
                painting[field] = val
    # Add notable works if not present
    if 'notable_works' not in painting and 'notable_works' in tags:
        painting['notable_works'] = tags['notable_works']
    # Expand categories using artist tags
    categories = set(painting.get('categories', []))
    for key in ['movement', 'genre', 'country_of_origin', 'artist_gender', 'birthplace']:
        val = painting.get(key) or tags.get(key)
        if val and isinstance(val, str):
            categories.add(val)
    if 'notable_works' in tags:
        for work in tags['notable_works']:
            if work.get('title'):
                categories.add(work['title'])
    categories = {c for c in categories if c and c != 'Unknown'}
    gender_val = (painting.get('artist_gender') or painting.get('gender') or tags.get('artist_gender') or tags.get('gender'))
    if gender_val and str(gender_val).lower() == 'female':
        categories.add('Women painters')
    for key in ['genre', 'movement']:
        val = (painting.get(key) or tags.get(key) or '')
        if isinstance(val, str) and 'portrait' in val.lower():
            categories.add('Portraits')
    for key in ['genre', 'movement']:
        val = (painting.get(key) or tags.get(key) or '')
        if isinstance(val, str) and 'landscape' in val.lower():
            categories.add('Landscapes')
    painting['categories'] = sorted(categories)

# Output merged file
with open('data/paintings_merged.json', 'w', encoding='utf-8') as f:
    json.dump(paintings, f, indent=2, ensure_ascii=False)

print('✅ Merged artist tags and bios into data/paintings_merged.json') 