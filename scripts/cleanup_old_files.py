#!/usr/bin/env python3
"""
Cleanup script to remove old redundant files after consolidation
"""

import os
import shutil
import glob

def cleanup_old_files():
    """Remove old redundant files and backup directories"""
    
    print("🧹 Cleaning up old files and directories...")
    
    # Files to remove (old consolidated scripts)
    old_scripts = [
        'apply_inferred_categories.py',
        'check_gender_periods.py', 
        'infer_movements.py',
        'analyze_artist_movements.py',
        'discover_categories.py',
        'category_artist_stats.py',
        'century_check.py',
        'category_stats.py',
        'debug_data_structure.py',
        'remove_artist.py',
        'remove_images.py',
        'remove_small_images.py',
        'fix_urls.py',
        'merge_artist_tags.py',
        'remove_duplicates.py',
        'collect_artist_tags.py',
        'check_urls.py',
        'check_duplicates.py'
    ]
    
    # Backup directories to remove
    backup_dirs = [
        'backup_20250726_180625',
        'backup_before_consolidation_20250730_202109',
        'backup_before_consolidation_20250730_202132', 
        'backup_before_consolidation_20250730_202213',
        'backup_before_consolidation_20250730_203247'
    ]
    
    # Old data files that are now redundant
    old_data_files = [
        'data/paintings_merged.json',  # Already removed by consolidate_data.py
        'data/artist_tags.json',       # Merged into artists.json
        'data/artist_tags_appended.json'  # Merged into artists.json
    ]
    
    # Other files to remove
    other_files = [
        'generate_favicon.html',
        'favicon.png',
        'favicon.ico'
    ]
    
    removed_files = []
    removed_dirs = []
    
    # Remove old scripts
    for script in old_scripts:
        if os.path.exists(script):
            os.remove(script)
            removed_files.append(script)
            print(f"  ✅ Removed: {script}")
    
    # Remove backup directories
    for backup_dir in backup_dirs:
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
            removed_dirs.append(backup_dir)
            print(f"  ✅ Removed directory: {backup_dir}")
    
    # Remove old data files
    for data_file in old_data_files:
        if os.path.exists(data_file):
            os.remove(data_file)
            removed_files.append(data_file)
            print(f"  ✅ Removed: {data_file}")
    
    # Remove other files
    for file in other_files:
        if os.path.exists(file):
            os.remove(file)
            removed_files.append(file)
            print(f"  ✅ Removed: {file}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"  - Removed {len(removed_files)} files")
    print(f"  - Removed {len(removed_dirs)} directories")
    
    # Show what's left
    print(f"\n📁 Current project structure:")
    current_files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
    current_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    print(f"  Files ({len(current_files)}): {', '.join(sorted(current_files))}")
    print(f"  Directories ({len(current_dirs)}): {', '.join(sorted(current_dirs))}")

if __name__ == '__main__':
    cleanup_old_files() 