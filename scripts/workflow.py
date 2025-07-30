#!/usr/bin/env python3
"""
Kunstquiz Complete Workflow Script
==================================

Handles the complete 6-step workflow:
1. Finding new images
2. Cleaning them and deleting bad ones  
3. Finding manual URLs and websites to add
4. Finding manual URLs and websites to remove
5. Push to app
6. App should have working game logic and information

USAGE EXAMPLES:
==============

# Complete workflow (all 6 steps)
python workflow.py --full

# Individual steps
python workflow.py --collect --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Artist"
python workflow.py --clean --quality --duplicates
python workflow.py --add-urls --file config/urls_to_add.txt
python workflow.py --remove-urls --file config/urls_to_remove.txt
python workflow.py --process --finalize
python workflow.py --deploy

# Quick workflow (collect, clean, process, deploy)
python workflow.py --quick

ARGUMENTS:
==========
--full: Run complete 6-step workflow
--quick: Run quick workflow (collect, clean, process, deploy)
--collect: Step 1 - Find new images
--clean: Step 2 - Clean and remove bad images
--add-urls: Step 3 - Add manual URLs
--remove-urls: Step 4 - Remove manual URLs
--process: Step 5 - Process and finalize data
--deploy: Step 6 - Deploy to app

--url: URL to collect from (for --collect)
--file: File with URLs (for --add-urls or --remove-urls)
--max: Maximum images per URL (default: 50)
--total-max: Maximum total images (default: 200)
--quality: Enable quality filtering
--duplicates: Enable duplicate removal
--dry-run: Show what would be done without doing it
--no-dry-run: Actually perform operations
"""

import json
import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any

# Data file paths
RAW_PAINTINGS = 'data/raw/paintings_raw.json'
RAW_ARTISTS = 'data/raw/artists_raw.json'
PROCESSED_PAINTINGS = 'data/processed/paintings.json'
PROCESSED_ARTISTS = 'data/processed/artists.json'
CONFIG_ADD_URLS = 'data/config/urls_to_add.txt'
CONFIG_REMOVE_URLS = 'data/config/urls_to_remove.txt'

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        'data/raw',
        'data/processed', 
        'data/config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Ensured directory: {directory}")

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

def step1_collect(url: str = None, max_images: int = 50, total_max: int = 200):
    """Step 1: Find new images"""
    print("Step 1: Finding new images...")
    
    if url:
        # Collect from specific URL
        cmd = [
            sys.executable, 'scripts/collect_art.py',
            '--url', url,
            '--max', str(max_images),
            '--total-max', str(total_max),
            '--quiet'
        ]
    else:
        # Collect from URLs file if it exists
        if os.path.exists(CONFIG_ADD_URLS):
            cmd = [
                sys.executable, 'scripts/collect_art.py',
                '--file', CONFIG_ADD_URLS,
                '--max', str(max_images),
                '--total-max', str(total_max),
                '--quiet'
            ]
        else:
            print("⚠️  No URL provided and no urls_to_add.txt found")
            return False
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Collection complete!")
        return True
    else:
        print(f"❌ Collection failed: {result.stderr}")
        return False

def step2_clean(quality: bool = True, duplicates: bool = True):
    """Step 2: Clean and remove bad images"""
    print("Step 2: Cleaning images...")
    
    # Load current data
    current_data = load_json('data/paintings.json')
    if not current_data:
        print("⚠️  No data to clean")
        return False
    
    print(f"Loaded {len(current_data)} paintings to clean")
    
    # Build clean command
    cmd = [sys.executable, 'scripts/clean.py']
    
    if duplicates:
        cmd.extend(['--duplicates', '--strategy', 'url'])
    
    if quality:
        cmd.extend(['--quality', '--min-width', '200', '--min-height', '200'])
    
    cmd.extend(['--no-dry-run'])
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Cleaning complete!")
        return True
    else:
        print(f"❌ Cleaning failed: {result.stderr}")
        return False

