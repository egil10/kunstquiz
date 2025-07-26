#!/usr/bin/env python3
"""
Enhanced Image Quality Filter for Norwegian Art Dataset

This script filters out low-quality images from the paintings dataset based on multiple criteria:
- Thumbnails and low-res previews
- Modern photographs (not paintings)
- Illustrations, sketches, and non-paintings
- Museum/catalog codes (often low-quality scans)
- Small dimensions
- Duplicates

The script is conservative - it only removes images that clearly match removal criteria.
"""

import json
import argparse
import os
import re
from urllib.parse import urlparse
from collections import defaultdict

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

def extract_dimensions_from_url(url, title=None):
    """
    Extract image dimensions from Wikimedia Commons URL or title.
    Returns (width, height) or (None, None) if not found.
    """
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
    """Check for museum/catalog codes that often indicate low-quality scans"""
    filename = os.path.basename(urlparse(url).path).lower()
    title_lower = title.lower() if title else ""
    
    # Only the most problematic museum/catalog code patterns
    # Removed b\d+ pattern as it's too aggressive
    code_patterns = [
        r'zkg\.2018-',  # Very specific problematic pattern
        r'athena_plus',  # Often low quality
        r'd000',        # Very specific problematic pattern
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, filename) or re.search(pattern, title_lower):
            return True, f"Museum/catalog code: {pattern}"
    
    return False, None

def check_modern_photograph(url, title):
    """Check if image appears to be a modern photograph rather than historical art"""
    filename = os.path.basename(urlparse(url).path).lower()
    title_lower = title.lower() if title else ""
    
    # Camera file indicators
    if 'img_' in filename:
        return True, "Modern camera photo (IMG_)"
    
    # Only very recent years (2020s) - exclude 18xx/19xx/20xx
    # This is more conservative - only flag very recent photos
    recent_years = re.findall(r'20[2-9][0-9]', filename + ' ' + title_lower)
    if recent_years:
        return True, f"Modern photo (year: {recent_years[0]})"
    
    # Only the most obvious photo keywords
    photo_keywords = [
        'norsk_portrettarkiv',  # Portrait archive - often photos
        '(cropped)'            # Edited photos
    ]
    
    for keyword in photo_keywords:
        if keyword in filename or keyword in title_lower:
            return True, f"Modern photo keyword: {keyword}"
    
    return False, None

def check_illustration_sketch(url, title):
    """Check if image is an illustration, sketch, or non-painting"""
    filename = os.path.basename(urlparse(url).path).lower()
    title_lower = title.lower() if title else ""
    
    # Only the most obvious non-painting content keywords
    non_painting_keywords = [
        'bamse'  # Cartoon bear - definitely not a painting
    ]
    
    for keyword in non_painting_keywords:
        if keyword in filename or keyword in title_lower:
            return True, f"Non-painting content: {keyword}"
    
    # Removed non-Norwegian artist check - too aggressive
    # Removed most illustration/sketch keywords - too broad
    
    return False, None

def check_small_dimensions(width, height, min_width=200, min_height=200):
    """Check if image dimensions are too small"""
    if width is None or height is None:
        return False, None  # Conservative - keep if dimensions unknown
    
    if width < min_width or height < min_height:
        return True, f"Small dimensions: {width}x{height} (min: {min_width}x{min_height})"
    
    return False, None

def check_duplicates(paintings):
    """Check for duplicate URLs"""
    seen_urls = set()
    duplicates = []
    
    for i, painting in enumerate(paintings):
        url = painting.get('url', '')
        if url in seen_urls:
            duplicates.append(i)
        else:
            seen_urls.add(url)
    
    return duplicates

def analyze_painting(painting, min_width=200, min_height=200):
    """
    Analyze a single painting and determine if it should be removed.
    Returns (should_remove, reasons)
    """
    url = painting.get('url', '')
    title = painting.get('title', '')
    reasons = []
    
    # Check each removal criterion
    checks = [
        check_thumbnail_lowres(url),
        check_modern_photograph(url, title),
        check_illustration_sketch(url, title),
        check_museum_catalog_codes(url, title),
        check_small_dimensions(*extract_dimensions_from_url(url, title), min_width, min_height)
    ]
    
    for should_remove, reason in checks:
        if should_remove and reason:
            reasons.append(reason)
    
    return len(reasons) > 0, reasons

def filter_paintings(paintings, min_width=200, min_height=200, dry_run=False):
    """
    Filter paintings based on quality criteria.
    Returns (filtered_paintings, removed_count, removal_stats, removed_details)
    """
    filtered_paintings = []
    removed_count = 0
    removal_stats = defaultdict(int)
    removed_details = []
    
    # Check for duplicates first
    duplicate_indices = check_duplicates(paintings)
    seen_urls = set()
    
    for i, painting in enumerate(paintings):
        url = painting.get('url', '')
        
        # Check for duplicates
        if url in seen_urls:
            removed_count += 1
            removal_stats['duplicates'] += 1
            removed_details.append({
                'title': painting.get('title', 'Unknown'),
                'artist': painting.get('artist', 'Unknown'),
                'url': url,
                'reasons': ['Duplicate URL']
            })
            if not dry_run:
                continue
        else:
            seen_urls.add(url)
        
        # Check other quality criteria
        should_remove, reasons = analyze_painting(painting, min_width, min_height)
        
        if should_remove:
            removed_count += 1
            for reason in reasons:
                removal_stats[reason] += 1
            
            removed_details.append({
                'title': painting.get('title', 'Unknown'),
                'artist': painting.get('artist', 'Unknown'),
                'url': url,
                'reasons': reasons
            })
            if not dry_run:
                continue
        
        filtered_paintings.append(painting)
    
    return filtered_paintings, removed_count, removal_stats, removed_details

def main():
    parser = argparse.ArgumentParser(description='Enhanced image quality filter for Norwegian art dataset')
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
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed removal reasons')
    
    args = parser.parse_args()
    
    # Load paintings
    paintings = load_json(args.input)
    if paintings is None:
        return
    
    print(f"📊 Loaded {len(paintings)} paintings from {args.input}")
    
    # Filter paintings
    filtered_paintings, removed_count, removal_stats, removed_details = filter_paintings(
        paintings, args.min_width, args.min_height, args.dry_run
    )
    
    # Show results
    print(f"\n🔍 Enhanced Image Quality Filter Results:")
    print(f"   Minimum dimensions: {args.min_width}x{args.min_height} pixels")
    print(f"   Original paintings: {len(paintings)}")
    print(f"   Remaining paintings: {len(filtered_paintings)}")
    print(f"   Removed paintings: {removed_count}")
    
    if removed_count > 0:
        print(f"\n📊 Removal Statistics:")
        for reason, count in sorted(removal_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   {reason}: {count}")
        
        if args.verbose:
            print(f"\n🗑️  Removed paintings (first 10):")
            for i, detail in enumerate(removed_details[:10]):
                print(f"   {i+1}. {detail['title']} by {detail['artist']}")
                for reason in detail['reasons']:
                    print(f"      - {reason}")
                print()
            
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
                    filtered_appended, removed_appended, _, _ = filter_paintings(
                        appended_paintings, args.min_width, args.min_height, False
                    )
                    if save_json(filtered_appended, appended_file):
                        print(f"✅ Also cleaned {appended_file}: {len(appended_paintings)} → {len(filtered_appended)} paintings")
    else:
        print(f"\n🔍 DRY RUN - No changes made")

if __name__ == '__main__':
    main() 