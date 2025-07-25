import json

# Load the paintings data
with open('data/paintings_appended.json', 'r', encoding='utf-8') as f:
    paintings = json.load(f)

print(f'Total paintings: {len(paintings)}')

# Check for duplicates based on (artist, title, url)
unique_combinations = set()
duplicates = 0
duplicate_details = []

for i, painting in enumerate(paintings):
    key = (painting.get('artist', ''), painting.get('title', ''), painting.get('url', ''))
    if key in unique_combinations:
        duplicates += 1
        duplicate_details.append({
            'index': i,
            'artist': painting.get('artist', ''),
            'title': painting.get('title', ''),
            'url': painting.get('url', '')
        })
    unique_combinations.add(key)

print(f'Unique paintings: {len(unique_combinations)}')
print(f'Duplicates found: {duplicates}')

# Check for duplicates based on just URL (most reliable)
url_counts = {}
for painting in paintings:
    url = painting.get('url', '')
    if url:
        url_counts[url] = url_counts.get(url, 0) + 1

url_duplicates = {url: count for url, count in url_counts.items() if count > 1}
print(f'URL duplicates: {len(url_duplicates)}')

if url_duplicates:
    print('\nSample URL duplicates:')
    for url, count in list(url_duplicates.items())[:5]:
        print(f'  {url}: {count} times')

# Check for duplicates based on just title (might be same painting, different URLs)
title_counts = {}
for painting in paintings:
    title = painting.get('title', '')
    if title:
        title_counts[title] = title_counts.get(title, 0) + 1

title_duplicates = {title: count for title, count in title_counts.items() if count > 1}
print(f'\nTitle duplicates: {len(title_duplicates)}')

if title_duplicates:
    print('\nSample title duplicates:')
    for title, count in list(title_duplicates.items())[:5]:
        print(f'  "{title}": {count} times')

# Show some sample duplicates
if duplicate_details:
    print('\nSample duplicate entries:')
    for dup in duplicate_details[:3]:
        print(f'  Index {dup["index"]}: {dup["artist"]} - "{dup["title"]}"') 