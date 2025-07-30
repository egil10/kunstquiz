#!/usr/bin/env python3
"""
Analyze categories by number of unique artists rather than painting count.
This is more important for quiz functionality.
"""

import json
import os
from collections import Counter, defaultdict

def analyze_categories_by_artists():
    """Analyze categories by number of unique artists."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Category Analysis by Artist Count")
    print(f"Total paintings: {len(data)}")
    print(f"Total unique artists: {len(set(item.get('artist', '') for item in data if item.get('artist')))}")
    print("-" * 60)
    
    # Define the categories we want to check
    categories = {
        'popular': 'Popular Painters (top 10 by painting count)',
        'landscape': 'Landscape',
        'realism': 'Realism',
        'expressionism': 'Expressionism', 
        'impressionism': 'Impressionism',
        'romantic_nationalism': 'Romantic Nationalism',
        'neo_romanticism': 'Neo-Romanticism'
    }
    
    # Analyze each category
    category_stats = {}
    
    for category_key, category_name in categories.items():
        artists_in_category = set()
        paintings_in_category = []
        
        for item in data:
            artist = item.get('artist', '')
            if not artist:
                continue
                
            # Check if this painting belongs to the category
            belongs_to_category = False
            
            if category_key == 'popular':
                # We'll handle this separately
                continue
            elif category_key == 'landscape':
                genre = item.get('genre', '')
                if 'landscape' in genre.lower():
                    belongs_to_category = True
            elif category_key == 'realism':
                movement = item.get('movement', '')
                if 'realism' in movement.lower():
                    belongs_to_category = True
            elif category_key == 'expressionism':
                movement = item.get('movement', '')
                if 'expressionism' in movement.lower():
                    belongs_to_category = True
            elif category_key == 'impressionism':
                movement = item.get('movement', '')
                if 'impressionism' in movement.lower():
                    belongs_to_category = True
            elif category_key == 'romantic_nationalism':
                movement = item.get('movement', '')
                if 'romantic nationalism' in movement.lower():
                    belongs_to_category = True
            elif category_key == 'neo_romanticism':
                movement = item.get('movement', '')
                if 'neo-romanticism' in movement.lower():
                    belongs_to_category = True
            
            if belongs_to_category:
                artists_in_category.add(artist)
                paintings_in_category.append(item)
        
        category_stats[category_key] = {
            'name': category_name,
            'artists': len(artists_in_category),
            'paintings': len(paintings_in_category),
            'artist_list': list(artists_in_category)
        }
    
    # Handle popular category separately
    artist_counts = Counter()
    for item in data:
        artist = item.get('artist', '')
        if artist:
            artist_counts[artist] += 1
    
    top_10_artists = [artist for artist, count in artist_counts.most_common(10)]
    popular_paintings = [item for item in data if item.get('artist') in top_10_artists]
    
    category_stats['popular'] = {
        'name': 'Popular Painters (top 10 by painting count)',
        'artists': len(top_10_artists),
        'paintings': len(popular_paintings),
        'artist_list': top_10_artists
    }
    
    # Sort by artist count (descending)
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['artists'], reverse=True)
    
    print("🎨 Categories by number of unique artists:")
    print()
    
    for i, (category_key, stats) in enumerate(sorted_categories, 1):
        print(f"{i}. {stats['name']}")
        print(f"   Artists: {stats['artists']}")
        print(f"   Paintings: {stats['paintings']}")
        if stats['artists'] > 0:
            print(f"   Avg paintings per artist: {stats['paintings'] / stats['artists']:.1f}")
        else:
            print(f"   Avg paintings per artist: N/A (no artists)")
        print()
    
    print("⚠️  Categories with 5 or fewer artists (problematic for quiz):")
    print()
    
    problematic_categories = [(key, stats) for key, stats in category_stats.items() if stats['artists'] <= 5]
    
    if problematic_categories:
        for category_key, stats in problematic_categories:
            print(f"• {stats['name']}: {stats['artists']} artists")
            print(f"  Artists: {', '.join(stats['artist_list'])}")
            print()
    else:
        print("  None found! All categories have sufficient artists.")
    
    print("✅ Categories with 10+ artists (good for quiz):")
    print()
    
    good_categories = [(key, stats) for key, stats in category_stats.items() if stats['artists'] >= 10]
    
    for category_key, stats in good_categories:
        print(f"• {stats['name']}: {stats['artists']} artists")
    
    print()
    print("📈 Summary:")
    print(f"• Total categories analyzed: {len(categories)}")
    print(f"• Categories with 5+ artists: {len([s for s in category_stats.values() if s['artists'] >= 5])}")
    print(f"• Categories with 10+ artists: {len([s for s in category_stats.values() if s['artists'] >= 10])}")

def main():
    analyze_categories_by_artists()

if __name__ == '__main__':
    main() 