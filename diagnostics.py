import json
from collections import Counter, defaultdict
import os
import re

PAINTINGS_FILE = 'data/paintings_appended.json'
BIOS_FILE = 'data/artist_bios.json'
REPORT_FILE = 'diagnostics.md'

CATEGORY_DEFS = [
    { 'value': 'all', 'label': 'Full Collection' },
    { 'value': 'popular', 'label': 'Popular Painters' },
    { 'value': 'landscape', 'label': 'Landscape Painting' },
    { 'value': 'romanticism', 'label': 'Romanticism' },
    { 'value': 'impressionism', 'label': 'Impressionism' },
    { 'value': 'expressionism', 'label': 'Expressionism' },
    { 'value': 'portraits', 'label': 'Portraits' },
    { 'value': 'historical', 'label': 'Historical/Nationalism' },
    { 'value': '19thcentury', 'label': '19th Century' },
    { 'value': '20thcentury', 'label': '20th Century' }
]

def arr(val):
    if isinstance(val, list):
        return val
    elif isinstance(val, str) and val:
        return [val]
    return []

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_report(lines):
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'\nMarkdown report written to {REPORT_FILE}')

def update_readme_with_stats(stats_md):
    readme_path = 'README.md'
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme = f.read()
    except FileNotFoundError:
        readme = ''
    start_marker = '<!-- STATS_START -->'
    end_marker = '<!-- STATS_END -->'
    stats_block = f'{start_marker}\n{stats_md}\n{end_marker}'
    if start_marker in readme and end_marker in readme:
        readme = re.sub(f'{start_marker}.*?{end_marker}', stats_block, readme, flags=re.DOTALL)
    else:
        readme += f'\n\n{stats_block}\n'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)

