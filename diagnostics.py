import json
from collections import Counter, defaultdict
import os
import re

PAINTINGS_FILE = 'data/paintings_appended.json'
PAINTINGS_MERGED_FILE = 'data/paintings_merged.json'
BIOS_FILE = 'data/artist_bios.json'
ARTIST_TAGS_FILE = 'data/artist_tags.json'
ARTIST_TAGS_APPENDED_FILE = 'data/artist_tags_appended.json'
REPORT_FILE = 'diagnostics.md'

CATEGORY_DEFS = [
    { 'value': 'all', 'label': 'Full Collection' },
    { 'value': 'popular', 'label': 'Popular Painters' },
    { 'value': 'landscape', 'label': 'Landscape Painting' },
    { 'value': 'portraits', 'label': 'Portraits' },
    { 'value': 'marine', 'label': 'Marine Painting' },
    { 'value': 'historical', 'label': 'Historical Painting' },
    { 'value': 'norwegian_romantic', 'label': 'Norwegian Romantic Nationalism' },
    { 'value': 'impressionism', 'label': 'Impressionism' },
    { 'value': 'expressionism', 'label': 'Expressionism' },
    { 'value': '19thcentury', 'label': '19th Century' },
    { 'value': '20thcentury', 'label': '20th Century' },
    { 'value': 'genre_painting', 'label': 'Genre Painting' },
    { 'value': 'religious', 'label': 'Religious Painting' }
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
    # Check for required files
    required_files = [PAINTINGS_FILE, BIOS_FILE]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f'ERROR: Missing required files: {missing_files}')
        return
    
    # Load data
    paintings = load_json(PAINTINGS_FILE)
    bios = load_json(BIOS_FILE)
    bios_by_name = {b['name']: b for b in bios}
    
    # Try to load optional files
    paintings_merged = None
    artist_tags = None
    artist_tags_appended = None
    
    if os.path.exists(PAINTINGS_MERGED_FILE):
        paintings_merged = load_json(PAINTINGS_MERGED_FILE)
    if os.path.exists(ARTIST_TAGS_FILE):
        artist_tags = load_json(ARTIST_TAGS_FILE)
    if os.path.exists(ARTIST_TAGS_APPENDED_FILE):
        artist_tags_appended = load_json(ARTIST_TAGS_APPENDED_FILE)

    # Get file statistics for all JSON files
    all_files = {
        'Paintings (Appended)': PAINTINGS_FILE,
        'Paintings (Merged)': PAINTINGS_MERGED_FILE,
        'Artist Bios': BIOS_FILE,
        'Artist Tags': ARTIST_TAGS_FILE,
        'Artist Tags (Appended)': ARTIST_TAGS_APPENDED_FILE
    }
    
    file_stats = {}
    for name, filepath in all_files.items():
        if os.path.exists(filepath):
            file_stats[name] = get_file_stats(filepath)
    
    # Health thresholds
    painting_thresholds = {
        'count': {'warning': 8000, 'critical': 15000},
        'size_mb': {'warning': 25, 'critical': 50},
        'line_count': {'warning': 100000, 'critical': 200000}
    }
    
    artist_thresholds = {
        'count': {'warning': 500, 'critical': 1000},
        'size_mb': {'warning': 1, 'critical': 5},
        'line_count': {'warning': 5000, 'critical': 10000}
    }

    lines = []
    lines.append(f'# Art Data Diagnostics\n')
    
    # File Health Section
    lines.append('## 📊 File Health & Performance')
    
    # Comprehensive file statistics
    lines.append('### 📁 All JSON Files Status')
    for name, stats in file_stats.items():
        if stats:
            lines.append(f'- **{name}:** {stats["size_mb"]} MB ({stats["line_count"]:,} lines)')
    
    # Paintings collection health
    paintings_stats = file_stats.get('Paintings (Appended)')
    if paintings_stats:
        lines.append(f'\n### 🎨 Paintings Collection Health')
        lines.append(f'- **File size:** {paintings_stats["size_mb"]} MB ({paintings_stats["line_count"]:,} lines)')
        lines.append(f'- **File size status:** {check_health_status(paintings_stats["size_mb"], painting_thresholds["size_mb"])}')
        lines.append(f'- **Line count status:** {check_health_status(paintings_stats["line_count"], painting_thresholds["line_count"])}')
        lines.append(f'- **Total paintings:** {len(paintings):,}')
        lines.append(f'- **Collection size status:** {check_health_status(len(paintings), painting_thresholds["count"])}')
    
    # Artist data health
    bios_stats = file_stats.get('Artist Bios')
    if bios_stats:
        lines.append(f'\n### 👨‍🎨 Artist Data Health')
        lines.append(f'- **Bios file:** {bios_stats["size_mb"]} MB ({bios_stats["line_count"]:,} lines)')
        lines.append(f'- **Total artists in bios:** {len(bios_by_name)}')
        lines.append(f'- **Bios file status:** {check_health_status(bios_stats["size_mb"], artist_thresholds["size_mb"])}')
    
    # Artist tags health
    tags_stats = file_stats.get('Artist Tags')
    if tags_stats:
        lines.append(f'- **Tags file:** {tags_stats["size_mb"]} MB ({tags_stats["line_count"]:,} lines)')
        lines.append(f'- **Tags file status:** {check_health_status(tags_stats["size_mb"], artist_thresholds["size_mb"])}')
    
    tags_appended_stats = file_stats.get('Artist Tags (Appended)')
    if tags_appended_stats:
        lines.append(f'- **Tags (Appended) file:** {tags_appended_stats["size_mb"]} MB ({tags_appended_stats["line_count"]:,} lines)')
        lines.append(f'- **Tags (Appended) status:** {check_health_status(tags_appended_stats["size_mb"], artist_thresholds["size_mb"])}')
    
    # Merged paintings health
    if paintings_merged:
        merged_stats = file_stats.get('Paintings (Merged)')
        if merged_stats:
            lines.append(f'\n### 🔗 Merged Data Health')
            lines.append(f'- **Merged paintings:** {len(paintings_merged):,}')
            lines.append(f'- **Merged file size:** {merged_stats["size_mb"]} MB ({merged_stats["line_count"]:,} lines)')
            lines.append(f'- **Merged file status:** {check_health_status(merged_stats["size_mb"], painting_thresholds["size_mb"])}')
    
    all_artists = set(p['artist'] for p in paintings if p.get('artist'))
    lines.append(f'- **Total unique artists in paintings:** {len(all_artists)}')
    
    # Data consistency checks
    lines.append(f'\n### 🔍 Data Consistency Checks')
    
    # Check if all artists in paintings have bios
    artists_without_bios = all_artists - set(bios_by_name.keys())
    artists_without_bios_count = len(artists_without_bios)
    lines.append(f'- **Artists without bios:** {artists_without_bios_count}')
    if artists_without_bios_count > 0:
        lines.append(f'- **Missing bios status:** 🟡 Warning - {artists_without_bios_count} artists need bios')
        if artists_without_bios_count <= 10:
            lines.append(f'- **Missing artists:** {", ".join(sorted(artists_without_bios))}')
    else:
        lines.append(f'- **Missing bios status:** 🟢 Good - All artists have bios')
    
    # Check if all bios have corresponding paintings
    bios_without_paintings = set(bios_by_name.keys()) - all_artists
    bios_without_paintings_count = len(bios_without_paintings)
    lines.append(f'- **Bios without paintings:** {bios_without_paintings_count}')
    if bios_without_paintings_count > 0:
        lines.append(f'- **Orphaned bios status:** 🟡 Warning - {bios_without_paintings_count} bios without paintings')
    else:
        lines.append(f'- **Orphaned bios status:** 🟢 Good - All bios have paintings')
    
    # Check merged vs appended paintings
    if paintings_merged:
        merged_count = len(paintings_merged)
        appended_count = len(paintings)
        lines.append(f'- **Merged vs Appended:** {merged_count:,} merged / {appended_count:,} appended')
        if merged_count != appended_count:
            lines.append(f'- **Merge consistency:** 🟡 Warning - Counts don\'t match')
        else:
            lines.append(f'- **Merge consistency:** 🟢 Good - Counts match')
    
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
        elif cat['value'] == 'portraits':
            filtered = [p for p in paintings if any('portrait' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'marine':
            filtered = [p for p in paintings if any('marine' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'historical':
            filtered = [p for p in paintings if any(any(x in (g or '').lower() for x in ['historical','history']) for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'norwegian_romantic':
            filtered = [p for p in paintings if any(any(x in (m or '').lower() for x in ['nasjonalromantikk','norwegian romantic nationalism','romantic nationalism']) for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'impressionism':
            filtered = [p for p in paintings if any('impressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == 'expressionism':
            filtered = [p for p in paintings if any('expressionism' in (m or '').lower() for m in arr(p.get('artist_movement')) + arr(p.get('movement')))]
        elif cat['value'] == '19thcentury':
            filtered = [p for p in paintings if bios_by_name.get(p.get('artist')) and bios_by_name[p['artist']].get('birth_year') and 1800 <= int(bios_by_name[p['artist']]['birth_year']) < 1900]
        elif cat['value'] == '20thcentury':
            filtered = [p for p in paintings if bios_by_name.get(p.get('artist')) and bios_by_name[p['artist']].get('birth_year') and 1900 <= int(bios_by_name[p['artist']]['birth_year']) < 2000]
        elif cat['value'] == 'genre_painting':
            filtered = [p for p in paintings if any('genre' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
        elif cat['value'] == 'religious':
            filtered = [p for p in paintings if any('religious' in (g or '').lower() for g in arr(p.get('artist_genre')) + arr(p.get('genre')))]
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