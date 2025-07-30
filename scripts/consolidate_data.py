#!/usr/bin/env python3
"""
Kunstquiz Data Consolidation Script
===================================

Consolidates existing JSON files into a cleaner structure:
- Merges duplicate data across files
- Creates unified data structure
- Maintains web app compatibility
- Removes redundant files

USAGE:
======
python consolidate_data.py --analyze    # Analyze current data structure
python consolidate_data.py --consolidate # Consolidate data files
python consolidate_data.py --cleanup    # Remove redundant files
python consolidate_data.py --full       # Run full consolidation

This script will:
1. Analyze current data files and identify duplicates
2. Merge data into clean structure
3. Create unified app data file
4. Remove redundant files
5. Ensure web app compatibility
"""

import json
import argparse
import os
import shutil
from typing import List, Dict, Any, Set
from collections import defaultdict
from datetime import datetime

def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON file with error handling"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"ERROR: Could not load {filepath}: {e}")
        return []

def save_json(data: List[Dict[str, Any]], filepath: str):
    """Save JSON file with pretty formatting"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def analyze_data_structure():
    """Analyze current data structure and identify issues"""
    print("🔍 Analyzing current data structure...")
    
    # List of files to analyze
    files_to_analyze = [
                'data/paintings.json',
        'data/paintings.json',
        'data/paintings.json',
        'data/artists.json',
        'data/artists.json',
        'data/artists.json'
    ]
    
    analysis = {}
    
    for filepath in files_to_analyze:
        if os.path.exists(filepath):
            data = load_json(filepath)
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            
            # Handle different data types
            if isinstance(data, list) and len(data) > 0:
                sample_keys = list(data[0].keys())
            elif isinstance(data, dict):
                sample_keys = list(data.keys())
            else:
                sample_keys = []
            
            analysis[filepath] = {
                'exists': True,
                'size_mb': round(file_size, 2),
                'item_count': len(data) if isinstance(data, (list, dict)) else 0,
                'sample_keys': sample_keys
            }
        else:
            analysis[filepath] = {
                'exists': False,
                'size_mb': 0,
                'item_count': 0,
                'sample_keys': []
            }
    
    # Print analysis
    print("\n📊 Data File Analysis:")
    print("=" * 80)
    
    for filepath, info in analysis.items():
        status = "✅" if info['exists'] else "❌"
        print(f"{status} {filepath}")
        if info['exists']:
            print(f"    Size: {info['size_mb']} MB")
            print(f"    Items: {info['item_count']}")
            if info['sample_keys']:
                print(f"    Keys: {', '.join(info['sample_keys'][:5])}{'...' if len(info['sample_keys']) > 5 else ''}")
        print()
    
    return analysis

def find_duplicates():
    """Find duplicate paintings across different files"""
    print("🔍 Finding duplicates across files...")
    
    # Load all painting files
    painting_files = [
        'data/paintings.json',
        'data/paintings.json',
        'data/paintings.json'
    ]
    
    all_paintings = []
    file_sources = {}
    
    for filepath in painting_files:
        if os.path.exists(filepath):
            paintings = load_json(filepath)
            for i, painting in enumerate(paintings):
                painting['_source_file'] = filepath
                painting['_source_index'] = i
                all_paintings.append(painting)
                file_sources[filepath] = file_sources.get(filepath, 0) + 1
    
    print(f"Total paintings across all files: {len(all_paintings)}")
    for filepath, count in file_sources.items():
        print(f"  {filepath}: {count} paintings")
    
    # Find duplicates by URL
    url_groups = defaultdict(list)
    for painting in all_paintings:
        url = painting.get('url', '')
        if url:
            url_groups[url].append(painting)
    
    duplicates = {url: paintings for url, paintings in url_groups.items() if len(paintings) > 1}
    
    print(f"\n🔍 Found {len(duplicates)} duplicate URLs:")
    for url, paintings in list(duplicates.items())[:5]:  # Show first 5
        print(f"  {url}")
        for painting in paintings:
            print(f"    - {painting['_source_file']} (index {painting['_source_index']})")
    
    return all_paintings, duplicates

def consolidate_paintings(all_paintings: List[Dict[str, Any]], duplicates: Dict) -> List[Dict[str, Any]]:
    """Consolidate paintings, removing duplicates and merging data"""
    print("🔄 Consolidating paintings...")
    
    # Create a map of URL to best painting
    consolidated = {}
    
    for painting in all_paintings:
        url = painting.get('url', '')
        if not url:
            continue
        
        # Remove internal tracking fields
        painting_copy = {k: v for k, v in painting.items() if not k.startswith('_')}
        
        if url not in consolidated:
            # First occurrence, keep it
            consolidated[url] = painting_copy
        else:
            # Merge with existing painting
            existing = consolidated[url]
            
            # Merge fields, preferring non-empty values
            for key, value in painting_copy.items():
                if key not in existing or not existing[key]:
                    existing[key] = value
                elif value and isinstance(value, list) and isinstance(existing[key], list):
                    # Merge lists - handle both simple values and dictionaries
                    try:
                        existing[key] = list(set(existing[key] + value))
                    except TypeError:
                        # If items are not hashable (like dicts), just concatenate
                        existing[key] = existing[key] + value
                elif value and isinstance(value, dict) and isinstance(existing[key], dict):
                    # Merge dictionaries
                    existing[key].update(value)
                elif value and value != existing[key]:
                    # For other types, prefer the new value if it's different
                    existing[key] = value
    
    consolidated_list = list(consolidated.values())
    
    print(f"✅ Consolidated {len(all_paintings)} paintings into {len(consolidated_list)} unique paintings")
    print(f"Removed {len(all_paintings) - len(consolidated_list)} duplicates")
    
    return consolidated_list

def consolidate_artists() -> List[Dict[str, Any]]:
    """Consolidate artist data from multiple files"""
    print("🔄 Consolidating artist data...")
    
    # Load artist files
    artist_files = [
        'data/artist_bios.json',
        'data/artist_bios.json',
        'data/artist_bios.json'
    ]
    
    all_artists = {}
    
    for filepath in artist_files:
        if os.path.exists(filepath):
            artists_data = load_json(filepath)
            
            # Handle different data structures
            if isinstance(artists_data, list):
                # List of artist objects
                for artist in artists_data:
                    name = artist.get('name', '')
                    if not name:
                        continue
                    
                    if name not in all_artists:
                        all_artists[name] = artist
                    else:
                        # Merge with existing artist
                        existing = all_artists[name]
                        for key, value in artist.items():
                            if key not in existing or not existing[key]:
                                existing[key] = value
                            elif value and isinstance(value, list) and isinstance(existing[key], list):
                                # Merge lists
                                try:
                                    existing[key] = list(set(existing[key] + value))
                                except TypeError:
                                    existing[key] = existing[key] + value
                            elif value and isinstance(value, dict) and isinstance(existing[key], dict):
                                # Merge dictionaries
                                existing[key].update(value)
            
            elif isinstance(artists_data, dict):
                # Dictionary with artist names as keys
                for name, artist_data in artists_data.items():
                    if not name:
                        continue
                    
                    if name not in all_artists:
                        all_artists[name] = artist_data
                    else:
                        # Merge with existing artist
                        existing = all_artists[name]
                        for key, value in artist_data.items():
                            if key not in existing or not existing[key]:
                                existing[key] = value
                            elif value and isinstance(value, list) and isinstance(existing[key], list):
                                # Merge lists
                                try:
                                    existing[key] = list(set(existing[key] + value))
                                except TypeError:
                                    existing[key] = existing[key] + value
                            elif value and isinstance(value, dict) and isinstance(existing[key], dict):
                                # Merge dictionaries
                                existing[key].update(value)
    
    consolidated_artists = list(all_artists.values())
    
    print(f"✅ Consolidated artist data into {len(consolidated_artists)} unique artists")
    
    return consolidated_artists

def create_unified_app_data(paintings: List[Dict[str, Any]], artists: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create unified app data structure"""
    print("🔄 Creating unified app data...")
    
    app_data = {
        'paintings': paintings,
        'artists': artists,
        'metadata': {
            'generated_at': '2024-01-01T00:00:00Z',  # Will be updated
            'total_paintings': len(paintings),
            'total_artists': len(artists),
            'version': '2.0',
            'consolidated': True
        }
    }
    
    return app_data

