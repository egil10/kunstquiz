#!/usr/bin/env python3
"""
Kunstquiz Data Analysis Script
==============================

Consolidated script for all data analysis and statistics operations.

USAGE EXAMPLES:
==============

# Basic dataset statistics
python scripts/stats.py --basic

# Category statistics by painting count
python scripts/stats.py --categories

# Category statistics by artist count
python scripts/stats.py --categories --by-artists

# Century analysis
python scripts/stats.py --centuries

# Data structure analysis
python scripts/stats.py --structure

# Full comprehensive analysis
python scripts/stats.py --full

# Generate diagnostics report
python scripts/stats.py --diagnostics

# Check gender and period distribution
python scripts/stats.py --gender-periods

ARGUMENTS:
==========
--basic: Basic dataset statistics
--categories: Category statistics
--centuries: Century analysis
--structure: Data structure analysis
--full: Full comprehensive analysis
--diagnostics: Generate diagnostics report
--gender-periods: Check gender and period distribution

--by-artists: For categories, count by unique artists instead of paintings
--input: Input JSON file (default: data/paintings.json)
--output: Output report file (default: diagnostics.md)
"""

import json
import os
import re
from collections import Counter, defaultdict
import argparse
from typing import Dict, List, Any

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

def get_file_stats(filepath: str):
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

def extract_dimensions_from_url(url, title=None):
    """Extract image dimensions from Wikimedia Commons URL or title."""
    try:
        from urllib.parse import urlparse
        import os
        
        # Parse the URL to get the filename
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        # Look for dimensions in the filename
        dimension_patterns = [
            r'_(\d+)x(\d+)\.',  # underscore separator
            r'-(\d+)x(\d+)\.',  # dash separator
            r'_(\d+)×(\d+)\.',  # underscore with × symbol
            r'-(\d+)×(\d+)\.',  # dash with × symbol
            r'(\d+)x(\d+)\.',   # direct pattern
            r'(\d+)×(\d+)\.',   # direct pattern with × symbol
        ]
        
        for pattern in dimension_patterns:
            match = re.search(pattern, filename)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                return width, height
        
        # If not found in URL, check the title field
        if title:
            title_patterns = [
                r'(\d+)\s*×\s*(\d+);',  # "400 × 257; 53 KB"
                r'(\d+)\s*x\s*(\d+);',  # "400 x 257; 53 KB"
                r'(\d+)\s*×\s*(\d+)',   # "400 × 257" (no semicolon)
                r'(\d+)\s*x\s*(\d+)',   # "400 x 257" (no semicolon)
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, title)
                if match:
                    width = int(match.group(1))
                    height = int(match.group(2))
                    return width, height
        
        return None, None
    except Exception:
        return None, None

def analyze_image_sizes(paintings):
    """Analyze image dimensions and quality"""
    total_paintings = len(paintings)
    paintings_with_dimensions = 0
    small_images = 0
    medium_images = 0
    large_images = 0
    
    width_sum = 0
    height_sum = 0
    
    for painting in paintings:
        url = painting.get('url', '')
        title = painting.get('title', '')
        
        width, height = extract_dimensions_from_url(url, title)
        
        if width and height:
            paintings_with_dimensions += 1
            width_sum += width
            height_sum += height
            
            # Categorize by size
            if width < 200 or height < 200:
                small_images += 1
            elif width < 800 or height < 800:
                medium_images += 1
            else:
                large_images += 1
    
    avg_width = width_sum / paintings_with_dimensions if paintings_with_dimensions > 0 else 0
    avg_height = height_sum / paintings_with_dimensions if paintings_with_dimensions > 0 else 0
    
    return {
        'total': total_paintings,
        'with_dimensions': paintings_with_dimensions,
        'small': small_images,
        'medium': medium_images,
        'large': large_images,
        'avg_width': round(avg_width),
        'avg_height': round(avg_height),
        'dimension_coverage': round((paintings_with_dimensions / total_paintings) * 100, 1)
    }

