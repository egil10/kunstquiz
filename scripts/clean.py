#!/usr/bin/env python3
"""
Kunstquiz Data Cleanup Script
=============================

Consolidated script for all data cleanup operations.

USAGE EXAMPLES:
==============

# Remove duplicates by URL (most reliable)
python scripts/clean.py --duplicates --strategy url

# Remove duplicates by title (same painting, different URLs)
python scripts/clean.py --duplicates --strategy title

# Remove duplicates by exact match (artist + title + URL)
python scripts/clean.py --duplicates --strategy exact --keep-self-portraits

# Remove all paintings by a specific artist
python scripts/clean.py --artist "Artist Name" --no-dry-run

# Remove images by URL list
python scripts/clean.py --urls --file urls_to_remove.txt

# Remove small/low-quality images
python scripts/clean.py --quality --min-width 200 --min-height 200

# Remove TIF files automatically
python scripts/clean.py --tif

# Check for duplicates without removing
python scripts/clean.py --check-duplicates

# Full cleanup workflow
python scripts/clean.py --full-cleanup --no-dry-run

ARGUMENTS:
==========
--duplicates: Remove duplicate paintings
--artist: Remove paintings by specific artist
--urls: Remove paintings by URL list
--quality: Remove low-quality images
--tif: Remove TIF files
--check-duplicates: Check for duplicates without removing
--full-cleanup: Run all cleanup operations

--strategy: Duplicate detection strategy (url|title|exact)
--keep-self-portraits: Keep self-portraits when removing duplicates
--min-width: Minimum image width for quality filter
--min-height: Minimum image height for quality filter
--file: File containing URLs to remove
--input: Input JSON file (default: data/paintings.json)
--output: Output JSON file (default: same as input)
--dry-run: Show what would be removed without actually removing
--no-dry-run: Actually perform the removal
"""

import json
import argparse
import os
import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from urllib.parse import urlparse

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

def is_self_portrait(item: Dict[str, Any]) -> bool:
    """Check if an item is likely a self-portrait"""
    title = item.get('title', '').lower()
    artist = item.get('artist', '').lower()
    
    # Common self-portrait indicators
    self_portrait_indicators = [
        'self-portrait', 'self portrait', 'selvportrett', 'selv portrett',
        'autoportret', 'auto-portrait', 'selfie', 'selv'
    ]
    
    # Check if title contains self-portrait indicators
    for indicator in self_portrait_indicators:
        if indicator in title:
            return True
    
    # Check if artist name appears in title (common for self-portraits)
    if artist and len(artist.split()) >= 2:  # At least first and last name
        artist_parts = artist.split()
        if any(part in title for part in artist_parts):
            return True
    
    return False

def find_duplicates(data: List[Dict[str, Any]], strategy: str = 'url', keep_self_portraits: bool = False) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict]:
    """Find duplicates based on the specified strategy."""
    if strategy == 'url':
        # Group by URL
        groups = defaultdict(list)
        for item in data:
            url = item.get('url', '')
            if url:
                groups[url].append(item)
    
    elif strategy == 'title':
        # Group by title (case-insensitive)
        groups = defaultdict(list)
        for item in data:
            title = item.get('title', '').strip().lower()
            if title:
                groups[title].append(item)
    
    elif strategy == 'exact':
        # Group by (artist, title, url) combination
        groups = defaultdict(list)
        for item in data:
            key = (item.get('artist', ''), item.get('title', ''), item.get('url', ''))
            groups[key].append(item)
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    # Find groups with duplicates
    duplicate_groups = {key: items for key, items in groups.items() if len(items) > 1}
    
    cleaned_data = []
    removed_items = []
    
    for key, items in groups.items():
        if len(items) == 1:
            # No duplicates, keep the item
            cleaned_data.append(items[0])
        else:
            # Has duplicates
            if keep_self_portraits:
                # Separate self-portraits from other duplicates
                self_portraits = [item for item in items if is_self_portrait(item)]
                other_items = [item for item in items if not is_self_portrait(item)]
                
                # Keep all self-portraits
                cleaned_data.extend(self_portraits)
                
                # For other items, keep the first one
                if other_items:
                    cleaned_data.append(other_items[0])
                    removed_items.extend(other_items[1:])
            else:
                # Keep the first item, remove the rest
                cleaned_data.append(items[0])
                removed_items.extend(items[1:])
    
    return cleaned_data, removed_items, duplicate_groups