def get_file_stats(filepath):
    """Get detailed file statistics"""
    if not os.path.exists(filepath):
        return None
    
    stats = os.stat(filepath)
    size_mb = stats.st_size / (1024 * 1024)
    
    # Count lines
    with open(filepath, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    
    return {
        'size_mb': round(size_mb, 2),
        'size_bytes': stats.st_size,
        'line_count': line_count,
        'modified': stats.st_mtime
    }

def check_health_status(value, thresholds):
    """Check if a value is within healthy ranges"""
    if value < thresholds['warning']:
        return '🟢 Good'
    elif value < thresholds['critical']:
        return '🟡 Warning'
    else:
        return '🔴 Critical'

def main():
    if not os.path.exists(PAINTINGS_FILE):
        print(f'ERROR: {PAINTINGS_FILE} not found.')
        return
    if not os.path.exists(BIOS_FILE):
        print(f'ERROR: {BIOS_FILE} not found.')
        return
    
    paintings = load_json(PAINTINGS_FILE)
    bios = load_json(BIOS_FILE)
    bios_by_name = {b['name']: b for b in bios}

    # Get file statistics
    paintings_stats = get_file_stats(PAINTINGS_FILE)
    bios_stats = get_file_stats(BIOS_FILE)
    
    # Health thresholds
    painting_thresholds = {
        'count': {'warning': 8000, 'critical': 15000},
        'size_mb': {'warning': 25, 'critical': 50},
        'line_count': {'warning': 100000, 'critical': 200000}
    }

    lines = []
    lines.append(f'# Art Data Diagnostics\n')
    
    # File Health Section
    lines.append('## 📊 File Health & Performance')
    if paintings_stats:
        lines.append(f'- **Paintings file size:** {paintings_stats["size_mb"]} MB ({paintings_stats["line_count"]:,} lines)')
        lines.append(f'- **File size status:** {check_health_status(paintings_stats["size_mb"], painting_thresholds["size_mb"])}')
        lines.append(f'- **Line count status:** {check_health_status(paintings_stats["line_count"], painting_thresholds["line_count"])}')
    
    if bios_stats:
        lines.append(f'- **Bios file size:** {bios_stats["size_mb"]} MB ({bios_stats["line_count"]:,} lines)')
    
    lines.append(f'- **Total paintings:** {len(paintings):,}')
    lines.append(f'- **Collection size status:** {check_health_status(len(paintings), painting_thresholds["count"])}')
    
    all_artists = set(p['artist'] for p in paintings if p.get('artist'))
    lines.append(f'- **Total unique artists in paintings:** {len(all_artists)}')
    lines.append(f'- **Total artists in bios:** {len(bios_by_name)}')
    
    # Performance recommendations
    lines.append('\n### 💡 Performance Recommendations')
    if paintings_stats and paintings_stats["size_mb"] > 25:
        lines.append('- ⚠️ **Large file detected:** Consider splitting data or optimizing storage')
    if len(paintings) > 8000:
        lines.append('- ⚠️ **Large collection:** Monitor quiz loading performance')
    if len(paintings) > 15000:
        lines.append('- 🔴 **Very large collection:** Consider data optimization or pagination')
    
    if len(paintings) < 1000:
        lines.append('- 💡 **Small collection:** Room for growth - keep collecting!')
    elif len(paintings) < 5000:
        lines.append('- 💡 **Good collection size:** Continue collecting for variety')
    else:
        lines.append('- 💡 **Large collection:** Focus on quality over quantity')

    # 1. Category counts (quiz categories)
    lines.append('\n## Quiz Categories')
    for cat in CATEGORY_DEFS:
        if cat['value'] == 'all':
            filtered = [p for p in paintings if p.get('artist') and p.get('url')]
        elif cat['value'] == 'popular':
            artist_counts = Counter(p['artist'] for p in paintings if p.get('artist'))
            top_artists = set(a for a, _ in artist_counts.most_common(10))
            filtered = [p for p in paintings if p.get('artist') in top_artists]
        elif cat['value'] == 'landscape':
            filtered = [p for p in paintings if any('landscape' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'romanticism':
            filtered = [p for p in paintings if any('romanticism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'impressionism':
            filtered = [p for p in paintings if any('impressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'expressionism':
            filtered = [p for p in paintings if any('expressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'portraits':
            filtered = [p for p in paintings if any('portrait' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'historical':
            filtered = [p for p in paintings if any(any(x in (g or '').lower() for x in ['historical','nationalism','mythology']) for g in arr(p.get('artist_genre')) + arr(p.get('genre')) + arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == '19thcentury':
            filtered = [p for p in paintings if bios_by_name.get(p.get('artist')) and bios_by_name[p['artist']].get('birth_year') and 1800 <= int(bios_by_name[p['artist']]['birth_year']) < 1900]
        elif cat['value'] == '20thcentury':
            filtered = [p for p in paintings if bios_by_name.get(p.get('artist')) and bios_by_name[p['artist']].get('birth_year') and 1900 <= int(bios_by_name[p['artist']]['birth_year']) < 2000]
        else:
            filtered = []
        unique_painters = set(p['artist'] for p in filtered if p.get('artist'))
        lines.append(f'- **{cat["label"]}:** {len(filtered)} paintings, {len(unique_painters)} painters')

    # 2. All unique genres, movements, awards
    genre_counter = Counter()
    movement_counter = Counter()
    award_counter = Counter()
    for b in bios:
        for g in arr(b.get('genre')):
            genre_counter[g] += 1
        for m in arr(b.get('movement')):
            movement_counter[m] += 1
        for a in arr(b.get('awards')):
            award_counter[a] += 1
    lines.append('\n## All Genres (from bios)')
    for g, c in genre_counter.most_common():
        lines.append(f'- {g}: {c}')
    lines.append('\n## All Movements (from bios)')
    for m, c in movement_counter.most_common():
        lines.append(f'- {m}: {c}')
    lines.append('\n## All Awards (from bios)')
    for a, c in award_counter.most_common():
        lines.append(f'- {a}: {c}')

    # 3. Painters with 0 paintings
    painters_with_0 = [b['name'] for b in bios if b['name'] not in all_artists]
    lines.append(f'\n## Painters in bios with 0 paintings: {len(painters_with_0)}')
    if painters_with_0:
        lines.append(', '.join(painters_with_0))

    # 4. Field type checks
    lines.append('\n## Field Type Checks')
    bad_movement = [p for p in paintings if not isinstance(p.get('movement', []), list)]
    bad_genre = [p for p in paintings if not isinstance(p.get('genre', []), list)]
    lines.append(f'- Movement is array for all paintings: {len(bad_movement) == 0}')
    lines.append(f'- Genre is array for all paintings: {len(bad_genre) == 0}')

    # 5. Duplicate Analysis
    lines.append('\n## 🔍 Duplicate Analysis')
    
    # Check exact duplicates (artist, title, url)
    seen = set()
    exact_dups = []
    for p in paintings:
        key = (p.get('artist'), p.get('title'), p.get('url'))
        if key in seen:
            exact_dups.append(key)
        else:
            seen.add(key)
    
    lines.append(f'- **Exact duplicates:** {len(exact_dups)}')
    if exact_dups:
        lines.append(f'- **Duplicate status:** 🔴 Critical - {len(exact_dups)} duplicates found')
        lines.append('- **Sample duplicates:**')
        for dup in exact_dups[:3]:
            lines.append(f'  - {dup[0]}: "{dup[1]}"')
    else:
        lines.append(f'- **Duplicate status:** 🟢 Good - No exact duplicates')
    
    # Check URL duplicates (same image, different contexts)
    url_counts = {}
    for p in paintings:
        url = p.get('url', '')
        if url:
            url_counts[url] = url_counts.get(url, 0) + 1
    
    url_duplicates = {url: count for url, count in url_counts.items() if count > 1}
    lines.append(f'- **URL duplicates:** {len(url_duplicates)} (same image in multiple categories)')
    
    if url_duplicates:
        lines.append(f'- **URL duplicate status:** 🟡 Warning - {len(url_duplicates)} images appear multiple times')
        lines.append('- **Sample URL duplicates:**')
        for url, count in list(url_duplicates.items())[:3]:
            lines.append(f'  - {url}: {count} times')
    else:
        lines.append(f'- **URL duplicate status:** 🟢 Good - No URL duplicates')
    
    # Check title duplicates (same painting, different URLs)
    title_counts = {}
    for p in paintings:
        title = p.get('title', '')
        if title:
            title_counts[title] = title_counts.get(title, 0) + 1
    
    title_duplicates = {title: count for title, count in title_counts.items() if count > 1}
    lines.append(f'- **Title duplicates:** {len(title_duplicates)} (same painting, different sources)')
    
    if title_duplicates:
        lines.append(f'- **Title duplicate status:** 🟡 Warning - {len(title_duplicates)} titles appear multiple times')
        lines.append('- **Sample title duplicates:**')
        for title, count in list(title_duplicates.items())[:3]:
            lines.append(f'  - "{title}": {count} times')
    else:
        lines.append(f'- **Title duplicate status:** 🟢 Good - No title duplicates')

    # 6. Largest/smallest categories
    lines.append('\n## Largest/Smallest Categories (by genre)')
    genre_painting_counts = Counter()
    for p in paintings:
        for g in arr(p.get('artist_genre')) + arr(p.get('genre')):
            genre_painting_counts[g] += 1
    if genre_painting_counts:
        lines.append('Largest genres:')
        for g, c in genre_painting_counts.most_common(5):
            lines.append(f'- {g}: {c}')
        lines.append('Smallest genres:')
        for g, c in genre_painting_counts.most_common()[-5:]:
            lines.append(f'- {g}: {c}')

    # 7. List all painters and their number of paintings
    lines.append('\n## All Painters and Number of Paintings')
    painter_counts = Counter(p['artist'] for p in paintings if p.get('artist'))
    for artist, count in painter_counts.most_common():
        lines.append(f'- {artist}: {count}')

    lines.append('\nDiagnostics complete.')

    # Write diagnostics report
    for line in lines:
        print(line)
    write_report(lines)

    # Prepare and update README.md with summary stats
    summary_lines = []
    summary_lines.append('**Latest Art Quiz Stats**')
    summary_lines.append(f'- Total paintings: {len(paintings)}')
    summary_lines.append(f'- Total unique artists in paintings: {len(all_artists)}')
    summary_lines.append(f'- Total artists in bios: {len(bios_by_name)}')
    summary_lines.append('- Categories:')
    for cat in CATEGORY_DEFS:
        if cat['value'] == 'all':
            filtered = [p for p in paintings if p.get('artist') and p.get('url')]
        elif cat['value'] == 'popular':
            artist_counts = Counter(p['artist'] for p in paintings if p.get('artist'))
            top_artists = set(a for a, _ in artist_counts.most_common(10))
            filtered = [p for p in paintings if p.get('artist') in top_artists]
        elif cat['value'] == 'landscape':
            filtered = [p for p in paintings if any('landscape' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'portraits':
            filtered = [p for p in paintings if any('portrait' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'romanticism':
            filtered = [p for p in paintings if any('romanticism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'expressionism':
            filtered = [p for p in paintings if any('expressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'impressionism':
            filtered = [p for p in paintings if any('impressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'historical_nationalism':
            filtered = [p for p in paintings if any(any(x in (g or '').lower() for x in ['historical','nationalism','mythology']) for g in arr(p.get('artist_genre')) + arr(p.get('genre')) + arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == '1800s':
            filtered = [p for p in paintings if bios_by_name.get(p.get('artist')) and bios_by_name[p['artist']].get('birth_year') and 1800 <= int(bios_by_name[p['artist']]['birth_year']) < 1900]
        elif cat['value'] == 'national_museum':
            filtered = [p for p in paintings if p.get('location') and 'national museum of norway' in p['location'].lower()]
        elif cat['value'] == 'women_painters':
            # Assuming 'womenPainters' is defined elsewhere or needs to be added.
            # For now, commenting out as it's not defined in the original file.
            # filtered = [p for p in paintings if p.get('artist') in womenPainters]
            pass # Placeholder for women_painters category
        else:
            filtered = []
        unique_painters = set(p['artist'] for p in filtered if p.get('artist'))
        summary_lines.append(f'  - {cat["label"]}: {len(filtered)} paintings, {len(unique_painters)} painters')
    stats_md = '\n'.join(summary_lines)
    update_readme_with_stats(stats_md)

if __name__ == '__main__':
    main() 