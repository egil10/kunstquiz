#!/usr/bin/env python3
"""
Discover all available categories in the dataset and analyze them by artist count.
This helps us pick the best categories for the quiz.
"""

import json
import os
from collections import Counter, defaultdict

def discover_all_categories():
    """Discover all categories in the dataset and analyze them."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"🔍 Discovering All Categories in Dataset")
    print(f"Total paintings: {len(data)}")
    print(f"Total unique artists: {len(set(item.get('artist', '') for item in data if item.get('artist')))}")
    print("-" * 70)
    
    # Collect all possible categories from different fields
    all_categories = defaultdict(set)
    all_artists = defaultdict(set)
    
    for item in data:
        artist = item.get('artist', '')
        if not artist:
            continue
        
        # Check genre field
        genre = item.get('genre', '')
        if genre and str(genre).strip():
            all_categories[str(genre)].add(artist)
            all_artists[str(genre)].add(artist)
        
        # Check movement field
        movement = item.get('movement', '')
        if movement and str(movement).strip():
            all_categories[str(movement)].add(artist)
            all_artists[str(movement)].add(artist)
        
        # Check categories list
        categories_list = item.get('categories', [])
        if isinstance(categories_list, list):
            for cat in categories_list:
                if cat and cat.strip():
                    all_categories[cat].add(artist)
                    all_artists[cat].add(artist)
        
        # Check century
        century = item.get('century', '')
        if century and str(century).strip():
            all_categories[f"Century: {century}"].add(artist)
            all_artists[f"Century: {century}"].add(artist)
        
        # Check artist gender
        gender = item.get('artist_gender', '')
        if gender and str(gender).strip():
            all_categories[f"Gender: {gender}"].add(artist)
            all_artists[f"Gender: {gender}"].add(artist)
    
    # Convert to statistics
    category_stats = []
    for category_name, artists in all_categories.items():
        # Count paintings for this category
        paintings_count = 0
        for item in data:
            artist = item.get('artist', '')
            if artist in artists:
                paintings_count += 1
        
        category_stats.append({
            'name': category_name,
            'artists': len(artists),
            'paintings': paintings_count,
            'avg_per_artist': paintings_count / len(artists) if artists else 0,
            'artist_list': list(artists)
        })
    
    # Sort by artist count (descending)
    category_stats.sort(key=lambda x: x['artists'], reverse=True)
    
    print("📊 All Discovered Categories (sorted by artist count):")
    print()
    
    for i, stats in enumerate(category_stats, 1):
        print(f"{i:2d}. {stats['name']}")
        print(f"    Artists: {stats['artists']:2d} | Paintings: {stats['paintings']:4d} | Avg: {stats['avg_per_artist']:5.1f}")
        if stats['artists'] <= 10:  # Show artist names for small categories
            print(f"    Artists: {', '.join(stats['artist_list'])}")
        print()
    
    print("✅ Excellent Categories (10+ artists):")
    print()
    excellent = [s for s in category_stats if s['artists'] >= 10]
    for stats in excellent:
        print(f"• {stats['name']} ({stats['artists']} artists, {stats['paintings']} paintings)")
    
    print()
    print("⚠️  Good Categories (5-9 artists):")
    print()
    good = [s for s in category_stats if 5 <= s['artists'] < 10]
    for stats in good:
        print(f"• {stats['name']} ({stats['artists']} artists, {stats['paintings']} paintings)")
    
    print()
    print("❌ Poor Categories (1-4 artists):")
    print()
    poor = [s for s in category_stats if 1 <= s['artists'] < 5]
    for stats in poor:
        print(f"• {stats['name']} ({stats['artists']} artists, {stats['paintings']} paintings)")
    
    print()
    print("📈 Summary:")
    print(f"• Total unique categories found: {len(category_stats)}")
    print(f"• Excellent categories (10+ artists): {len(excellent)}")
    print(f"• Good categories (5-9 artists): {len(good)}")
    print(f"• Poor categories (1-4 artists): {len(poor)}")
    
    # Show some specific recommendations
    print()
    print("🎯 Recommended Categories for Quiz:")
    print()
    
    # Top 10 by artist count
    top_10 = category_stats[:10]
    for i, stats in enumerate(top_10, 1):
        quality = "🟢" if stats['artists'] >= 10 else "🟡" if stats['artists'] >= 5 else "🔴"
        print(f"{i}. {quality} {stats['name']} ({stats['artists']} artists)")

def main():
    discover_all_categories()

if __name__ == '__main__':
    main() 