def remove_artist_paintings(data: List[Dict[str, Any]], artist_name: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Remove all paintings by a specific artist."""
    removed_items = []
    cleaned_data = []
    
    for item in data:
        if item.get('artist', '').strip().lower() == artist_name.strip().lower():
            removed_items.append(item)
        else:
            cleaned_data.append(item)
    
    return cleaned_data, removed_items

def load_urls_to_remove(filepath: str) -> List[str]:
    """Load URLs to remove from text file, ignoring comments and empty lines"""
    urls = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                # Skip section headers (lines without http)
                if not line.startswith('http'):
                    continue
                urls.append(line)
        print(f"Loaded {len(urls)} URLs to remove from {filepath}")
    except FileNotFoundError:
        print(f"ERROR: {filepath} not found.")
    return urls

def remove_images_by_url(data: List[Dict[str, Any]], urls_to_remove: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Remove images by URL and return cleaned data and removed items"""
    urls_set = set(urls_to_remove)
    cleaned_data = []
    removed_items = []
    
    for item in data:
        url = item.get('url', '')
        
        # Remove if URL is in the removal list OR if it's a TIF file
        if url in urls_set or url.lower().endswith('.tif') or url.lower().endswith('.tiff'):
            removed_items.append(item)
        else:
            cleaned_data.append(item)
    
    return cleaned_data, removed_items

def extract_dimensions_from_url(url, title=None):
    """Extract image dimensions from Wikimedia Commons URL or title."""
    try:
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

def check_thumbnail_lowres(url):
    """Check if URL is a thumbnail or low-res preview"""
    if '/thumb/' in url:
        # Check for pixel size patterns like /120px-, /250px-
        if re.search(r'/\d+px-', url):
            return True, "Thumbnail/low-res preview"
    return False, None

def check_museum_catalog_codes(url, title):
    """Check if URL/title contains museum catalog codes"""
    catalog_patterns = [
        r'NMK\.[A-Z]\d+',  # National Museum codes
        r'NG\.[A-Z]\d+',   # National Gallery codes
        r'IN\.\d+',        # Inventory numbers
        r'Cat\.\d+',       # Catalog numbers
        r'Inv\.\d+',       # Inventory numbers
    ]
    
    for pattern in catalog_patterns:
        if re.search(pattern, url, re.IGNORECASE) or re.search(pattern, title, re.IGNORECASE):
            return True, "Museum catalog code"
    return False, None

def check_modern_photograph(url, title):
    """Check if this is a modern photograph rather than a painting"""
    photo_indicators = [
        'photograph', 'photo', 'fotografi', 'foto',
        'digital', 'scan', 'scanned', 'digitized',
        'camera', 'lens', 'aperture', 'shutter'
    ]
    
    combined_text = (url + ' ' + title).lower()
    for indicator in photo_indicators:
        if indicator in combined_text:
            return True, "Modern photograph"
    return False, None

def check_illustration_sketch(url, title):
    """Check if this is an illustration or sketch rather than a painting"""
    sketch_indicators = [
        'sketch', 'drawing', 'illustration', 'skisse', 'tegning',
        'pencil', 'charcoal', 'ink', 'pen', 'crayon',
        'watercolor', 'watercolour', 'gouache'
    ]
    
    combined_text = (url + ' ' + title).lower()
    for indicator in sketch_indicators:
        if indicator in combined_text:
            return True, "Illustration/sketch"
    return False, None

def check_small_dimensions(width, height, min_width=200, min_height=200):
    """Check if image dimensions are too small"""
    if width and height:
        if width < min_width or height < min_height:
            return True, f"Small dimensions ({width}x{height})"
    return False, None

def analyze_painting(painting, min_width=200, min_height=200):
    """Analyze a painting for quality issues"""
    url = painting.get('url', '')
    title = painting.get('title', '')
    
    issues = []
    
    # Check for thumbnails/low-res
    is_thumb, reason = check_thumbnail_lowres(url)
    if is_thumb:
        issues.append(reason)
    
    # Check for museum catalog codes
    is_catalog, reason = check_museum_catalog_codes(url, title)
    if is_catalog:
        issues.append(reason)
    
    # Check for modern photographs
    is_photo, reason = check_modern_photograph(url, title)
    if is_photo:
        issues.append(reason)
    
    # Check for illustrations/sketches
    is_sketch, reason = check_illustration_sketch(url, title)
    if is_sketch:
        issues.append(reason)
    
    # Check dimensions
    width, height = extract_dimensions_from_url(url, title)
    is_small, reason = check_small_dimensions(width, height, min_width, min_height)
    if is_small:
        issues.append(reason)
    
    return issues

def filter_paintings(data: List[Dict[str, Any]], min_width=200, min_height=200) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Filter paintings based on quality criteria"""
    cleaned_data = []
    removed_items = []
    
    for painting in data:
        issues = analyze_painting(painting, min_width, min_height)
        
        if issues:
            removed_items.append({
                'painting': painting,
                'issues': issues
            })
        else:
            cleaned_data.append(painting)
    
    return cleaned_data, removed_items

def check_duplicates_simple(data: List[Dict[str, Any]]):
    """Simple duplicate checking without removal"""
    print(f'Total paintings: {len(data)}')
    
    # Check for duplicates based on (artist, title, url)
    unique_combinations = set()
    duplicates = 0
    duplicate_details = []
    
    for i, painting in enumerate(data):
        key = (painting.get('artist', ''), painting.get('title', ''), painting.get('url', ''))
        if key in unique_combinations:
            duplicates += 1
            duplicate_details.append({
                'index': i,
                'artist': painting.get('artist', ''),
                'title': painting.get('title', ''),
                'url': painting.get('url', '')
            })
        unique_combinations.add(key)
    
    print(f'Unique paintings: {len(unique_combinations)}')
    print(f'Duplicates found: {duplicates}')
    
    # Check for duplicates based on just URL
    url_counts = {}
    for painting in data:
        url = painting.get('url', '')
        if url:
            url_counts[url] = url_counts.get(url, 0) + 1
    
    url_duplicates = {url: count for url, count in url_counts.items() if count > 1}
    print(f'URL duplicates: {len(url_duplicates)}')
    
    if url_duplicates:
        print('\nSample URL duplicates:')
        for url, count in list(url_duplicates.items())[:5]:
            print(f'  {url}: {count} times')
    
    # Check for duplicates based on just title
    title_counts = {}
    for painting in data:
        title = painting.get('title', '')
        if title:
            title_counts[title] = title_counts.get(title, 0) + 1
    
    title_duplicates = {title: count for title, count in title_counts.items() if count > 1}
    print(f'\nTitle duplicates: {len(title_duplicates)}')
    
    if title_duplicates:
        print('\nSample title duplicates:')
        for title, count in list(title_duplicates.items())[:5]:
            print(f'  "{title}": {count} times')
    
    # Show some sample duplicates
    if duplicate_details:
        print('\nSample duplicate entries:')
        for dup in duplicate_details[:3]:
            print(f'  Index {dup["index"]}: {dup["artist"]} - "{dup["title"]}"')

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Data Cleanup Script')
    
    # Operation flags
    parser.add_argument('--duplicates', action='store_true', help='Remove duplicate paintings')
    parser.add_argument('--artist', type=str, help='Remove paintings by specific artist')
    parser.add_argument('--urls', action='store_true', help='Remove paintings by URL list')
    parser.add_argument('--quality', action='store_true', help='Remove low-quality images')
    parser.add_argument('--tif', action='store_true', help='Remove TIF files')
    parser.add_argument('--check-duplicates', action='store_true', help='Check for duplicates without removing')
    parser.add_argument('--full-cleanup', action='store_true', help='Run all cleanup operations')
    
    # Options
    parser.add_argument('--strategy', choices=['url', 'title', 'exact'], default='url',
                       help='Duplicate detection strategy (default: url)')
    parser.add_argument('--keep-self-portraits', action='store_true',
                       help='Keep self-portraits when removing duplicates')
    parser.add_argument('--min-width', type=int, default=200,
                       help='Minimum image width for quality filter (default: 200)')
    parser.add_argument('--min-height', type=int, default=200,
                       help='Minimum image height for quality filter (default: 200)')
    parser.add_argument('--file', default='urls_to_remove.txt',
                       help='File containing URLs to remove (default: urls_to_remove.txt)')
    parser.add_argument('--input', default='data/paintings.json',
                       help='Input JSON file (default: data/paintings.json)')
    parser.add_argument('--output', default=None,
                       help='Output JSON file (default: same as input)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Show what would be removed without actually removing (default)')
    parser.add_argument('--no-dry-run', action='store_true',
                       help='Actually perform the removal')
    
    args = parser.parse_args()
    
    # Set output file
    if args.output is None:
        args.output = args.input
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} items from {args.input}")
    
    # Check for duplicates only
    if args.check_duplicates:
        check_duplicates_simple(data)
        return
    
    # Determine if this is a dry run
    dry_run = args.dry_run and not args.no_dry_run
    
    if dry_run:
        print("\nDRY RUN - No changes will be made")
    
    total_removed = 0
    
    # Remove duplicates
    if args.duplicates or args.full_cleanup:
        print(f"\nRemoving duplicates (strategy: {args.strategy})...")
        cleaned_data, removed_items, duplicate_groups = find_duplicates(
            data, args.strategy, args.keep_self_portraits
        )
        
        print(f"Found {len(duplicate_groups)} duplicate groups")
        print(f"Would remove {len(removed_items)} duplicate items")
        
        if not dry_run:
            data = cleaned_data
            total_removed += len(removed_items)
            print(f"Removed {len(removed_items)} duplicates")
    
    # Remove by artist
    if args.artist:
        print(f"\nRemoving paintings by artist: '{args.artist}'")
        cleaned_data, removed_items = remove_artist_paintings(data, args.artist)
        
        print(f"Found {len(removed_items)} paintings by '{args.artist}'")
        
        if not dry_run:
            data = cleaned_data
            total_removed += len(removed_items)
            print(f"Removed {len(removed_items)} paintings by '{args.artist}'")
    
    # Remove by URLs
    if args.urls or args.full_cleanup:
        print(f"\nRemoving images by URL list...")
        urls_to_remove = load_urls_to_remove(args.file)
        if urls_to_remove:
            cleaned_data, removed_items = remove_images_by_url(data, urls_to_remove)
            
            print(f"Would remove {len(removed_items)} items by URL")
            
            if not dry_run:
                data = cleaned_data
                total_removed += len(removed_items)
                print(f"Removed {len(removed_items)} items by URL")
    
    # Remove TIF files
    if args.tif:
        print(f"\nRemoving TIF files...")
        urls_to_remove = []  # Empty list, but TIF removal is built into remove_images_by_url
        cleaned_data, removed_items = remove_images_by_url(data, urls_to_remove)
        
        print(f"Would remove {len(removed_items)} TIF files")
        
        if not dry_run:
            data = cleaned_data
            total_removed += len(removed_items)
            print(f"Removed {len(removed_items)} TIF files")
    
    # Remove low-quality images
    if args.quality or args.full_cleanup:
        print(f"\nRemoving low-quality images (min: {args.min_width}x{args.min_height})...")
        cleaned_data, removed_items = filter_paintings(data, args.min_width, args.min_height)
        
        print(f"Would remove {len(removed_items)} low-quality items")
        
        if not dry_run:
            data = cleaned_data
            total_removed += len(removed_items)
            print(f"Removed {len(removed_items)} low-quality items")
    
    # Save results
    if not dry_run and total_removed > 0:
        print(f"\nSaving cleaned data to {args.output}...")
        save_json(data, args.output)
        
        # Also update merged file if it exists
        merged_file = 'data/paintings.json'
        if os.path.exists(merged_file) and args.output != merged_file:
            print(f"Also updating {merged_file}...")
            save_json(data, merged_file)
        
        print(f"Cleanup complete! Removed {total_removed} items total")
        print(f"Remaining items: {len(data)}")
    elif dry_run:
        print(f"\nDRY RUN SUMMARY:")
        print(f"Would remove approximately {total_removed} items total")
        print(f"Would have {len(data)} items remaining")
        print("\nTo actually perform the cleanup, run with --no-dry-run")
    else:
        print("\nNo cleanup operations specified or no items to remove")

if __name__ == '__main__':
    main() 