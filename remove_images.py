#!/usr/bin/env python3
"""
Remove unwanted images from JSON files based on URLs in a text file.
Usage: python remove_images.py [--file urls_to_remove.txt] [--dry-run]
"""

import json
import argparse
import os
from typing import List, Dict, Any

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

def remove_images_by_url(data: List[Dict[str, Any]], urls_to_remove: List[str], dry_run: bool = False) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Remove images by URL and return cleaned data and removed items"""
    urls_set = set(urls_to_remove)
    cleaned_data = []
    removed_items = []
    
    for item in data:
        if item.get('url') in urls_set:
            removed_items.append(item)
            if not dry_run:
                print(f"Removing: {item.get('artist', 'Unknown')} - {item.get('title', 'Unknown')}")
        else:
            cleaned_data.append(item)
    
    return cleaned_data, removed_items

def main():
    parser = argparse.ArgumentParser(description='Remove unwanted images from JSON files')
    parser.add_argument('--file', default='urls_to_remove.txt', 
                       help='Text file containing URLs to remove (default: urls_to_remove.txt)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be removed without actually removing')
    parser.add_argument('--input', default='data/paintings_appended.json',
                       help='Input JSON file (default: data/paintings_appended.json)')
    parser.add_argument('--output', default='data/paintings_appended.json',
                       help='Output JSON file (default: same as input)')
    
    args = parser.parse_args()
    
    # Load URLs to remove
    urls_to_remove = load_urls_to_remove(args.file)
    if not urls_to_remove:
        print("No URLs to remove. Exiting.")
        return
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} items from {args.input}")
    
    # Remove images
    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
    
    cleaned_data, removed_items = remove_images_by_url(data, urls_to_remove, args.dry_run)
    
    # Report results
    print(f"\n📊 Removal Summary:")
    print(f"- Original items: {len(data):,}")
    print(f"- Items to remove: {len(removed_items):,}")
    print(f"- Remaining items: {len(cleaned_data):,}")
    
    if removed_items:
        print(f"\n🗑️ Items to be removed:")
        for item in removed_items[:10]:  # Show first 10
            print(f"  - {item.get('artist', 'Unknown')}: {item.get('title', 'Unknown')}")
        if len(removed_items) > 10:
            print(f"  ... and {len(removed_items) - 10} more")
    
    # Save if not dry run
    if not args.dry_run and removed_items:
        print(f"\n💾 Saving cleaned data to {args.output}...")
        save_json(cleaned_data, args.output)
        print(f"✅ Successfully removed {len(removed_items)} items")
        
        # Also clean merged file if it exists
        merged_file = 'data/paintings_merged.json'
        if os.path.exists(merged_file):
            print(f"Cleaning merged file {merged_file}...")
            merged_data = load_json(merged_file)
            if merged_data:
                cleaned_merged, removed_merged = remove_images_by_url(merged_data, urls_to_remove)
                if removed_merged:
                    save_json(cleaned_merged, merged_file)
                    print(f"✅ Removed {len(removed_merged)} items from merged file")
    elif args.dry_run:
        print(f"\n💡 Run without --dry-run to actually remove the items")

if __name__ == '__main__':
    main() 