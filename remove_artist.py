#!/usr/bin/env python3
"""
Remove all paintings by a specific artist from the dataset.

Usage:
python remove_artist.py "Artist Name"
"""

import json
import argparse
import os
from typing import List, Dict, Any

def remove_artist_paintings(artist_name: str, dry_run: bool = True) -> None:
    """
    Remove all paintings by the specified artist from the dataset.
    
    Args:
        artist_name: Name of the artist to remove
        dry_run: If True, only show what would be removed without actually removing
    """
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} paintings from {data_file}")
    
    # Find paintings by the artist
    removed_items = []
    cleaned_data = []
    
    for item in data:
        if item.get('artist', '').strip().lower() == artist_name.strip().lower():
            removed_items.append(item)
            if not dry_run:
                print(f"Removing: {item.get('artist', 'Unknown')} - {item.get('title', 'Unknown')}")
        else:
            cleaned_data.append(item)
    
    print(f"\nFound {len(removed_items)} paintings by '{artist_name}'")
    
    if dry_run:
        print("\nDRY RUN - No changes made. To actually remove, run with --no-dry-run")
        for item in removed_items:
            print(f"  - {item.get('title', 'Unknown')} ({item.get('url', 'No URL')})")
    else:
        # Save the cleaned data
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nRemoved {len(removed_items)} paintings by '{artist_name}'")
        print(f"Remaining paintings: {len(cleaned_data)}")
        
        # Also update the merged file if it exists
        merged_file = 'data/paintings_merged.json'
        if os.path.exists(merged_file):
            with open(merged_file, 'r', encoding='utf-8') as f:
                merged_data = json.load(f)
            
            # Remove from merged data too
            merged_cleaned = [item for item in merged_data 
                            if item.get('artist', '').strip().lower() != artist_name.strip().lower()]
            
            with open(merged_file, 'w', encoding='utf-8') as f:
                json.dump(merged_cleaned, f, ensure_ascii=False, indent=2)
            
            print(f"Also updated {merged_file}")

def main():
    parser = argparse.ArgumentParser(description='Remove all paintings by a specific artist')
    parser.add_argument('artist_name', help='Name of the artist to remove')
    parser.add_argument('--no-dry-run', action='store_true', 
                       help='Actually remove the paintings (default is dry run)')
    
    args = parser.parse_args()
    
    dry_run = not args.no_dry_run
    
    print(f"Artist to remove: '{args.artist_name}'")
    print(f"Dry run: {dry_run}")
    print("-" * 50)
    
    remove_artist_paintings(args.artist_name, dry_run)

if __name__ == '__main__':
    main() 