def basic_stats(data: List[Dict[str, Any]]):
    """Generate basic dataset statistics"""
    print("📊 Basic Dataset Statistics")
    print("=" * 50)
    
    total_paintings = len(data)
    unique_artists = len(set(item.get('artist', '') for item in data if item.get('artist')))
    
    print(f"Total paintings: {total_paintings}")
    print(f"Unique artists: {unique_artists}")
    
    # Count by genre
    genre_counts = Counter()
    for item in data:
        genre = item.get('genre', 'Unknown')
        genre_counts[genre] += 1
    
    print(f"\n🎨 Genres by number of paintings:")
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (genre, count) in enumerate(sorted_genres, 1):
        percentage = (count / total_paintings) * 100
        print(f"{i:2d}. {genre:<20} {count:4d} paintings ({percentage:5.1f}%)")
    
    # Count by movement
    movement_counts = Counter()
    for item in data:
        movement = item.get('movement', 'Unknown')
        movement_counts[movement] += 1
    
    print(f"\n🎭 Art Movements by number of paintings:")
    sorted_movements = sorted(movement_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (movement, count) in enumerate(sorted_movements, 1):
        percentage = (count / total_paintings) * 100
        print(f"{i:2d}. {movement:<25} {count:4d} paintings ({percentage:5.1f}%)")
    
    # Top artists
    artist_counts = Counter()
    for item in data:
        artist = item.get('artist', 'Unknown')
        artist_counts[artist] += 1
    
    print(f"\n👨‍🎨 Top 10 artists by number of paintings:")
    sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (artist, count) in enumerate(sorted_artists[:10], 1):
        percentage = (count / total_paintings) * 100
        print(f"{i:2d}. {artist:<25} {count:4d} paintings ({percentage:5.1f}%)")

def category_stats(data: List[Dict[str, Any]], by_artists: bool = False):
    """Generate category statistics"""
    if by_artists:
        print("📊 Category Analysis by Artist Count")
        print("=" * 50)
        
        total_paintings = len(data)
        total_unique_artists = len(set(item.get('artist', '') for item in data if item.get('artist')))
        
        print(f"Total paintings: {total_paintings}")
        print(f"Total unique artists: {total_unique_artists}")
        print("-" * 60)
        
        # Define the categories we want to check
        categories = {
            'popular': 'Popular Painters (top 10 by painting count)',
            'landscape': 'Landscape',
            'realism': 'Realism',
            'expressionism': 'Expressionism', 
            'impressionism': 'Impressionism',
            'romantic_nationalism': 'Romantic Nationalism',
            'modernism': 'Modernism',
            'female_artists': 'Female Artists',
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
                    genres = item.get('genre', [])
                    artist_genres = item.get('artist_genre', [])
                    values = (genres if isinstance(genres, list) else [genres]) + (artist_genres if isinstance(artist_genres, list) else [artist_genres])
                    if any('landscape' in (g or '').lower() for g in values):
                        belongs_to_category = True
                elif category_key == 'realism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    if any('realism' in (m or '').lower() for m in values):
                        belongs_to_category = True
                elif category_key == 'expressionism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    if any('expressionism' in (m or '').lower() for m in values):
                        belongs_to_category = True
                elif category_key == 'impressionism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    if any('impressionism' in (m or '').lower() for m in values):
                        belongs_to_category = True
                elif category_key == 'romantic_nationalism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    synonyms = ['nasjonalromantikk', 'norwegian romantic nationalism', 'romantic nationalism', 'national romantic']
                    if any(any(s in (m or '').lower() for s in synonyms) for m in values):
                        belongs_to_category = True
                elif category_key == 'modernism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    bio_text = (item.get('artist_bio', '') or '')
                    if any('modernism' in (m or '').lower() for m in values) or ('modernist' in bio_text.lower()) or ('modernism' in bio_text.lower()):
                        belongs_to_category = True
                elif category_key == 'female_artists':
                    if item.get('artist_gender') == 'female':
                        belongs_to_category = True
                elif category_key == 'neo_romanticism':
                    movements = item.get('movement', [])
                    artist_movements = item.get('artist_movement', [])
                    values = (movements if isinstance(movements, list) else [movements]) + (artist_movements if isinstance(artist_movements, list) else [artist_movements])
                    if any('neo-romanticism' in (m or '').lower() for m in values):
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
        popular_paintings = [item for item in data if item.get('artist', '') in top_10_artists]
        popular_artists = set(top_10_artists)
        
        category_stats['popular'] = {
            'name': 'Popular Painters (top 10 by painting count)',
            'artists': len(popular_artists),
            'paintings': len(popular_paintings),
            'artist_list': list(popular_artists)
        }
        
        # Display results
        print("Category Analysis by Artist Count:")
        print()
        
        for category_key, stats in category_stats.items():
            print(f"• {stats['name']}:")
            print(f"  - Artists: {stats['artists']}")
            print(f"  - Paintings: {stats['paintings']}")
            if stats['artists'] <= 10:  # Show artist list if small
                print(f"  - Artists: {', '.join(stats['artist_list'])}")
            print()
    
    else:
        print("📊 Category Statistics by Painting Count")
        print("=" * 50)
        
        total_paintings = len(data)
        print(f"Total paintings: {total_paintings}")
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
            percentage = (count / total_paintings) * 100
            print(f"{i:2d}. {genre:<20} {count:4d} paintings ({percentage:5.1f}%)")
        
        print()
        print("🎭 Art Movements by number of paintings:")
        print()
        
        # Sort movements by count (descending)
        sorted_movements = sorted(movement_counts.items(), key=lambda x: x[1], reverse=True)
        
        for i, (movement, count) in enumerate(sorted_movements, 1):
            percentage = (count / total_paintings) * 100
            print(f"{i:2d}. {movement:<25} {count:4d} paintings ({percentage:5.1f}%)")
        
        print()
        print("🏷️  Categories (from categories list) by number of paintings:")
        print()
        
        # Sort categories by count (descending)
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        for i, (category, count) in enumerate(sorted_categories[:15], 1):  # Show top 15
            percentage = (count / total_paintings) * 100
            print(f"{i:2d}. {category:<25} {count:4d} paintings ({percentage:5.1f}%)")
        
        print()
        print("👨‍🎨 Top 10 artists by number of paintings:")
        print()
        
        # Sort artists by count (descending)
        sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)
        
        for i, (artist, count) in enumerate(sorted_artists[:10], 1):
            percentage = (count / total_paintings) * 100
            print(f"{i:2d}. {artist:<25} {count:4d} paintings ({percentage:5.1f}%)")

def century_analysis(data: List[Dict[str, Any]]):
    """Analyze century distribution"""
    print("📊 Century Analysis")
    print("=" * 50)
    
    total_paintings = len(data)
    print(f"Total paintings: {total_paintings}")
    print("-" * 50)
    
    # Count by century
    century_counts = Counter()
    year_counts = Counter()
    
    for item in data:
        century = item.get('century', 'Unknown')
        year = item.get('year', 'Unknown')
        
        century_counts[century] += 1
        year_counts[year] += 1
    
    print("📅 Centuries by number of paintings:")
    print()
    
    # Sort centuries by count (descending)
    sorted_centuries = sorted(century_counts.items(), key=lambda x: x[1], reverse=True)
    
    for century, count in sorted_centuries:
        percentage = (count / total_paintings) * 100
        print(f"• {century}: {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("📅 Year distribution (top 20):")
    print()
    
    # Sort years by count (descending)
    sorted_years = sorted(year_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (year, count) in enumerate(sorted_years[:20], 1):
        percentage = (count / total_paintings) * 100
        print(f"{i:2d}. {year}: {count:4d} paintings ({percentage:5.1f}%)")
    
    # Check for 18th, 19th, 20th century presence
    print()
    print("🔍 Century Coverage:")
    centuries_present = set(century_counts.keys())
    
    if '18' in centuries_present or '1800s' in centuries_present:
        print("✅ 18th century: Present")
    else:
        print("❌ 18th century: Missing")
    
    if '19' in centuries_present or '1900s' in centuries_present:
        print("✅ 19th century: Present")
    else:
        print("❌ 19th century: Missing")
    
    if '20' in centuries_present or '2000s' in centuries_present:
        print("✅ 20th century: Present")
    else:
        print("❌ 20th century: Missing")
    
    if '21' in centuries_present or '2100s' in centuries_present:
        print("✅ 21st century: Present")
    else:
        print("❌ 21st century: Missing")

def data_structure_analysis(data: List[Dict[str, Any]]):
    """Analyze data structure and field coverage"""
    print("📊 Data Structure Analysis")
    print("=" * 50)
    
    total_paintings = len(data)
    print(f"Total paintings: {total_paintings}")
    print("-" * 50)
    
    # Examine first few items
    print("🔍 First 3 items structure:")
    for i, item in enumerate(data[:3], 1):
        print(f"\nItem {i}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
    
    # Check what fields exist
    print(f"\n📋 All available fields in the dataset:")
    all_fields = set()
    for item in data:
        all_fields.update(item.keys())
    
    for field in sorted(all_fields):
        print(f"  • {field}")
    
    # Check for category-like fields
    print(f"\n🎨 Looking for category-related fields:")
    category_fields = [field for field in all_fields if 'category' in field.lower() or 'type' in field.lower() or 'genre' in field.lower()]
    
    if category_fields:
        for field in category_fields:
            unique_values = set()
            for item in data:
                value = item.get(field, '')
                if value:
                    unique_values.add(str(value))
            
            print(f"  • {field}: {len(unique_values)} unique values")
            if len(unique_values) <= 10:
                print(f"    Values: {sorted(unique_values)}")
    else:
        print("  No obvious category fields found!")
    
    # Check for any field that might contain category info
    print(f"\n🔍 Checking all fields for potential category data:")
    for field in sorted(all_fields):
        if field not in ['artist', 'title', 'url', 'year', 'image_url']:  # Skip obvious non-category fields
            unique_values = set()
            for item in data:
                value = item.get(field, '')
                if value and str(value).strip():
                    unique_values.add(str(value).strip())
            
            if 1 < len(unique_values) <= 20:  # Reasonable number for categories
                print(f"  • {field}: {len(unique_values)} values - {sorted(unique_values)}")

def gender_period_analysis(data: List[Dict[str, Any]]):
    """Analyze gender and period distribution"""
    print("📊 Gender and Period Analysis")
    print("=" * 50)
    
    total_paintings = len(data)
    print(f"Total paintings: {total_paintings}")
    print("-" * 50)
    
    # Load artist bios to get gender information
    bios_file = 'data/artists.json'
    artist_genders = {}
    
    if os.path.exists(bios_file):
        try:
            with open(bios_file, 'r', encoding='utf-8') as f:
                bios_data = json.load(f)
            
            for artist in bios_data:
                name = artist.get('name', '')
                gender = artist.get('gender', 'Unknown')
                if name:
                    artist_genders[name] = gender
            
            print(f"Loaded gender data for {len(artist_genders)} artists")
        except Exception as e:
            print(f"Error loading artist bios: {e}")
    else:
        print("Artist bios file not found")
    
    # Analyze gender distribution
    gender_counts = Counter()
    period_gender_counts = defaultdict(Counter)
    
    for item in data:
        artist = item.get('artist', '')
        century = item.get('century', 'Unknown')
        
        if artist in artist_genders:
            gender = artist_genders[artist]
            gender_counts[gender] += 1
            period_gender_counts[century][gender] += 1
        else:
            gender_counts['Unknown'] += 1
            period_gender_counts[century]['Unknown'] += 1
    
    print("\n👥 Gender Distribution:")
    for gender, count in gender_counts.most_common():
        percentage = (count / total_paintings) * 100
        print(f"• {gender}: {count} paintings ({percentage:.1f}%)")
    
    print("\n📅 Gender by Century:")
    for century in sorted(period_gender_counts.keys()):
        print(f"\n{century}:")
        total_in_century = sum(period_gender_counts[century].values())
        for gender, count in period_gender_counts[century].most_common():
            percentage = (count / total_in_century) * 100 if total_in_century > 0 else 0
            print(f"  • {gender}: {count} paintings ({percentage:.1f}%)")

def full_analysis(data: List[Dict[str, Any]]):
    """Run full comprehensive analysis"""
    print("🔍 FULL COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    # Basic stats
    basic_stats(data)
    print("\n" + "=" * 60 + "\n")
    
    # Category stats
    category_stats(data)
    print("\n" + "=" * 60 + "\n")
    
    # Century analysis
    century_analysis(data)
    print("\n" + "=" * 60 + "\n")
    
    # Data structure analysis
    data_structure_analysis(data)
    print("\n" + "=" * 60 + "\n")
    
    # Gender and period analysis
    gender_period_analysis(data)
    print("\n" + "=" * 60 + "\n")
    
    # Image quality analysis
    print("📸 Image Quality Analysis")
    print("=" * 50)
    image_stats = analyze_image_sizes(data)
    
    print(f"Total paintings: {image_stats['total']}")
    print(f"Paintings with dimensions: {image_stats['with_dimensions']} ({image_stats['dimension_coverage']}%)")
    print(f"Small images (<200px): {image_stats['small']}")
    print(f"Medium images (200-800px): {image_stats['medium']}")
    print(f"Large images (>800px): {image_stats['large']}")
    print(f"Average dimensions: {image_stats['avg_width']}x{image_stats['avg_height']}")

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Data Analysis Script')
    
    # Analysis types
    parser.add_argument('--basic', action='store_true', help='Basic dataset statistics')
    parser.add_argument('--categories', action='store_true', help='Category statistics')
    parser.add_argument('--centuries', action='store_true', help='Century analysis')
    parser.add_argument('--structure', action='store_true', help='Data structure analysis')
    parser.add_argument('--full', action='store_true', help='Full comprehensive analysis')
    parser.add_argument('--diagnostics', action='store_true', help='Generate diagnostics report')
    parser.add_argument('--gender-periods', action='store_true', help='Check gender and period distribution')
    
    # Options
    parser.add_argument('--by-artists', action='store_true', help='For categories, count by unique artists instead of paintings')
    parser.add_argument('--input', default='data/paintings.json', help='Input JSON file')
    parser.add_argument('--output', default='diagnostics.md', help='Output report file')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} items from {args.input}")
    print()
    
    # Run requested analyses
    if args.basic:
        basic_stats(data)
    
    if args.categories:
        category_stats(data, args.by_artists)
    
    if args.centuries:
        century_analysis(data)
    
    if args.structure:
        data_structure_analysis(data)
    
    if args.gender_periods:
        gender_period_analysis(data)
    
    if args.full:
        full_analysis(data)
    
    # If no specific analysis requested, run basic
    if not any([args.basic, args.categories, args.centuries, args.structure, args.full, args.gender_periods]):
        basic_stats(data)

if __name__ == '__main__':
    main() 