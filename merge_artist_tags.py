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
    
    # Fix various artist name variations
    if artist:
        original_artist = artist
        
        # Fix museum-specific artist names (e.g., "Nikolai Astrup in Sogn og Fjordane Kunstmuseum" -> "Nikolai Astrup")
        if ' in ' in artist:
            artist = artist.split(' in ')[0]
        
        # Fix category prefixes (e.g., "Category:Drawings by Hans Gude" -> "Hans Gude")
        elif artist.startswith('Category:'):
            artist = artist.replace('Category:', '').strip()
            # Extract artist name after "by" or "from"
            if ' by ' in artist:
                artist = artist.split(' by ')[-1]
            elif ' from ' in artist:
                artist = artist.split(' from ')[0]
        
        # Fix "Artworks by" prefixes (e.g., "Artworks by Edvard Munch" -> "Edvard Munch")
        elif artist.startswith('Artworks by '):
            artist = artist.replace('Artworks by ', '')
        
        # Fix life and works suffixes (e.g., "Johan Christian Dahl, 1788-1857: life and works" -> "Johan Christian Dahl")
        elif ', ' in artist and ': life and works' in artist:
            artist = artist.split(', ')[0]
        
        # Fix "Dahl and Friedrich" type names (e.g., "Dahl and Friedrich. Romantic Landscapes" -> "Johan Christian Dahl")
        elif 'Dahl and Friedrich' in artist:
            artist = 'Johan Christian Dahl'
        
        # Fix "Christian Krohg. Pictures that captivate" -> "Christian Krohg"
        elif 'Christian Krohg. Pictures that captivate' in artist:
            artist = 'Christian Krohg'
        
        # Fix "Hans Gude from Af Hans Gudes liv og værker" -> "Hans Gude"
        elif 'Hans Gude from Af Hans Gudes liv og værker' in artist or 'Hans Gude from Af Hans Gudes liv og v%C3%A6rker' in artist:
            artist = 'Hans Gude'
        
        # Fix URL-encoded characters in artist names
        elif '%' in artist:
            import urllib.parse
            artist = urllib.parse.unquote(artist)
            # Clean up any remaining URL artifacts
            if ' from ' in artist and 'Hans Gude' in artist:
                artist = 'Hans Gude'
        
        # Update the painting if the artist name changed
        if artist != original_artist:
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