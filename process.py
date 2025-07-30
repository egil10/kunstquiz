#!/usr/bin/env python3
"""
Kunstquiz Data Processing Script
================================

Consolidated script for all data processing operations.

USAGE EXAMPLES:
==============

# Apply inferred categories
python process.py --categories

# Infer art movements
python process.py --movements

# Analyze artist movements
python process.py --analyze-movements

# Discover new categories
python process.py --discover

# Merge artist tags
python process.py --merge-tags

# Full processing workflow
python process.py --full-process

ARGUMENTS:
==========
--categories: Apply inferred categories
--movements: Infer art movements
--analyze-movements: Analyze artist movements
--discover: Discover new categories
--merge-tags: Merge artist tags
--full-process: Run all processing operations

--input: Input JSON file (default: data/paintings_appended.json)
--output: Output JSON file (default: data/paintings_merged.json)
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
    print("🏷️  Applying inferred categories...")
    
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
    
    print(f"✅ Applied categories to {processed_count} paintings")
    return data

def infer_movements(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Infer art movements based on various criteria"""
    print("🎭 Inferring art movements...")
    
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
    
    print(f"✅ Inferred movements for {processed_count} paintings")
    return data

def analyze_artist_movements(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze movements by artist"""
    print("👨‍🎨 Analyzing artist movements...")
    
    artist_movements = defaultdict(set)
    artist_counts = Counter()
    
    for item in data:
        artist = item.get('artist', '')
        if not artist:
            continue
        
        artist_counts[artist] += 1
        
        # Collect all movement information
        movements = []
        
        # Explicit movements
        if item.get('movement'):
            movements.append(item['movement'])
        
        # Inferred movements
        if item.get('inferred_movements'):
            movements.extend(item['inferred_movements'])
        
        # Add to artist's movement set
        for movement in movements:
            artist_movements[artist].add(movement)
    
    # Analyze results
    analysis = {
        'total_artists': len(artist_counts),
        'artists_with_movements': len([a for a, m in artist_movements.items() if m]),
        'movement_distribution': Counter(),
        'artist_movement_details': {}
    }
    
    # Count movements across all artists
    for movements in artist_movements.values():
        for movement in movements:
            analysis['movement_distribution'][movement] += 1
    
    # Create detailed artist analysis
    for artist, movements in artist_movements.items():
        analysis['artist_movement_details'][artist] = {
            'movements': list(movements),
            'painting_count': artist_counts[artist],
            'movement_count': len(movements)
        }
    
    print(f"✅ Analyzed movements for {analysis['artists_with_movements']} artists")
    return analysis

def discover_categories(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Discover new categories in the dataset"""
    print("🔍 Discovering new categories...")
    
    # Collect all potential category indicators
    title_keywords = Counter()
    genre_keywords = Counter()
    movement_keywords = Counter()
    
    for item in data:
        title = item.get('title', '').lower()
        genre = item.get('genre', '').lower()
        movement = item.get('movement', '').lower()
        
        # Extract keywords from titles
        words = re.findall(r'\b\w+\b', title)
        for word in words:
            if len(word) > 3:  # Skip short words
                title_keywords[word] += 1
        
        # Collect genres and movements
        if genre:
            genre_keywords[genre] += 1
        if movement:
            movement_keywords[movement] += 1
    
    # Analyze results
    discovery = {
        'common_title_keywords': title_keywords.most_common(20),
        'genres': genre_keywords.most_common(),
        'movements': movement_keywords.most_common(),
        'potential_categories': []
    }
    
    # Identify potential new categories
    potential_categories = []
    
    # Look for common themes in titles
    for keyword, count in title_keywords.most_common(50):
        if count >= 5:  # At least 5 occurrences
            potential_categories.append({
                'type': 'title_keyword',
                'name': keyword,
                'count': count,
                'confidence': 'medium'
            })
    
    # Look for underrepresented genres
    for genre, count in genre_keywords.items():
        if count >= 3 and count <= 20:  # Not too common, not too rare
            potential_categories.append({
                'type': 'genre',
                'name': genre,
                'count': count,
                'confidence': 'high'
            })
    
    discovery['potential_categories'] = potential_categories
    
    print(f"✅ Discovered {len(potential_categories)} potential categories")
    return discovery

def merge_artist_tags(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge artist tags and bios into paintings data"""
    print("🔗 Merging artist tags and bios...")
    
    # Load artist bios
    bios_file = 'data/artist_bios.json'
    artist_bios = {}
    
    if os.path.exists(bios_file):
        try:
            with open(bios_file, 'r', encoding='utf-8') as f:
                bios_data = json.load(f)
            
            for artist in bios_data:
                name = artist.get('name', '')
                if name:
                    artist_bios[name] = artist
            
            print(f"Loaded bios for {len(artist_bios)} artists")
        except Exception as e:
            print(f"Error loading artist bios: {e}")
    else:
        print("Artist bios file not found")
    
    # Load artist tags
    tags_file = 'data/artist_tags.json'
    artist_tags = {}
    
    if os.path.exists(tags_file):
        try:
            with open(tags_file, 'r', encoding='utf-8') as f:
                tags_data = json.load(f)
            
            for artist in tags_data:
                name = artist.get('name', '')
                if name:
                    artist_tags[name] = artist
            
            print(f"Loaded tags for {len(artist_tags)} artists")
        except Exception as e:
            print(f"Error loading artist tags: {e}")
    else:
        print("Artist tags file not found")
    
    # Merge data
    merged_count = 0
    
    for item in data:
        artist = item.get('artist', '')
        if not artist:
            continue
        
        # Add bio information
        if artist in artist_bios:
            bio = artist_bios[artist]
            item['artist_bio'] = bio.get('bio', '')
            item['artist_birth_year'] = bio.get('birth_year', '')
            item['artist_death_year'] = bio.get('death_year', '')
            item['artist_gender'] = bio.get('gender', '')
            merged_count += 1
        
        # Add tag information
        if artist in artist_tags:
            tags = artist_tags[artist]
            item['artist_tags'] = tags.get('tags', [])
            item['artist_movements'] = tags.get('movements', [])
            item['artist_genres'] = tags.get('genres', [])
            merged_count += 1
    
    print(f"✅ Merged data for {merged_count} paintings")
    return data

def full_process(data: List[Dict[str, Any]], input_file: str, output_file: str) -> List[Dict[str, Any]]:
    """Run full processing workflow"""
    print("🔄 Running full processing workflow...")
    
    # Step 1: Apply inferred categories
    data = apply_inferred_categories(data)
    
    # Step 2: Infer movements
    data = infer_movements(data)
    
    # Step 3: Merge artist tags and bios
    data = merge_artist_tags(data)
    
    # Step 4: Analyze artist movements
    movement_analysis = analyze_artist_movements(data)
    
    # Step 5: Discover new categories
    category_discovery = discover_categories(data)
    
    # Save processed data
    print(f"💾 Saving processed data to {output_file}...")
    save_json(data, output_file)
    
    # Save analysis results
    analysis_file = 'data/processing_analysis.json'
    analysis_data = {
        'movement_analysis': movement_analysis,
        'category_discovery': category_discovery,
        'processing_summary': {
            'total_paintings': len(data),
            'paintings_with_categories': len([item for item in data if item.get('inferred_categories')]),
            'paintings_with_movements': len([item for item in data if item.get('inferred_movements')]),
            'paintings_with_bios': len([item for item in data if item.get('artist_bio')])
        }
    }
    
    save_json(analysis_data, analysis_file)
    
    print("✅ Full processing workflow complete!")
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
    parser.add_argument('--input', default='data/paintings_appended.json', help='Input JSON file')
    parser.add_argument('--output', default='data/paintings_merged.json', help='Output JSON file')
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
        print("\n🔍 DRY RUN - No changes will be made")
    
    # Run requested operations
    if args.categories:
        print("\n🏷️  Applying inferred categories...")
        if not dry_run:
            data = apply_inferred_categories(data)
        else:
            print("Would apply inferred categories")
    
    if args.movements:
        print("\n🎭 Inferring art movements...")
        if not dry_run:
            data = infer_movements(data)
        else:
            print("Would infer art movements")
    
    if args.analyze_movements:
        print("\n👨‍🎨 Analyzing artist movements...")
        if not dry_run:
            analysis = analyze_artist_movements(data)
            print(f"Analysis complete for {analysis['artists_with_movements']} artists")
        else:
            print("Would analyze artist movements")
    
    if args.discover:
        print("\n🔍 Discovering new categories...")
        if not dry_run:
            discovery = discover_categories(data)
            print(f"Discovered {len(discovery['potential_categories'])} potential categories")
        else:
            print("Would discover new categories")
    
    if args.merge_tags:
        print("\n🔗 Merging artist tags...")
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
        print(f"\n💾 Saving processed data to {args.output}...")
        save_json(data, args.output)
        print("✅ Processing complete!")
    elif dry_run:
        print("\n📊 DRY RUN SUMMARY:")
        print("No actual processing performed. To process, run with --no-dry-run")
    else:
        print("\n✅ No processing operations specified")

if __name__ == '__main__':
    main() 