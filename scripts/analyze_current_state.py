#!/usr/bin/env python3
"""
Quick Analysis of Current Kunstquiz State
=========================================

This script quickly analyzes the current state of your data and provides
recommendations for consolidation and improvement.

Run this to understand what needs to be done:
python analyze_current_state.py
"""

import json
import os
from collections import Counter, defaultdict

def analyze_files():
    """Analyze all data files"""
    print("🔍 Analyzing current data files...")
    print("=" * 60)
    
    files_to_check = [
        'data/paintings_appended.json',
        'data/paintings_merged.json',
        'data/paintings_with_inferred_categories.json',
        'data/artist_bios.json',
        'data/artist_tags.json',
        'data/artist_tags_appended.json'
    ]
    
    total_paintings = 0
    total_artists = 0
    file_info = {}
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                
                if 'paintings' in filepath:
                    total_paintings += len(data)
                    file_info[filepath] = {
                        'type': 'paintings',
                        'count': len(data),
                        'size_mb': round(file_size, 2),
                        'sample_keys': list(data[0].keys()) if data else []
                    }
                else:
                    total_artists += len(data)
                    file_info[filepath] = {
                        'type': 'artists',
                        'count': len(data),
                        'size_mb': round(file_size, 2),
                        'sample_keys': list(data[0].keys()) if data else []
                    }
                
                print(f"✅ {filepath}")
                print(f"   Type: {file_info[filepath]['type']}")
                print(f"   Count: {file_info[filepath]['count']}")
                print(f"   Size: {file_info[filepath]['size_mb']} MB")
                if file_info[filepath]['sample_keys']:
                    print(f"   Keys: {', '.join(file_info[filepath]['sample_keys'][:5])}{'...' if len(file_info[filepath]['sample_keys']) > 5 else ''}")
                print()
                
            except Exception as e:
                print(f"❌ {filepath} - Error: {e}")
        else:
            print(f"❌ {filepath} - Not found")
    
    print(f"📊 Summary:")
    print(f"   Total paintings across files: {total_paintings}")
    print(f"   Total artists across files: {total_artists}")
    
    return file_info

def check_duplicates():
    """Check for duplicates across painting files"""
    print("\n🔍 Checking for duplicates...")
    print("=" * 60)
    
    painting_files = [
        'data/paintings_appended.json',
        'data/paintings_merged.json',
        'data/paintings_with_inferred_categories.json'
    ]
    
    all_urls = []
    file_urls = {}
    
    for filepath in painting_files:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            urls = [item.get('url', '') for item in data if item.get('url')]
            file_urls[filepath] = set(urls)
            all_urls.extend(urls)
    
    # Count URL occurrences
    url_counts = Counter(all_urls)
    duplicates = {url: count for url, count in url_counts.items() if count > 1}
    
    print(f"Found {len(duplicates)} duplicate URLs across files")
    
    if duplicates:
        print("\nSample duplicates:")
        for url, count in list(duplicates.items())[:5]:
            print(f"  {url} (appears {count} times)")
    
    return len(duplicates)

def check_web_app_compatibility():
    """Check if current data structure works with web app"""
    print("\n🔧 Checking web app compatibility...")
    print("=" * 60)
    
    # Check if web app can load required files
    required_files = [
        'data/paintings_with_inferred_categories.json',
        'data/artist_bios.json'
    ]
    
    compatibility_issues = []
    
    for filepath in required_files:
        if not os.path.exists(filepath):
            compatibility_issues.append(f"Missing required file: {filepath}")
        else:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {filepath} - {len(data)} items")
            except Exception as e:
                compatibility_issues.append(f"Error reading {filepath}: {e}")
    
    if compatibility_issues:
        print("❌ Compatibility issues found:")
        for issue in compatibility_issues:
            print(f"  - {issue}")
    else:
        print("✅ Web app compatibility: OK")
    
    return len(compatibility_issues) == 0

def provide_recommendations():
    """Provide recommendations for improvement"""
    print("\n💡 Recommendations:")
    print("=" * 60)
    
    print("1. 🧹 CONSOLIDATE DATA:")
    print("   Run: python consolidate_data.py --analyze")
    print("   Then: python consolidate_data.py --full")
    print()
    
    print("2. 🚀 SETUP WORKFLOW:")
    print("   Run: python workflow.py --init")
    print("   Then: python workflow.py --quick")
    print()
    
    print("3. 📁 NEW DATA STRUCTURE:")
    print("   data/")
    print("   ├── raw/                    # Raw collected data")
    print("   │   ├── paintings_raw.json  # All collected paintings")
    print("   │   └── artists_raw.json    # All collected artist data")
    print("   ├── processed/              # Clean, processed data")
    print("   │   ├── paintings.json      # Single clean paintings file")
    print("   │   └── artists.json        # Single clean artists file")
    print("   ├── config/                 # Configuration files")
    print("   │   ├── urls_to_add.txt     # Manual URLs to collect")
    print("   │   └── urls_to_remove.txt  # Manual URLs to exclude")
    print("   └── app_data.json          # Unified app data")
    print()
    
    print("4. 🎯 BENEFITS:")
    print("   - No more duplicate data across files")
    print("   - Single source of truth for paintings and artists")
    print("   - Cleaner workflow with 6-step process")
    print("   - Better organization and maintainability")
    print("   - Web app compatibility maintained")
    print()
    
    print("5. 🚨 SAFETY:")
    print("   - All operations create backups automatically")
    print("   - Web app compatibility is preserved")
    print("   - No data loss during consolidation")

def main():
    print("🎨 Kunstquiz Current State Analysis")
    print("=" * 60)
    
    # Analyze files
    file_info = analyze_files()
    
    # Check duplicates
    duplicate_count = check_duplicates()
    
    # Check web app compatibility
    web_app_ok = check_web_app_compatibility()
    
    # Provide recommendations
    provide_recommendations()
    
    print("\n🎯 Next Steps:")
    if duplicate_count > 0:
        print(f"   - Found {duplicate_count} duplicates to clean up")
    if not web_app_ok:
        print("   - Web app compatibility issues need fixing")
    
    print("   - Run: python consolidate_data.py --analyze")
    print("   - Run: python workflow.py --init")

if __name__ == '__main__':
    main() 