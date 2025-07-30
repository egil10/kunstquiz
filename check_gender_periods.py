#!/usr/bin/env python3
"""
Check gender and time period categories for quiz viability.
"""

import json
import os
from collections import Counter, defaultdict

def check_gender_and_periods():
    """Check gender and time period categories."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"👥 Gender and Time Period Analysis")
    print(f"Total paintings: {len(data)}")
    print("-" * 60)
    
    # Group paintings by artist
    artist_data = defaultdict(list)
    for item in data:
        artist = item.get('artist', '')
        if artist:
            artist_data[artist].append(item)
    
    # Analyze gender categories
    print("👥 Gender Categories:")
    print()
    
    male_artists = set()
    female_artists = set()
    unknown_gender_artists = set()
    
    for artist, paintings in artist_data.items():
        # Check gender from first painting (should be consistent)
        gender = paintings[0].get('artist_gender', '')
        
        if gender == 'male':
            male_artists.add(artist)
        elif gender == 'female':
            female_artists.add(artist)
        else:
            unknown_gender_artists.add(artist)
    
    print(f"Male artists: {len(male_artists)}")
    print(f"Female artists: {len(female_artists)}")
    print(f"Unknown gender: {len(unknown_gender_artists)}")
    print()
    
    if female_artists:
        print("Female artists:")
        for artist in sorted(female_artists):
            painting_count = len(artist_data[artist])
            print(f"  • {artist} ({painting_count} paintings)")
        print()
    
    # Analyze time periods
    print("📅 Time Period Categories:")
    print()
    
    period_artists = defaultdict(set)
    century_artists = defaultdict(set)
    
    for artist, paintings in artist_data.items():
        for painting in paintings:
            # Check century field
            century = painting.get('century', '')
            if century:
                century_artists[str(century)].add(artist)
            
            # Check categories for time periods
            categories = painting.get('categories', [])
            if isinstance(categories, list):
                for cat in categories:
                    if any(period in cat.lower() for period in ['1800s', '1900s', '2000s', '2100s']):
                        period_artists[cat].add(artist)
    
    print("Century-based categories:")
    for century, artists in sorted(century_artists.items()):
        print(f"  • Century {century}: {len(artists)} artists")
        if len(artists) <= 10:  # Show artist names for smaller categories
            print(f"    Artists: {', '.join(sorted(artists))}")
        print()
    
    print("Period-based categories:")
    for period, artists in sorted(period_artists.items()):
        print(f"  • {period}: {len(artists)} artists")
        if len(artists) <= 10:  # Show artist names for smaller categories
            print(f"    Artists: {', '.join(sorted(artists))}")
        print()
    
    # Check for specific year ranges that might work well
    print("🎯 Specific Year Range Analysis:")
    print()
    
    # Group artists by their dominant time period
    artist_periods = {}
    for artist, paintings in artist_data.items():
        years = []
        for painting in paintings:
            year_str = painting.get('year', '')
            if year_str:
                # Extract year from string
                import re
                year_match = re.search(r'\b(17|18|19|20)\d{2}\b', str(year_str))
                if year_match:
                    years.append(int(year_match.group()))
        
        if years:
            # Find the most common decade
            decade_counts = Counter()
            for year in years:
                decade = (year // 10) * 10
                decade_counts[decade] += 1
            
            if decade_counts:
                dominant_decade = max(decade_counts.items(), key=lambda x: x[1])[0]
                artist_periods[artist] = dominant_decade
    
    # Group by decades
    decade_groups = defaultdict(list)
    for artist, decade in artist_periods.items():
        decade_groups[decade].append(artist)
    
    print("Decade-based categories:")
    for decade, artists in sorted(decade_groups.items()):
        if len(artists) >= 3:  # Only show categories with 3+ artists
            print(f"  • {decade}s: {len(artists)} artists")
            if len(artists) <= 15:  # Show artist names for smaller categories
                print(f"    Artists: {', '.join(sorted(artists))}")
            print()
    
    # Summary and recommendations
    print("📊 Quiz Category Recommendations:")
    print()
    
    recommendations = []
    
    # Gender categories
    if len(male_artists) >= 10:
        recommendations.append(("Male Artists", len(male_artists), "🟢"))
    elif len(male_artists) >= 5:
        recommendations.append(("Male Artists", len(male_artists), "🟡"))
    
    if len(female_artists) >= 5:
        recommendations.append(("Female Artists", len(female_artists), "🟡"))
    elif len(female_artists) >= 3:
        recommendations.append(("Female Artists", len(female_artists), "🟠"))
    
    # Century categories
    for century, artists in century_artists.items():
        if len(artists) >= 10:
            recommendations.append((f"Century {century}", len(artists), "🟢"))
        elif len(artists) >= 5:
            recommendations.append((f"Century {century}", len(artists), "🟡"))
    
    # Period categories
    for period, artists in period_artists.items():
        if len(artists) >= 10:
            recommendations.append((period, len(artists), "🟢"))
        elif len(artists) >= 5:
            recommendations.append((period, len(artists), "🟡"))
    
    # Sort by artist count
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    for category, count, quality in recommendations:
        print(f"{quality} {category} ({count} artists)")

def main():
    check_gender_and_periods()

if __name__ == '__main__':
    main() 