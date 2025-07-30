#!/usr/bin/env python3
"""
Infer art movements for artists missing movement data based on time periods and patterns.
"""

import json
import os
import re
from collections import defaultdict

def extract_year_from_string(year_str):
    """Extract a year from various date string formats."""
    if not year_str:
        return None
    
    # Look for 4-digit year patterns
    year_match = re.search(r'\b(17|18|19|20)\d{2}\b', str(year_str))
    if year_match:
        return int(year_match.group())
    
    return None

def infer_artist_movements():
    """Infer movements for artists based on their time periods and patterns."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"🎨 Inferring Art Movements")
    print(f"Total paintings: {len(data)}")
    print("-" * 60)
    
    # Group paintings by artist
    artist_data = defaultdict(list)
    for item in data:
        artist = item.get('artist', '')
        if artist:
            artist_data[artist].append(item)
    
    # Known movements from the data
    known_movements = {
        'Edvard Munch': 'Expressionism',
        'Rolf Nesch': 'Expressionism',
        'Christian Krohg': 'Realism',
        'Amaldus Nielsen': 'Realism',
        'Frits Thaulow': 'Impressionism',
        'Peder Severin Krøyer': 'Impressionism',
        'Adolph Tidemand': 'Romantic Nationalism',
        'Oda Krohg': 'Kristiania Bohemians',
        'Christian Skredsvig': 'Neo-Romanticism',
        'Halfdan Egedius': 'Symbolism',
        'Ludvig Karsten': 'Pointillism'
    }
    
    # Movement inference rules based on time periods
    def infer_movement_by_period(artist, years):
        if not years:
            return None
        
        # Extract years and find the most common period
        year_counts = defaultdict(int)
        for year_str in years:
            year = extract_year_from_string(year_str)
            if year:
                if year < 1850:
                    year_counts['pre-1850'] += 1
                elif 1850 <= year < 1880:
                    year_counts['1850-1880'] += 1
                elif 1880 <= year < 1900:
                    year_counts['1880-1900'] += 1
                elif 1900 <= year < 1920:
                    year_counts['1900-1920'] += 1
                else:
                    year_counts['post-1920'] += 1
        
        if not year_counts:
            return None
        
        dominant_period = max(year_counts.items(), key=lambda x: x[1])[0]
        
        # Norwegian art history periods
        if dominant_period == 'pre-1850':
            return 'Neo-Classicism'  # Early Norwegian art
        elif dominant_period == '1850-1880':
            return 'Romantic Nationalism'  # Golden age of Norwegian art
        elif dominant_period == '1880-1900':
            return 'Realism'  # Social realism period
        elif dominant_period == '1900-1920':
            return 'Impressionism'  # Late impressionism/early modern
        else:
            return 'Modernism'  # Post-1920
    
    # Analyze each artist
    artist_movements = {}
    artists_with_movements = []
    artists_without_movements = []
    inferred_movements = {}
    
    for artist, paintings in artist_data.items():
        movements = set()
        years = set()
        categories = set()
        
        for painting in paintings:
            # Collect existing movement data
            movement = painting.get('movement', '')
            if movement and movement.strip():
                movements.add(movement.strip())
            
            # Collect year data
            year = painting.get('year', '')
            if year and year.strip():
                years.add(year.strip())
            
            # Collect categories
            cats = painting.get('categories', [])
            if isinstance(cats, list):
                for cat in cats:
                    if cat and cat.strip():
                        categories.add(cat.strip())
        
        if movements:
            # Artist already has movement data
            artists_with_movements.append(artist)
            artist_movements[artist] = list(movements)
        else:
            # Artist needs movement inference
            artists_without_movements.append(artist)
            
            # Try to infer movement
            inferred_movement = None
            
            # Check if we have a known movement for this artist
            if artist in known_movements:
                inferred_movement = known_movements[artist]
            else:
                # Infer based on time period
                inferred_movement = infer_movement_by_period(artist, years)
            
            if inferred_movement:
                inferred_movements[artist] = inferred_movement
                artist_movements[artist] = [inferred_movement]
    
    print(f"Artists with existing movement data: {len(artists_with_movements)}")
    print(f"Artists without movement data: {len(artists_without_movements)}")
    print(f"Artists with inferred movements: {len(inferred_movements)}")
    print()
    
    # Show inferred movements
    print("🎭 Inferred Movements:")
    print()
    
    # Group by inferred movement
    movement_groups = defaultdict(list)
    for artist, movement in inferred_movements.items():
        movement_groups[movement].append(artist)
    
    for movement, artists in sorted(movement_groups.items()):
        print(f"• {movement} ({len(artists)} artists):")
        for artist in sorted(artists):
            painting_count = len(artist_data[artist])
            print(f"  - {artist} ({painting_count} paintings)")
        print()
    
    # Show artists that couldn't be inferred
    uninferred = [artist for artist in artists_without_movements if artist not in inferred_movements]
    if uninferred:
        print("❓ Artists that couldn't be inferred:")
        for artist in uninferred:
            painting_count = len(artist_data[artist])
            print(f"  - {artist} ({painting_count} paintings)")
        print()
    
    # Summary statistics
    print("📊 Movement Distribution After Inference:")
    print()
    
    all_movements = defaultdict(int)
    for artist, movements in artist_movements.items():
        for movement in movements:
            all_movements[movement] += 1
    
    for movement, count in sorted(all_movements.items(), key=lambda x: x[1], reverse=True):
        print(f"• {movement}: {count} artists")
    
    print()
    print("🎯 Quiz Category Recommendations:")
    print()
    
    # Recommend categories based on inferred movements
    good_categories = []
    for movement, count in all_movements.items():
        if count >= 5:
            good_categories.append((movement, count))
    
    good_categories.sort(key=lambda x: x[1], reverse=True)
    
    for movement, count in good_categories:
        quality = "🟢" if count >= 10 else "🟡"
        print(f"{quality} {movement} ({count} artists)")
    
    return artist_movements, inferred_movements

def main():
    infer_artist_movements()

if __name__ == '__main__':
    main() 