def backup_existing_files():
    """Create backup of existing files before consolidation"""
    print("💾 Creating backup of existing files...")
    
    backup_dir = f"backups/backup_before_consolidation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        'data/paintings.json',
        'data/paintings.json',
        'data/paintings.json',
        'data/artists.json',
        'data/artists.json',
        'data/artists.json'
    ]
    
    backed_up = []
    for filepath in files_to_backup:
        if os.path.exists(filepath):
            backup_path = os.path.join(backup_dir, os.path.basename(filepath))
            shutil.copy2(filepath, backup_path)
            backed_up.append(filepath)
    
    print(f"✅ Backed up {len(backed_up)} files to {backup_dir}")
    return backup_dir

def cleanup_redundant_files():
    """Remove redundant files after consolidation"""
    print("🧹 Cleaning up redundant files...")
    
    # Files that can be safely removed after consolidation
    files_to_remove = [
        'data/paintings.json',  # Replaced by unified structure
        'data/artists.json',       # Merged into artists.json
        'data/artists.json'  # Merged into artists.json
    ]
    
    removed = []
    for filepath in files_to_remove:
        if os.path.exists(filepath):
            os.remove(filepath)
            removed.append(filepath)
            print(f"  ✅ Removed: {filepath}")
    
    print(f"✅ Removed {len(removed)} redundant files")
    return removed