def step3_add_urls(file_path: str = None):
    """Step 3: Add manual URLs and websites"""
    print("Step 3: Adding manual URLs...")
    
    if file_path and os.path.exists(file_path):
        # Use provided file
        urls_file = file_path
    elif os.path.exists(CONFIG_ADD_URLS):
        # Use default config file
        urls_file = CONFIG_ADD_URLS
    else:
        print("⚠️  No URLs file found")
        return False
    
    # Read URLs to add
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not urls:
        print("⚠️  No URLs found in file")
        return False
    
    print(f"Found {len(urls)} URLs to add")
    
    # Collect from each URL
    for url in urls:
        print(f"Collecting from: {url}")
        success = step1_collect(url, max_images=30, total_max=100)
        if not success:
            print(f"⚠️  Failed to collect from {url}")
    
    print("✅ URL addition complete!")
    return True

def step4_remove_urls(file_path: str = None):
    """Step 4: Remove manual URLs and websites"""
    print("Step 4: Removing manual URLs...")
    
    if file_path and os.path.exists(file_path):
        # Use provided file
        urls_file = file_path
    elif os.path.exists(CONFIG_REMOVE_URLS):
        # Use default config file
        urls_file = CONFIG_REMOVE_URLS
    else:
        print("⚠️  No URLs file found")
        return False
    
    # Run clean script with URL removal
    cmd = [
        sys.executable, 'scripts/clean.py',
        '--urls',
        '--file', urls_file,
        '--no-dry-run'
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ URL removal complete!")
        return True
    else:
        print(f"❌ URL removal failed: {result.stderr}")
        return False

def step5_process():
    """Step 5: Process and finalize data for app"""
    print("Step 5: Processing data for app...")
    
    # Run full processing workflow
    cmd = [
        sys.executable, 'scripts/process.py',
        '--full-process',
        '--no-dry-run'
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Processing complete!")
        return True
    else:
        print(f"❌ Processing failed: {result.stderr}")
        return False

def step6_deploy():
    """Step 6: Deploy to app (create final app data)"""
    print("Step 6: Deploying to app...")
    
    # Load processed data
    paintings_data = load_json('data/paintings.json')
    artists_data = load_json('data/artists.json')
    
    if not paintings_data:
        print("❌ No paintings data found")
        return False
    
    # Create final app data structure
    app_data = {
        'paintings': paintings_data,
        'artists': artists_data,
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_paintings': len(paintings_data),
            'total_artists': len(artists_data) if artists_data else 0,
            'version': '1.0'
        }
    }
    
    # Save unified app data
    save_json(app_data, 'data/app_data.json')
    
    # Also save individual files for backward compatibility
    save_json(paintings_data, 'data/paintings.json')
    save_json(artists_data, 'data/artists.json')
    
    print(f"App deployment complete!")
    print(f"  - Total paintings: {len(paintings_data)}")
    print(f"  - Total artists: {len(artists_data) if artists_data else 0}")
    print(f"  - App data saved to: data/app_data.json")
    
    return True

def run_full_workflow():
    """Run complete 6-step workflow"""
    print("Running complete 6-step workflow...")
    print("=" * 50)
    
    # Step 1: Collect
    if not step1_collect():
        print("❌ Workflow failed at Step 1")
        return False
    
    # Step 2: Clean
    if not step2_clean():
        print("❌ Workflow failed at Step 2")
        return False
    
    # Step 3: Add URLs
    if not step3_add_urls():
        print("⚠️  Step 3 skipped (no URLs to add)")
    
    # Step 4: Remove URLs
    if not step4_remove_urls():
        print("⚠️  Step 4 skipped (no URLs to remove)")
    
    # Step 5: Process
    if not step5_process():
        print("❌ Workflow failed at Step 5")
        return False
    
    # Step 6: Deploy
    if not step6_deploy():
        print("❌ Workflow failed at Step 6")
        return False
    
    print("🎉 Complete workflow successful!")
    return True

def run_quick_workflow():
    """Run quick workflow (collect, clean, process, deploy)"""
    print("Running quick workflow...")
    print("=" * 50)
    
    # Step 1: Collect
    if not step1_collect():
        print("❌ Quick workflow failed at Step 1")
        return False
    
    # Step 2: Clean
    if not step2_clean():
        print("❌ Quick workflow failed at Step 2")
        return False
    
    # Step 5: Process
    if not step5_process():
        print("❌ Quick workflow failed at Step 5")
        return False
    
    # Step 6: Deploy
    if not step6_deploy():
        print("❌ Quick workflow failed at Step 6")
        return False
    
    print("🎉 Quick workflow successful!")
    return True

def create_config_files():
    """Create default config files if they don't exist"""
    if not os.path.exists(CONFIG_ADD_URLS):
        with open(CONFIG_ADD_URLS, 'w', encoding='utf-8') as f:
            f.write("# URLs to add to the collection\n")
            f.write("# One URL per line\n")
            f.write("# Lines starting with # are comments\n")
            f.write("\n")
            f.write("# Example:\n")
            f.write("# https://commons.wikimedia.org/wiki/Category:Paintings_by_Artist_Name\n")
        print(f"✅ Created: {CONFIG_ADD_URLS}")
    
    if not os.path.exists(CONFIG_REMOVE_URLS):
        with open(CONFIG_REMOVE_URLS, 'w', encoding='utf-8') as f:
            f.write("# URLs to remove from the collection\n")
            f.write("# One URL per line\n")
            f.write("# Lines starting with # are comments\n")
            f.write("\n")
            f.write("# Example:\n")
            f.write("# https://commons.wikimedia.org/wiki/File:example.jpg\n")
        print(f"✅ Created: {CONFIG_REMOVE_URLS}")

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Complete Workflow Script')
    
    # Workflow options
    parser.add_argument('--full', action='store_true', help='Run complete 6-step workflow')
    parser.add_argument('--quick', action='store_true', help='Run quick workflow (collect, clean, process, deploy)')
    
    # Individual steps
    parser.add_argument('--collect', action='store_true', help='Step 1 - Find new images')
    parser.add_argument('--clean', action='store_true', help='Step 2 - Clean and remove bad images')
    parser.add_argument('--add-urls', action='store_true', help='Step 3 - Add manual URLs')
    parser.add_argument('--remove-urls', action='store_true', help='Step 4 - Remove manual URLs')
    parser.add_argument('--process', action='store_true', help='Step 5 - Process and finalize data')
    parser.add_argument('--deploy', action='store_true', help='Step 6 - Deploy to app')
    
    # Options
    parser.add_argument('--url', type=str, help='URL to collect from (for --collect)')
    parser.add_argument('--file', type=str, help='File with URLs (for --add-urls or --remove-urls)')
    parser.add_argument('--max', type=int, default=50, help='Maximum images per URL (default: 50)')
    parser.add_argument('--total-max', type=int, default=200, help='Maximum total images (default: 200)')
    parser.add_argument('--quality', action='store_true', help='Enable quality filtering')
    parser.add_argument('--duplicates', action='store_true', help='Enable duplicate removal')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without doing it')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually perform operations')
    parser.add_argument('--init', action='store_true', help='Initialize directory structure and config files')
    
    args = parser.parse_args()
    
    # Initialize if requested
    if args.init:
        ensure_directories()
        create_config_files()
        return
    
    # Ensure directories exist
    ensure_directories()
    
    # Determine if this is a dry run
    dry_run = args.dry_run and not args.no_dry_run
    
    if dry_run:
        print("🔍 DRY RUN - No changes will be made")
    
    # Run workflows
    if args.full:
        if not dry_run:
            run_full_workflow()
        else:
            print("Would run complete 6-step workflow")
    
    elif args.quick:
        if not dry_run:
            run_quick_workflow()
        else:
            print("Would run quick workflow")
    
    # Run individual steps
    elif args.collect:
        if not dry_run:
            step1_collect(args.url, args.max, args.total_max)
        else:
            print(f"Would collect from URL: {args.url}")
    
    elif args.clean:
        if not dry_run:
            step2_clean(args.quality, args.duplicates)
        else:
            print("Would clean data")
    
    elif args.add_urls:
        if not dry_run:
            step3_add_urls(args.file)
        else:
            print(f"Would add URLs from file: {args.file}")
    
    elif args.remove_urls:
        if not dry_run:
            step4_remove_urls(args.file)
        else:
            print(f"Would remove URLs from file: {args.file}")
    
    elif args.process:
        if not dry_run:
            step5_process()
        else:
            print("Would process data")
    
    elif args.deploy:
        if not dry_run:
            step6_deploy()
        else:
            print("Would deploy to app")
    
    else:
        print("No operation specified. Use --help for options.")
        print("\nQuick start:")
        print("  python workflow.py --init          # Initialize structure")
        print("  python workflow.py --quick         # Run quick workflow")
        print("  python workflow.py --full          # Run complete workflow")

if __name__ == '__main__':
    main() 