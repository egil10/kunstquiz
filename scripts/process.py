#!/usr/bin/env python3
"""
Kunstquiz Data Processing Script
================================

Consolidated script for all data processing operations.

USAGE EXAMPLES:
==============

# Apply inferred categories
python scripts/process.py --categories

# Infer art movements
python scripts/process.py --movements

# Analyze artist movements
python scripts/process.py --analyze-movements

# Discover new categories
python scripts/process.py --discover

# Merge artist tags
python scripts/process.py --merge-tags

# Full processing workflow
python scripts/process.py --full-process

ARGUMENTS:
==========
--categories: Apply inferred categories
--movements: Infer art movements
--analyze-movements: Analyze artist movements
--discover: Discover new categories
--merge-tags: Merge artist tags
--full-process: Run all processing operations

--input: Input JSON file (default: data/paintings.json)
--output: Output JSON file (default: data/paintings.json)
--dry-run: Show what would be processed without actually processing
--no-dry-run: Actually perform the processing
"""

import json
import argparse
import os
import re
from typing import List, Dict, Any, Set
from collections import Counter, defaultdict

def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {filepath} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        return []

def save_json(data: List[Dict[str, Any]], filepath: str):
    """Save JSON file with pretty formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def apply_inferred_categories(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply inferred categories to paintings"""
    print("Applying inferred categories...")
    
    # Define category mappings
    category_mappings = {
        'landscape': ['landscape', 'landskap', 'nature', 'natur', 'mountain', 'fjell', 'forest', 'skog'],
        'portrait': ['portrait', 'portrett', 'person', 'face', 'head'],
        'still_life': ['still life', 'stilleben', 'fruit', 'frukt', 'flower', 'blomst'],
        'genre': ['genre', 'everyday', 'hverdags', 'peasant', 'bonde'],
        'historical': ['historical', 'historisk', 'battle', 'slag', 'war', 'krig'],
        'religious': ['religious', 'religiøs', 'bible', 'bibel', 'christ', 'kristus'],
        'mythological': ['mythological', 'mythologisk', 'myth', 'myte', 'greek', 'gresk'],
        'romantic': ['romantic', 'romantisk', 'romanticism', 'romantikk'],
        'realism': ['realism', 'realistisk', 'realist'],
        'impressionism': ['impressionism', 'impressionistisk', 'impressionist'],
        'expressionism': ['expressionism', 'expressionistisk', 'expressionist'],
        'modern': ['modern', 'moderne', 'contemporary', 'samtidig'],
        'abstract': ['abstract', 'abstrakt', 'non-figurative', 'ikke-figurativ']
    }
    
    processed_count = 0
    
    for item in data:
        title = item.get('title', '').lower()
        genre = item.get('genre', '').lower()
        movement = item.get('movement', '').lower()
        
        # Combine all text for analysis
        all_text = f"{title} {genre} {movement}"
        
        # Find matching categories
        matched_categories = []
        for category, keywords in category_mappings.items():
            if any(keyword in all_text for keyword in keywords):
                matched_categories.append(category)
        
        # Apply categories if found
        if matched_categories:
            item['inferred_categories'] = matched_categories
            processed_count += 1
    
            print(f"Applied categories to {processed_count} paintings")
    return data