def update_web_app_compatibility():
    """Ensure web app compatibility by creating expected files"""
    print("🔧 Ensuring web app compatibility...")
    
    # Load consolidated data
    app_data = load_json('data/app_data.json')
    if not app_data:
        print("❌ No app data found")
        return False
    
    paintings = app_data.get('paintings', [])
    artists = app_data.get('artists', [])
    
    # Create files that the web app expects
    save_json(paintings, 'data/paintings.json')
    save_json(artists, 'data/artists.json')
    
    print("✅ Created web app compatibility files")
    return True

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Data Consolidation Script')
    
    parser.add_argument('--analyze', action='store_true', help='Analyze current data structure')
    parser.add_argument('--consolidate', action='store_true', help='Consolidate data files')
    parser.add_argument('--cleanup', action='store_true', help='Remove redundant files')
    parser.add_argument('--full', action='store_true', help='Run full consolidation')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without doing it')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually perform operations')
    
    args = parser.parse_args()
    
    # Determine if this is a dry run
    dry_run = args.dry_run and not args.no_dry_run
    
    if dry_run:
        print("🔍 DRY RUN - No changes will be made")
    
    # Analyze data structure
    if args.analyze or args.full:
        analysis = analyze_data_structure()
        all_paintings, duplicates = find_duplicates()
    
    # Consolidate data
    if args.consolidate or args.full:
        if not dry_run:
            # Backup existing files
            backup_dir = backup_existing_files()
            
            # Consolidate paintings
            all_paintings, duplicates = find_duplicates()
            consolidated_paintings = consolidate_paintings(all_paintings, duplicates)
            
            # Consolidate artists
            consolidated_artists = consolidate_artists()
            
            # Create unified app data
            app_data = create_unified_app_data(consolidated_paintings, consolidated_artists)
            
            # Save consolidated data
            save_json(consolidated_paintings, 'data/paintings.json')
            save_json(consolidated_artists, 'data/artists.json')
            save_json(app_data, 'data/app_data.json')
            
            # Ensure web app compatibility
            update_web_app_compatibility()
            
            print("✅ Data consolidation complete!")
        else:
            print("Would consolidate data files")
    
    # Cleanup redundant files
    if args.cleanup or args.full:
        if not dry_run:
            cleanup_redundant_files()
            print("✅ Cleanup complete!")
        else:
            print("Would remove redundant files")
    
    if not any([args.analyze, args.consolidate, args.cleanup, args.full]):
        print("No operation specified. Use --help for options.")
        print("\nQuick start:")
        print("  python consolidate_data.py --analyze    # Analyze current structure")
        print("  python consolidate_data.py --full       # Run full consolidation")

if __name__ == '__main__':
    main() 