#!/usr/bin/env python3
"""
Fix Image URLs in Kunstquiz Data

This script fixes truncated URLs and other URL issues in the paintings JSON files.
"""

import json
import re
import requests
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import time

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
        print(f"✅ Saved: {filepath}")
    except Exception as e:
        print(f"ERROR: Failed to save {filepath}: {e}")

def clean_title(title):
    """Clean HTML from titles"""
    if not title:
        return title
    
    # Remove HTML tags
    title = re.sub(r'<[^>]+>', '', title)
    # Remove extra whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def is_truncated_url(url):
    """Check if URL appears to be truncated"""
    if not url:
        return False
    
    # Check if URL ends with common truncation patterns
    if url.endswith('...') or url.endswith('…'):
        return True
    
    # Check if URL is missing file extension
    if not re.search(r'\.(jpg|jpeg|png|gif|webp|svg|tif|tiff)$', url, re.IGNORECASE):
        return True
    
    # Check if URL is suspiciously short for a Wikimedia URL
    if len(url) < 80:
        return True
    
    return False

def extract_filename_from_url(url):
    """Extract filename from a truncated Wikimedia URL"""
    if not url:
        return None
    
    # Remove truncation markers
    url = url.replace('...', '').replace('…', '')
    
    # Try to extract the filename part
    # Wikimedia URLs typically follow: /wikipedia/commons/X/XX/Filename.jpg
    match = re.search(r'/commons/[a-f0-9]/[a-f0-9]{2}/([^/]+)$', url)
    if match:
        filename = match.group(1)
        # URL decode the filename
        filename = unquote(filename)
        return filename
    
    return None

def find_complete_url_from_filename(filename):
    """Try to find the complete URL by searching Wikimedia Commons"""
    if not filename:
        return None
    
    try:
        # Search for the file on Wikimedia Commons
        search_url = f"https://commons.wikimedia.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'titles': f'File:{filename}',
            'prop': 'imageinfo',
            'iiprop': 'url|size|mime'
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract the image URL
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if page_id != '-1':  # Page exists
                imageinfo = page_data.get('imageinfo', [])
                if imageinfo:
                    return imageinfo[0].get('url')
        
        return None
        
    except Exception as e:
        print(f"   ⚠️  Error searching for {filename}: {e}")
        return None

def fix_thumbnail_url(url):
    """Fix thumbnail URLs that are missing size specification"""
    if not url or '/thumb/' not in url:
        return url
    
    # Check if it already has a size specification
    if re.search(r'/\d+px-', url):
        return url
    
    # Try to add a reasonable size (300px)
    if '/thumb/' in url:
        # Find the position after /thumb/
        thumb_pos = url.find('/thumb/')
        if thumb_pos != -1:
            # Insert size specification
            new_url = url[:thumb_pos + 7] + '300px-' + url[thumb_pos + 7:]
            return new_url
    
    return url

def fix_painting_urls(paintings, verbose=False):
    """Fix URLs in paintings data"""
    fixed_count = 0
    cleaned_count = 0
    
    for i, painting in enumerate(paintings):
        original_url = painting.get('url', '')
        original_title = painting.get('title', '')
        
        # Clean the title
        cleaned_title = clean_title(original_title)
        if cleaned_title != original_title:
            painting['title'] = cleaned_title
            cleaned_count += 1
        
        # Fix truncated URLs
        if is_truncated_url(original_url):
            if verbose:
                print(f"   [{i}] Fixing truncated URL: {original_url[:80]}...")
            
            # Try to extract filename and find complete URL
            filename = extract_filename_from_url(original_url)
            if filename:
                complete_url = find_complete_url_from_filename(filename)
                if complete_url:
                    painting['url'] = complete_url
                    fixed_count += 1
                    if verbose:
                        print(f"      ✅ Fixed: {complete_url[:80]}...")
                    # Add delay to be respectful to Wikimedia servers
                    time.sleep(0.1)
                else:
                    if verbose:
                        print(f"      ❌ Could not find complete URL for: {filename}")
            else:
                if verbose:
                    print(f"      ❌ Could not extract filename from: {original_url}")
        
        # Fix thumbnail URLs
        elif '/thumb/' in original_url:
            fixed_url = fix_thumbnail_url(original_url)
            if fixed_url != original_url:
                painting['url'] = fixed_url
                fixed_count += 1
                if verbose:
                    print(f"   [{i}] Fixed thumbnail URL: {fixed_url[:80]}...")
    
    return fixed_count, cleaned_count

def main():
    files_to_fix = [
        'data/paintings_merged.json',
        'data/paintings_appended.json'
    ]
    
    for filepath in files_to_fix:
        print(f"\n🔧 Fixing: {filepath}")
        print("=" * 60)
        
        paintings = load_json(filepath)
        if not paintings:
            continue
        
        print(f"📊 Total paintings: {len(paintings)}")
        
        # Count issues before fixing
        truncated_count = sum(1 for p in paintings if is_truncated_url(p.get('url', '')))
        html_titles = sum(1 for p in paintings if '<' in p.get('title', ''))
        
        print(f"🚨 Issues found:")
        print(f"   Truncated URLs: {truncated_count}")
        print(f"   HTML in titles: {html_titles}")
        
        if truncated_count == 0 and html_titles == 0:
            print("✅ No issues found!")
            continue
        
        # Fix the issues
        print(f"\n🔧 Fixing issues...")
        fixed_urls, cleaned_titles = fix_painting_urls(paintings, verbose=True)
        
        print(f"\n📈 Results:")
        print(f"   Fixed URLs: {fixed_urls}")
        print(f"   Cleaned titles: {cleaned_titles}")
        
        # Save the fixed data
        save_json(paintings, filepath)
        
        # Verify fixes
        truncated_after = sum(1 for p in paintings if is_truncated_url(p.get('url', '')))
        html_after = sum(1 for p in paintings if '<' in p.get('title', ''))
        
        print(f"   Remaining truncated URLs: {truncated_after}")
        print(f"   Remaining HTML in titles: {html_after}")

if __name__ == '__main__':
    main() 