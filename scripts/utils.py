#!/usr/bin/env python3
"""
Kunstquiz Utilities Script
==========================

Consolidated script for all utility operations.

USAGE EXAMPLES:
==============

# Check URLs for validity
python scripts/utils.py --check-urls

# Fix broken URLs
python scripts/utils.py --fix-urls

# Check gender and period distribution
python scripts/utils.py --gender-periods

# Create backup
python scripts/utils.py --backup --create

# List available backups
python scripts/utils.py --backup --list

# Restore from backup
python scripts/utils.py --backup --restore backup_20231201_143022

# Check data health
python scripts/utils.py --health-check

ARGUMENTS:
==========
--check-urls: Check URLs for validity
--fix-urls: Fix broken URLs
--gender-periods: Check gender and period distribution
--backup: Backup operations
--health-check: Comprehensive data health check

--create: Create new backup
--list: List available backups
--restore: Restore from backup (requires backup name)
--input: Input JSON file (default: data/paintings.json)
--output: Output JSON file (default: same as input)
--dry-run: Show what would be done without actually doing it
--no-dry-run: Actually perform the operation
"""

import json
import argparse
import os
import re
import shutil
import requests
from datetime import datetime
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
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

def check_urls(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check URLs for validity"""
    print("🔗 Checking URLs for validity...")
    
    total_urls = 0
    valid_urls = 0
    invalid_urls = 0
    broken_urls = []
    
    for item in data:
        url = item.get('url', '')
        if not url:
            continue
        
        total_urls += 1
        
        try:
            # Check if URL is well-formed
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                invalid_urls += 1
                broken_urls.append({
                    'url': url,
                    'artist': item.get('artist', ''),
                    'title': item.get('title', ''),
                    'reason': 'Malformed URL'
                })
                continue
            
            # Try to access the URL
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                valid_urls += 1
            else:
                invalid_urls += 1
                broken_urls.append({
                    'url': url,
                    'artist': item.get('artist', ''),
                    'title': item.get('title', ''),
                    'reason': f'HTTP {response.status_code}'
                })
        
        except requests.exceptions.RequestException as e:
            invalid_urls += 1
            broken_urls.append({
                'url': url,
                'artist': item.get('artist', ''),
                'title': item.get('title', ''),
                'reason': str(e)
            })
        except Exception as e:
            invalid_urls += 1
            broken_urls.append({
                'url': url,
                'artist': item.get('artist', ''),
                'title': item.get('title', ''),
                'reason': f'Error: {str(e)}'
            })
    
    results = {
        'total_urls': total_urls,
        'valid_urls': valid_urls,
        'invalid_urls': invalid_urls,
        'success_rate': (valid_urls / total_urls * 100) if total_urls > 0 else 0,
        'broken_urls': broken_urls
    }
    
    print(f"✅ URL check complete:")
    print(f"  Total URLs: {total_urls}")
    print(f"  Valid URLs: {valid_urls}")
    print(f"  Invalid URLs: {invalid_urls}")
    print(f"  Success rate: {results['success_rate']:.1f}%")
    
    if broken_urls:
        print(f"\n❌ Sample broken URLs:")
        for broken in broken_urls[:5]:
            print(f"  • {broken['artist']} - {broken['title']}")
            print(f"    URL: {broken['url']}")
            print(f"    Reason: {broken['reason']}")
    
    return results

def fix_urls(data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Fix broken URLs"""
    print("🔧 Fixing broken URLs...")
    
    fixed_count = 0
    
    for item in data:
        url = item.get('url', '')
        if not url:
            continue
        
        # Common URL fixes
        original_url = url
        
        # Fix common Wikimedia Commons issues
        if 'commons.wikimedia.org' in url:
            # Fix thumb URLs to full resolution
            if '/thumb/' in url:
                # Extract the original filename from thumb URL
                match = re.search(r'/thumb/[^/]+/([^/]+)$', url)
                if match:
                    filename = match.group(1)
                    # Remove size suffix if present
                    filename = re.sub(r'-\d+px-', '-', filename)
                    url = f"https://upload.wikimedia.org/wikipedia/commons/{filename}"
        
        # Fix missing protocol
        if url.startswith('//'):
            url = 'https:' + url
        elif not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Fix common domain issues
        url = url.replace('http://', 'https://')
        
        # Update URL if changed
        if url != original_url:
            item['url'] = url
            fixed_count += 1
    
    print(f"✅ Fixed {fixed_count} URLs")
    return data, fixed_count

def check_gender_periods(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check gender and period distribution"""
    print("👥 Checking gender and period distribution...")
    
    # Load artist bios for gender information
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
    
    # Analyze distribution
    gender_counts = Counter()
    period_gender_counts = defaultdict(Counter)
    century_gender_counts = defaultdict(Counter)
    
    for item in data:
        artist = item.get('artist', '')
        year = item.get('year', '')
        century = item.get('century', '')
        
        if artist in artist_genders:
            gender = artist_genders[artist]
            gender_counts[gender] += 1
            
            # By year period
            if year and year != 'Unknown':
                try:
                    year_int = int(year)
                    if year_int < 1800:
                        period = 'Pre-1800'
                    elif year_int < 1850:
                        period = '1800-1849'
                    elif year_int < 1900:
                        period = '1850-1899'
                    elif year_int < 1950:
                        period = '1900-1949'
                    else:
                        period = '1950+'
                    period_gender_counts[period][gender] += 1
                except ValueError:
                    pass
            
            # By century
            if century and century != 'Unknown':
                century_gender_counts[century][gender] += 1
    
    results = {
        'total_paintings': len(data),
        'paintings_with_gender': sum(gender_counts.values()),
        'gender_distribution': dict(gender_counts),
        'period_gender_distribution': {k: dict(v) for k, v in period_gender_counts.items()},
        'century_gender_distribution': {k: dict(v) for k, v in century_gender_counts.items()}
    }
    
    print(f"✅ Gender analysis complete:")
    print(f"  Total paintings: {results['total_paintings']}")
    print(f"  Paintings with gender data: {results['paintings_with_gender']}")
    
    print(f"\n👥 Gender Distribution:")
    for gender, count in gender_counts.most_common():
        percentage = (count / results['paintings_with_gender']) * 100 if results['paintings_with_gender'] > 0 else 0
        print(f"  • {gender}: {count} paintings ({percentage:.1f}%)")
    
    return results

def create_backup() -> str:
    """Create a new backup"""
    print("💾 Creating backup...")
    
    # Create backup directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Files to backup
    files_to_backup = [
        'data/paintings.json',
        'data/paintings.json',
        'data/artists.json',
        'data/artists.json',
        'data/artists.json'
    ]
    
    backed_up_files = []
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            # Copy file to backup directory
            filename = os.path.basename(file_path)
            backup_path = os.path.join(backup_dir, filename)
            shutil.copy2(file_path, backup_path)
            backed_up_files.append(filename)
            print(f"  ✅ Backed up {filename}")
        else:
            print(f"  ⚠️  File not found: {file_path}")
    
    print(f"✅ Backup created: {backup_dir}")
    print(f"Backed up {len(backed_up_files)} files")
    
    return backup_dir

def list_backups() -> List[str]:
    """List available backups"""
    print("📋 Available backups:")
    
    backups = []
    
    # Check if backups directory exists
    if not os.path.exists('backups'):
        print("  No backups directory found")
        return []
    
    for item in os.listdir('backups'):
        if item.startswith('backup_') and os.path.isdir(os.path.join('backups', item)):
            backups.append(item)
    
    if not backups:
        print("  No backups found")
        return []
    
    # Sort by creation time (newest first)
    backups.sort(key=lambda x: os.path.getctime(x), reverse=True)
    
    for i, backup in enumerate(backups, 1):
        # Get backup info
        ctime = os.path.getctime(backup)
        ctime_str = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")
        
        # Count files in backup
        file_count = len([f for f in os.listdir(backup) if os.path.isfile(os.path.join(backup, f))])
        
        print(f"  {i}. {backup}")
        print(f"     Created: {ctime_str}")
        print(f"     Files: {file_count}")
    
    return backups

def restore_backup(backup_name: str) -> bool:
    """Restore from backup"""
    print(f"🔄 Restoring from backup: {backup_name}")
    
    backup_path = os.path.join('backups', backup_name)
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_name}")
        return False
    
    if not os.path.isdir(backup_path):
        print(f"❌ Not a backup directory: {backup_name}")
        return False
    
    # Files to restore
    files_to_restore = [
        'paintings.json',
        'artists.json'
    ]
    
    restored_files = []
    
    for filename in files_to_restore:
        backup_file = os.path.join(backup_path, filename)
        restore_file = os.path.join('data', filename)
        
        if os.path.exists(backup_file):
            # Ensure data directory exists
            os.makedirs('data', exist_ok=True)
            
            # Copy file from backup
            shutil.copy2(backup_file, restore_file)
            restored_files.append(filename)
            print(f"  ✅ Restored {filename}")
        else:
            print(f"  ⚠️  File not found in backup: {filename}")
    
    print(f"✅ Restore complete! Restored {len(restored_files)} files")
    return True

def health_check(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Comprehensive data health check"""
    print("🏥 Running comprehensive data health check...")
    
    total_paintings = len(data)
    
    # Check for required fields
    missing_artist = 0
    missing_title = 0
    missing_url = 0
    missing_year = 0
    
    for item in data:
        if not item.get('artist'):
            missing_artist += 1
        if not item.get('title'):
            missing_title += 1
        if not item.get('url'):
            missing_url += 1
        if not item.get('year'):
            missing_year += 1
    
    # Check for duplicates
    url_counts = Counter()
    title_counts = Counter()
    
    for item in data:
        url = item.get('url', '')
        title = item.get('title', '')
        
        if url:
            url_counts[url] += 1
        if title:
            title_counts[title] += 1
    
    url_duplicates = sum(1 for count in url_counts.values() if count > 1)
    title_duplicates = sum(1 for count in title_counts.values() if count > 1)
    
    # Check image quality
    small_images = 0
    images_without_dimensions = 0
    
    for item in data:
        url = item.get('url', '')
        title = item.get('title', '')
        
        # Simple dimension check from URL
        if '/thumb/' in url and re.search(r'/\d+px-', url):
            small_images += 1
        
        # Check if dimensions are missing
        if not re.search(r'\d+x\d+', url) and not re.search(r'\d+\s*×\s*\d+', title):
            images_without_dimensions += 1
    
    # Calculate health scores
    completeness_score = ((total_paintings - missing_artist - missing_title - missing_url) / (total_paintings * 3)) * 100
    uniqueness_score = ((total_paintings - url_duplicates - title_duplicates) / (total_paintings * 2)) * 100
    quality_score = ((total_paintings - small_images - images_without_dimensions) / (total_paintings * 2)) * 100
    
    overall_score = (completeness_score + uniqueness_score + quality_score) / 3
    
    results = {
        'total_paintings': total_paintings,
        'completeness': {
            'score': completeness_score,
            'missing_artist': missing_artist,
            'missing_title': missing_title,
            'missing_url': missing_url,
            'missing_year': missing_year
        },
        'uniqueness': {
            'score': uniqueness_score,
            'url_duplicates': url_duplicates,
            'title_duplicates': title_duplicates
        },
        'quality': {
            'score': quality_score,
            'small_images': small_images,
            'images_without_dimensions': images_without_dimensions
        },
        'overall_score': overall_score
    }
    
    print(f"✅ Health check complete:")
    print(f"  Overall health score: {overall_score:.1f}%")
    print(f"  Completeness: {completeness_score:.1f}%")
    print(f"  Uniqueness: {uniqueness_score:.1f}%")
    print(f"  Quality: {quality_score:.1f}%")
    
    # Health recommendations
    if overall_score < 70:
        print("\n⚠️  Health recommendations:")
        if missing_artist > 0:
            print(f"  • Fix {missing_artist} missing artist names")
        if missing_title > 0:
            print(f"  • Fix {missing_title} missing titles")
        if url_duplicates > 0:
            print(f"  • Remove {url_duplicates} URL duplicates")
        if small_images > 0:
            print(f"  • Replace {small_images} small/thumbnail images")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Utilities Script')
    
    # Utility operations
    parser.add_argument('--check-urls', action='store_true', help='Check URLs for validity')
    parser.add_argument('--fix-urls', action='store_true', help='Fix broken URLs')
    parser.add_argument('--gender-periods', action='store_true', help='Check gender and period distribution')
    parser.add_argument('--backup', action='store_true', help='Backup operations')
    parser.add_argument('--health-check', action='store_true', help='Comprehensive data health check')
    
    # Backup options
    parser.add_argument('--create', action='store_true', help='Create new backup')
    parser.add_argument('--list', action='store_true', help='List available backups')
    parser.add_argument('--restore', type=str, help='Restore from backup (requires backup name)')
    
    # Options
    parser.add_argument('--input', default='data/paintings.json', help='Input JSON file')
    parser.add_argument('--output', default=None, help='Output JSON file (default: same as input)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Show what would be done without actually doing it (default)')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually perform the operation')
    
    args = parser.parse_args()
    
    # Set output file
    if args.output is None:
        args.output = args.input
    
    # Determine if this is a dry run
    dry_run = args.dry_run and not args.no_dry_run
    
    if dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
    
    # Handle backup operations
    if args.backup:
        if args.create:
            if not dry_run:
                backup_dir = create_backup()
                print(f"💡 To restore later, use: python scripts/utils.py --backup --restore {backup_dir}")
            else:
                print("Would create new backup")
        
        elif args.list:
            list_backups()
        
        elif args.restore:
            if not dry_run:
                restore_backup(args.restore)
            else:
                print(f"Would restore from backup: {args.restore}")
        
        else:
            print("Backup operation requires --create, --list, or --restore")
        
        return
    
    # Load data for other operations
    if any([args.check_urls, args.fix_urls, args.gender_periods, args.health_check]):
        print(f"Loading data from {args.input}...")
        data = load_json(args.input)
        if not data:
            print("No data loaded. Exiting.")
            return
        
        print(f"Loaded {len(data)} items from {args.input}")
    
    # Run requested operations
    if args.check_urls:
        print("\n🔗 Checking URLs...")
        if not dry_run:
            url_results = check_urls(data)
        else:
            print("Would check URLs for validity")
    
    if args.fix_urls:
        print("\n🔧 Fixing URLs...")
        if not dry_run:
            data, fixed_count = fix_urls(data)
            print(f"Fixed {fixed_count} URLs")
        else:
            print("Would fix broken URLs")
    
    if args.gender_periods:
        print("\n👥 Checking gender and periods...")
        if not dry_run:
            gender_results = check_gender_periods(data)
        else:
            print("Would check gender and period distribution")
    
    if args.health_check:
        print("\n🏥 Running health check...")
        if not dry_run:
            health_results = health_check(data)
        else:
            print("Would run comprehensive health check")
    
    # Save results if not dry run and operations were performed
    if not dry_run and any([args.fix_urls]):
        print(f"\n💾 Saving updated data to {args.output}...")
        save_json(data, args.output)
        print("✅ Operations complete!")
    elif dry_run:
        print("\n📊 DRY RUN SUMMARY:")
        print("No actual operations performed. To execute, run with --no-dry-run")
    else:
        print("\n✅ No operations specified")

if __name__ == '__main__':
    main() 