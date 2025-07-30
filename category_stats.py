#!/usr/bin/env python3
"""
Quick diagnostic to find categories with most entries.

Usage:
python category_stats.py
"""

import json
import os
from collections import Counter
from typing import Dict, List, Any

def analyze_categories() -> None:
    """Analyze the dataset and show category statistics."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Dataset Analysis")
    print(f"Total paintings: {len(data)}")
    print("-" * 50)
    
    # Count by category and genre
    category_counts = Counter()
    genre_counts = Counter()
    movement_counts = Counter()
    artist_counts = Counter()
    
    for item in data:
        artist = item.get('artist', 'Unknown')
        artist_counts[artist] += 1
        
        # Count by genre
        genre = item.get('genre', 'Unknown')
        genre_counts[genre] += 1
        
        # Count by movement
        movement = item.get('movement', 'Unknown')
        movement_counts[movement] += 1
        
        # Count by categories (list field)
        categories = item.get('categories', [])
        if isinstance(categories, list):
            for category in categories:
                category_counts[category] += 1
        else:
            category_counts['Unknown'] += 1
    
    # Show genre statistics
    print("🎨 Genres by number of paintings:")
    print()
    
    # Sort genres by count (descending)
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (genre, count) in enumerate(sorted_genres, 1):
        percentage = (count / len(data)) * 100
        print(f"{i:2d}. {genre:<20} {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("🎭 Art Movements by number of paintings:")
    print()
    
    # Sort movements by count (descending)
    sorted_movements = sorted(movement_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (movement, count) in enumerate(sorted_movements, 1):
        percentage = (count / len(data)) * 100
        print(f"{i:2d}. {movement:<25} {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("🏷️  Categories (from categories list) by number of paintings:")
    print()
    
    # Sort categories by count (descending)
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (category, count) in enumerate(sorted_categories[:15], 1):  # Show top 15
        percentage = (count / len(data)) * 100
        print(f"{i:2d}. {category:<25} {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("👨‍🎨 Top 10 artists by number of paintings:")
    print()
    
    # Sort artists by count (descending)
    sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (artist, count) in enumerate(sorted_artists[:10], 1):
        percentage = (count / len(data)) * 100
        print(f"{i:2d}. {artist:<25} {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("📈 Summary:")
    print(f"• Total genres: {len(genre_counts)}")
    print(f"• Total movements: {len(movement_counts)}")
    print(f"• Total categories: {len(category_counts)}")
    print(f"• Total artists: {len(artist_counts)}")
    print(f"• Most paintings in a genre: {max(genre_counts.values()) if genre_counts else 0}")
    print(f"• Most paintings in a movement: {max(movement_counts.values()) if movement_counts else 0}")
    print(f"• Most paintings by one artist: {max(artist_counts.values()) if artist_counts else 0}")
    
    # Show genres with very few paintings
    print()
    print("⚠️  Genres with 5 or fewer paintings:")
    small_genres = [(genre, count) for genre, count in genre_counts.items() if count <= 5]
    if small_genres:
        for genre, count in sorted(small_genres, key=lambda x: x[1]):
            print(f"  • {genre}: {count} paintings")
    else:
        print("  None found!")
    
    # Show movements with very few paintings
    print()
    print("⚠️  Movements with 5 or fewer paintings:")
    small_movements = [(movement, count) for movement, count in movement_counts.items() if count <= 5]
    if small_movements:
        for movement, count in sorted(small_movements, key=lambda x: x[1]):
            print(f"  • {movement}: {count} paintings")
    else:
        print("  None found!")

def main():
    analyze_categories()

if __name__ == '__main__':
    main() 