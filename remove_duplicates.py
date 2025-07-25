#!/usr/bin/env python3
"""
Remove duplicates from JSON files with smart detection options.
Usage: python remove_duplicates.py [--strategy url|title|exact] [--dry-run] [--keep-self-portraits]
"""

import json
import argparse
import os
from typing import List, Dict, Any, Tuple
from collections import defaultdict

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
    """
    Find duplicates based on the specified strategy.
    Returns: (cleaned_data, removed_items, duplicate_groups)
    """
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
                
                # For other items, keep the first one, remove the rest
                if other_items:
                    cleaned_data.append(other_items[0])
                    removed_items.extend(other_items[1:])
            else:
                # Keep the first item, remove the rest
                cleaned_data.append(items[0])
                removed_items.extend(items[1:])
    
    return cleaned_data, removed_items, duplicate_groups

def analyze_duplicates(duplicate_groups: Dict, strategy: str) -> None:
    """Analyze and display duplicate information"""
    print(f"\n🔍 Duplicate Analysis (Strategy: {strategy}):")
    
    total_duplicates = sum(len(items) - 1 for items in duplicate_groups.values())
    print(f"- Total duplicate groups: {len(duplicate_groups)}")
    print(f"- Total duplicate items: {total_duplicates}")
    
    if duplicate_groups:
        print(f"\n📋 Sample duplicate groups:")
        for i, (key, items) in enumerate(list(duplicate_groups.items())[:5]):
            print(f"\nGroup {i+1} ({len(items)} items):")
            if strategy == 'url':
                print(f"  URL: {key}")
            elif strategy == 'title':
                print(f"  Title: '{key}'")
            elif strategy == 'exact':
                artist, title, url = key
                print(f"  Artist: {artist}")
                print(f"  Title: '{title}'")
                print(f"  URL: {url}")
            
            for j, item in enumerate(items):
                artist = item.get('artist', 'Unknown')
                title = item.get('title', 'Unknown')
                is_sp = " (self-portrait)" if is_self_portrait(item) else ""
                print(f"    {j+1}. {artist}: {title}{is_sp}")

def main():
    parser = argparse.ArgumentParser(description='Remove duplicates from JSON files')
    parser.add_argument('--strategy', choices=['url', 'title', 'exact'], default='url',
                       help='Duplicate detection strategy: url, title, or exact (artist+title+url)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be removed without actually removing')
    parser.add_argument('--keep-self-portraits', action='store_true',
                       help='Keep all self-portraits even if they are duplicates')
    parser.add_argument('--input', default='data/paintings_appended.json',
                       help='Input JSON file (default: data/paintings_appended.json)')
    parser.add_argument('--output', default='data/paintings_appended.json',
                       help='Output JSON file (default: same as input)')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} items from {args.input}")
    
    # Find duplicates
    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
    
    cleaned_data, removed_items, duplicate_groups = find_duplicates(
        data, args.strategy, args.keep_self_portraits
    )
    
    # Analyze duplicates
    analyze_duplicates(duplicate_groups, args.strategy)
    
    # Report results
    print(f"\n📊 Removal Summary:")
    print(f"- Original items: {len(data):,}")
    print(f"- Items to remove: {len(removed_items):,}")
    print(f"- Remaining items: {len(cleaned_data):,}")
    
    if removed_items:
        print(f"\n🗑️ Items to be removed:")
        for item in removed_items[:10]:  # Show first 10
            artist = item.get('artist', 'Unknown')
            title = item.get('title', 'Unknown')
            is_sp = " (self-portrait)" if is_self_portrait(item) else ""
            print(f"  - {artist}: {title}{is_sp}")
        if len(removed_items) > 10:
            print(f"  ... and {len(removed_items) - 10} more")
    
    # Save if not dry run
    if not args.dry_run and removed_items:
        print(f"\n💾 Saving cleaned data to {args.output}...")
        save_json(cleaned_data, args.output)
        print(f"✅ Successfully removed {len(removed_items)} duplicate items")
        
        # Also clean merged file if it exists
        merged_file = 'data/paintings_merged.json'
        if os.path.exists(merged_file):
            print(f"Cleaning merged file {merged_file}...")
            merged_data = load_json(merged_file)
            if merged_data:
                cleaned_merged, removed_merged, _ = find_duplicates(
                    merged_data, args.strategy, args.keep_self_portraits
                )
                if removed_merged:
                    save_json(cleaned_merged, merged_file)
                    print(f"✅ Removed {len(removed_merged)} duplicate items from merged file")
    elif args.dry_run:
        print(f"\n💡 Run without --dry-run to actually remove the duplicates")

if __name__ == '__main__':
    main() 