def infer_movements(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Infer art movements based on various criteria"""
    print("Inferring art movements...")
    
    # Define movement inference rules
    movement_rules = {
        'romanticism': {
            'keywords': ['romantic', 'romantisk', 'romanticism', 'romantikk', 'nationalism'],
            'period': ['19th', '1800s'],
            'artists': ['johan christian dahl', 'thomas fearnley', 'hans gude']
        },
        'realism': {
            'keywords': ['realism', 'realistisk', 'realist', 'naturalism'],
            'period': ['19th', '1800s'],
            'artists': ['adolph tidemand', 'hans fredrik gude']
        },
        'impressionism': {
            'keywords': ['impressionism', 'impressionistisk', 'impressionist', 'plein air'],
            'period': ['19th', '20th', '1800s', '1900s'],
            'artists': ['frits thaulow', 'christian krohg', 'erik werenskiold']
        },
        'expressionism': {
            'keywords': ['expressionism', 'expressionistisk', 'expressionist', 'emotion'],
            'period': ['20th', '1900s'],
            'artists': ['edvard munch', 'ludvig karsten']
        },
        'modernism': {
            'keywords': ['modern', 'moderne', 'modernism', 'contemporary'],
            'period': ['20th', '1900s'],
            'artists': ['reidar aulie', 'per krohg']
        }
    }
    
    processed_count = 0
    
    for item in data:
        title = item.get('title', '').lower()
        artist = item.get('artist', '').lower()
        year = item.get('year', '')
        century = item.get('century', '')
        
        # Combine all text for analysis
        all_text = f"{title} {artist}"
        
        # Find matching movements
        matched_movements = []
        for movement, rules in movement_rules.items():
            score = 0
            
            # Check keywords
            if any(keyword in all_text for keyword in rules['keywords']):
                score += 2
            
            # Check period
            if any(period in str(year) or period in str(century) for period in rules['period']):
                score += 1
            
            # Check artists
            if any(artist_name in artist for artist_name in rules['artists']):
                score += 2
            
            # If score is high enough, add movement
            if score >= 2:
                matched_movements.append(movement)
        
        # Apply movements if found
        if matched_movements:
            item['inferred_movements'] = matched_movements
            processed_count += 1
    
            print(f"Inferred movements for {processed_count} paintings")
    return data

def analyze_artist_movements(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze movements by artist"""
    print("Analyzing artist movements...")
    
    artist_movements = defaultdict(set)
    artist_periods = defaultdict(list)
    
    for painting in data:
        artist = painting.get('artist', '')
        movement = painting.get('movement', '')
        period = painting.get('period', '')
        
        if artist and movement:
            artist_movements[artist].add(movement)
        if artist and period:
            artist_periods[artist].append(period)
    
    # Find artists with multiple movements
    multi_movement_artists = {artist: list(movements) for artist, movements in artist_movements.items() if len(movements) > 1}
    
    # Find artists with multiple periods
    multi_period_artists = {}
    for artist, periods in artist_periods.items():
        unique_periods = list(set(periods))
        if len(unique_periods) > 1:
            multi_period_artists[artist] = unique_periods
    
    analysis = {
        'total_artists': len(artist_movements),
        'artists_with_movements': len(artist_movements),
        'multi_movement_artists': len(multi_movement_artists),
        'multi_period_artists': len(multi_period_artists),
        'sample_multi_movement': dict(list(multi_movement_artists.items())[:5]),
        'sample_multi_period': dict(list(multi_period_artists.items())[:5])
    }
    
    print(f"Analyzed movements for {analysis['artists_with_movements']} artists")
    return analysis

def discover_categories(data: List[Dict[str, Any]]) -> List[str]:
    """Discover potential new categories from the data"""
    print("Discovering new categories...")
    
    # Collect all unique values
    all_categories = set()
    all_movements = set()
    all_periods = set()
    all_techniques = set()
    
    for painting in data:
        if painting.get('category'):
            all_categories.add(painting['category'])
        if painting.get('movement'):
            all_movements.add(painting['movement'])
        if painting.get('period'):
            all_periods.add(painting['period'])
        if painting.get('technique'):
            all_techniques.add(painting['technique'])
    
    # Find potential new categories
    potential_categories = []
    
    # Movements that aren't categories yet
    for movement in all_movements:
        if movement and movement not in all_categories:
            potential_categories.append(f"Movement: {movement}")
    
    # Periods that aren't categories yet
    for period in all_periods:
        if period and period not in all_categories:
            potential_categories.append(f"Period: {period}")
    
    # Techniques that aren't categories yet
    for technique in all_techniques:
        if technique and technique not in all_categories:
            potential_categories.append(f"Technique: {technique}")
    
    # Find common themes in titles
    title_words = defaultdict(int)
    for painting in data:
        title = painting.get('title', '').lower()
        if title:
            words = re.findall(r'\b\w{4,}\b', title)  # Words with 4+ characters
            for word in words:
                title_words[word] += 1
    
    # Add common title words as potential categories
    common_words = {word: count for word, count in title_words.items() if count >= 3}
    for word, count in sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:10]:
        potential_categories.append(f"Title Theme: {word.title()} ({count} occurrences)")
    
    print(f"Discovered {len(potential_categories)} potential categories")
    return potential_categories

