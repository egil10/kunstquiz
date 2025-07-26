#!/usr/bin/env python3
"""
Remove paintings with small images from JSON files.

This script filters out paintings where the image dimensions are too small,
which helps remove stamps, thumbnails, and other tiny images that aren't
suitable for the quiz.
"""

import json
import argparse
import os
from urllib.parse import urlparse

def load_json(filepath):
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        return None

def save_json(data, filepath):
    """Save JSON file with error handling"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"ERROR: Could not save {filepath}: {e}")
        return False

def extract_dimensions_from_url(url):
    """
    Extract image dimensions from Wikimedia Commons URL.
    Returns (width, height) or (None, None) if not found.
    """
    try:
        # Parse the URL to get the filename
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        # Look for dimensions in the filename
        # Common patterns: filename_123x456.jpg, filename-123x456.jpg
        import re
        
        # Pattern for dimensions like 123x456 or 123×456 (with × symbol)
        dimension_patterns = [
            r'_(\d+)x(\d+)\.',  # underscore separator
            r'-(\d+)x(\d+)\.',  # dash separator
            r'_(\d+)×(\d+)\.',  # underscore with × symbol
            r'-(\d+)×(\d+)\.',  # dash with × symbol
        ]
        
        for pattern in dimension_patterns:
            match = re.search(pattern, filename)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                return width, height
        
        return None, None
    except Exception:
        return None, None

def is_small_image(width, height, min_width=200, min_height=200):
    """
    Check if image is too small.
    Returns True if image should be removed.
    """
    if width is None or height is None:
        # If we can't determine dimensions, keep the image
        return False
    
    return width < min_width or height < min_height

def remove_small_images(paintings, min_width=200, min_height=200, dry_run=False):
    """
    Remove paintings with small images.
    Returns (filtered_paintings, removed_count, removed_details)
    """
    filtered_paintings = []
    removed_count = 0
    removed_details = []
    
    for painting in paintings:
        url = painting.get('url', '')
        width, height = extract_dimensions_from_url(url)
        
        if is_small_image(width, height, min_width, min_height):
            removed_count += 1
            removed_details.append({
                'title': painting.get('title', 'Unknown'),
                'artist': painting.get('artist', 'Unknown'),
                'url': url,
                'dimensions': f"{width}x{height}" if width and height else "unknown"
            })
            if not dry_run:
                continue
        
        filtered_paintings.append(painting)
    
    return filtered_paintings, removed_count, removed_details

def main():
    parser = argparse.ArgumentParser(description='Remove paintings with small images from JSON files')
    parser.add_argument('--input', default='data/paintings_merged.json', 
                       help='Input JSON file (default: data/paintings_merged.json)')
    parser.add_argument('--output', default='data/paintings_merged.json',
                       help='Output JSON file (default: data/paintings_merged.json)')
    parser.add_argument('--min-width', type=int, default=200,
                       help='Minimum image width in pixels (default: 200)')
    parser.add_argument('--min-height', type=int, default=200,
                       help='Minimum image height in pixels (default: 200)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be removed without making changes')
    parser.add_argument('--clean-both', action='store_true',
                       help='Also clean paintings_appended.json')
    
    args = parser.parse_args()
    
    # Load paintings
    paintings = load_json(args.input)
    if paintings is None:
        return
    
    print(f"📊 Loaded {len(paintings)} paintings from {args.input}")
    
    # Remove small images
    filtered_paintings, removed_count, removed_details = remove_small_images(
        paintings, args.min_width, args.min_height, args.dry_run
    )
    
    # Show results
    print(f"\n🔍 Image Size Filter Results:")
    print(f"   Minimum dimensions: {args.min_width}x{args.min_height} pixels")
    print(f"   Original paintings: {len(paintings)}")
    print(f"   Remaining paintings: {len(filtered_paintings)}")
    print(f"   Removed paintings: {removed_count}")
    
    if removed_count > 0:
        print(f"\n🗑️  Removed paintings (first 10):")
        for i, detail in enumerate(removed_details[:10]):
            print(f"   {i+1}. {detail['title']} by {detail['artist']} ({detail['dimensions']})")
        
        if len(removed_details) > 10:
            print(f"   ... and {len(removed_details) - 10} more")
    
    # Save if not dry run
    if not args.dry_run:
        if save_json(filtered_paintings, args.output):
            print(f"\n✅ Saved {len(filtered_paintings)} paintings to {args.output}")
        
        # Also clean appended file if requested
        if args.clean_both:
            appended_file = 'data/paintings_appended.json'
            if os.path.exists(appended_file):
                appended_paintings = load_json(appended_file)
                if appended_paintings:
                    filtered_appended, removed_appended, _ = remove_small_images(
                        appended_paintings, args.min_width, args.min_height, False
                    )
                    if save_json(filtered_appended, appended_file):
                        print(f"✅ Also cleaned {appended_file}: {len(appended_paintings)} → {len(filtered_appended)} paintings")
    else:
        print(f"\n🔍 DRY RUN - No changes made")

if __name__ == '__main__':
    main() 