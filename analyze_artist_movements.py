#!/usr/bin/env python3
"""
Analyze artists and their movements in detail to see if we can infer more movement classifications.
"""

import json
import os
from collections import Counter, defaultdict

def analyze_artist_movements():
    """Analyze artists and their movements to see what we can infer."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"🎨 Artist Movement Analysis")
    print(f"Total paintings: {len(data)}")
    print("-" * 60)
    
    # Group paintings by artist
    artist_data = defaultdict(list)
    for item in data:
        artist = item.get('artist', '')
        if artist:
            artist_data[artist].append(item)
    
    print(f"Total unique artists: {len(artist_data)}")
    print()
    
    # Analyze each artist
    artist_movements = {}
    artists_with_movements = []
    artists_without_movements = []
    
    for artist, paintings in artist_data.items():
        movements = set()
        genres = set()
        categories = set()
        years = set()
        
        for painting in paintings:
            # Collect movement data
            movement = painting.get('movement', '')
            if movement and movement.strip():
                movements.add(movement.strip())
            
            # Collect genre data
            genre = painting.get('genre', '')
            if genre and genre.strip():
                genres.add(genre.strip())
            
            # Collect categories data
            cats = painting.get('categories', [])
            if isinstance(cats, list):
                for cat in cats:
                    if cat and cat.strip():
                        categories.add(cat.strip())
            
            # Collect year data
            year = painting.get('year', '')
            if year and year.strip():
                years.add(year.strip())
        
        artist_movements[artist] = {
            'movements': list(movements),
            'genres': list(genres),
            'categories': list(categories),
            'years': list(years),
            'painting_count': len(paintings)
        }
        
        if movements:
            artists_with_movements.append(artist)
        else:
            artists_without_movements.append(artist)
    
    print(f"Artists with movement data: {len(artists_with_movements)}")
    print(f"Artists without movement data: {len(artists_without_movements)}")
    print()
    
    # Show artists with movement data
    print("🎭 Artists with Movement Data:")
    print()
    for artist in artists_with_movements:
        info = artist_movements[artist]
        print(f"• {artist} ({info['painting_count']} paintings)")
        print(f"  Movements: {', '.join(info['movements']) if info['movements'] else 'None'}")
        print(f"  Genres: {', '.join(info['genres']) if info['genres'] else 'None'}")
        print(f"  Categories: {', '.join(info['categories'][:5]) if info['categories'] else 'None'}")
        print()
    
    # Show artists without movement data
    print("❓ Artists WITHOUT Movement Data (potential for inference):")
    print()
    for artist in artists_without_movements[:20]:  # Show first 20
        info = artist_movements[artist]
        print(f"• {artist} ({info['painting_count']} paintings)")
        print(f"  Genres: {', '.join(info['genres']) if info['genres'] else 'None'}")
        print(f"  Categories: {', '.join(info['categories'][:3]) if info['categories'] else 'None'}")
        print(f"  Years: {', '.join(info['years'][:3]) if info['years'] else 'None'}")
        print()
    
    if len(artists_without_movements) > 20:
        print(f"... and {len(artists_without_movements) - 20} more artists without movement data")
    
    # Analyze what movements we have
    print("📊 Movement Analysis:")
    print()
    
    all_movements = Counter()
    all_genres = Counter()
    all_categories = Counter()
    
    for artist_info in artist_movements.values():
        for movement in artist_info['movements']:
            all_movements[movement] += 1
        for genre in artist_info['genres']:
            all_genres[genre] += 1
        for category in artist_info['categories']:
            all_categories[category] += 1
    
    print("🎭 All Movements Found:")
    for movement, count in all_movements.most_common():
        print(f"• {movement}: {count} artists")
    
    print()
    print("🎨 All Genres Found:")
    for genre, count in all_genres.most_common():
        print(f"• {genre}: {count} artists")
    
    print()
    print("🏷️ Top Categories Found:")
    for category, count in all_categories.most_common(15):
        print(f"• {category}: {count} artists")
    
    # Look for patterns that might help with inference
    print()
    print("🔍 Potential Inference Patterns:")
    print()
    
    # Check if certain artists are consistently categorized together
    artist_categories = defaultdict(set)
    for artist, info in artist_movements.items():
        for category in info['categories']:
            artist_categories[category].add(artist)
    
    print("Categories with multiple artists (potential movement groups):")
    for category, artists in sorted(artist_categories.items(), key=lambda x: len(x[1]), reverse=True):
        if len(artists) >= 3:  # Only show categories with 3+ artists
            print(f"• {category}: {len(artists)} artists")
            print(f"  Artists: {', '.join(sorted(artists))}")
            print()

def main():
    analyze_artist_movements()

if __name__ == '__main__':
    main() 