def merge_artist_tags(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge artist tag data from multiple sources"""
    print("Merging artist tags...")
    
    # Load existing artist tags
    artist_tags = {}
    tag_files = ['data/artists.json', 'data/artists.json']
    
    for filepath in tag_files:
        if os.path.exists(filepath):
            try:
                tags_data = load_json(filepath)
                if isinstance(tags_data, dict):
                    artist_tags.update(tags_data)
                elif isinstance(tags_data, list):
                    for artist in tags_data:
                        name = artist.get('name', '')
                        if name:
                            artist_tags[name] = artist
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
    
    # Merge tags into paintings data
    merged_count = 0
    for painting in data:
        artist = painting.get('artist', '')
        if artist and artist in artist_tags:
            artist_data = artist_tags[artist]
            
            # Merge tags
            if 'tags' in artist_data and artist_data['tags']:
                if 'tags' not in painting:
                    painting['tags'] = []
                painting['tags'].extend(artist_data['tags'])
                painting['tags'] = list(set(painting['tags']))  # Remove duplicates
            
            # Merge other basic fields
            for key in ['bio', 'nationality', 'birth_year', 'death_year']:
                if key in artist_data and artist_data[key] and key not in painting:
                    painting[key] = artist_data[key]

            # Merge movement and genre from artist bios for richer category filters
            # Normalize to arrays on the painting: 'artist_movement', 'artist_genre'
            def to_list(value):
                if value is None:
                    return []
                return value if isinstance(value, list) else [value]

            if 'movement' in artist_data and artist_data['movement']:
                painting['artist_movement'] = to_list(artist_data['movement'])

            if 'genre' in artist_data and artist_data['genre']:
                painting['artist_genre'] = to_list(artist_data['genre'])

            # Merge gender so category filters like female_artists work reliably
            if 'gender' in artist_data and artist_data['gender']:
                painting['artist_gender'] = artist_data['gender']

            # Provide a simple artist_bio text for filters that scan bio text (e.g., modernism)
            if 'english_bio' in artist_data and artist_data['english_bio']:
                painting.setdefault('artist_bio', artist_data['english_bio'])
            elif 'norwegian_bio' in artist_data and artist_data['norwegian_bio']:
                painting.setdefault('artist_bio', artist_data['norwegian_bio'])
            
            merged_count += 1
    
    print(f"Merged data for {merged_count} paintings")
    return data

def full_process(data: List[Dict[str, Any]], input_file: str, output_file: str) -> List[Dict[str, Any]]:
    """Run full processing workflow"""
    print("Running full processing workflow...")
    
    # Step 1: Apply inferred categories
    data = apply_inferred_categories(data)
    
    # Step 2: Infer movements
    data = infer_movements(data)
    
    # Step 3: Analyze artist movements
    analysis = analyze_artist_movements(data)
    
    # Step 4: Discover categories
    potential_categories = discover_categories(data)
    
    # Step 5: Merge artist tags
    data = merge_artist_tags(data)
    
    # Save results
    print(f"Saving processed data to {output_file}...")
    save_json(data, output_file)
    
    # Print summary
    print(f"Full processing workflow complete!")
    print(f"  - Processed {len(data)} paintings")
    print(f"  - Artists with movements: {analysis['artists_with_movements']}")
    print(f"  - Potential categories: {len(potential_categories)}")
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Data Processing Script')
    
    # Processing operations
    parser.add_argument('--categories', action='store_true', help='Apply inferred categories')
    parser.add_argument('--movements', action='store_true', help='Infer art movements')
    parser.add_argument('--analyze-movements', action='store_true', help='Analyze artist movements')
    parser.add_argument('--discover', action='store_true', help='Discover new categories')
    parser.add_argument('--merge-tags', action='store_true', help='Merge artist tags')
    parser.add_argument('--full-process', action='store_true', help='Run all processing operations')
    
    # Options
    parser.add_argument('--input', default='data/paintings.json', help='Input JSON file')
    parser.add_argument('--output', default='data/paintings.json', help='Output JSON file')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Show what would be processed without actually processing (default)')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually perform the processing')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} items from {args.input}")
    
    # Determine if this is a dry run
    dry_run = args.dry_run and not args.no_dry_run
    
    if dry_run:
        print("\nDRY RUN - No changes will be made")
    
    # Run requested operations
    if args.categories:
        print("\nApplying inferred categories...")
        if not dry_run:
            data = apply_inferred_categories(data)
        else:
            print("Would apply inferred categories")
    
    if args.movements:
        print("\nInferring art movements...")
        if not dry_run:
            data = infer_movements(data)
        else:
            print("Would infer art movements")
    
    if args.analyze_movements:
        print("\nAnalyzing artist movements...")
        if not dry_run:
            analysis = analyze_artist_movements(data)
            print(f"Analysis complete for {analysis['artists_with_movements']} artists")
        else:
            print("Would analyze artist movements")
    
    if args.discover:
        print("\nDiscovering new categories...")
        if not dry_run:
            potential_categories = discover_categories(data)
            print(f"Discovered {len(potential_categories)} potential categories")
        else:
            print("Would discover new categories")
    
    if args.merge_tags:
        print("\nMerging artist tags...")
        if not dry_run:
            data = merge_artist_tags(data)
        else:
            print("Would merge artist tags")
    
    if args.full_process:
        if not dry_run:
            data = full_process(data, args.input, args.output)
        else:
            print("Would run full processing workflow")
    
    # Save results if not dry run and operations were performed
    if not dry_run and any([args.categories, args.movements, args.merge_tags, args.full_process]):
        print(f"\nSaving processed data to {args.output}...")
        save_json(data, args.output)
        print("Processing complete!")
    elif dry_run:
        print("\nDRY RUN SUMMARY:")
        print("No actual processing performed. To process, run with --no-dry-run")
    else:
        print("\nNo processing operations specified")

if __name__ == '__main__':
    main() 