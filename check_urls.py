#!/usr/bin/env python3
"""
Check Image URLs in Kunstquiz Data

This script analyzes the image URLs in the paintings JSON files to identify:
- Malformed URLs
- Non-Wikimedia Commons URLs
- URLs that might not load properly
- Common URL patterns and issues
"""

import json
import re
from urllib.parse import urlparse
from collections import Counter

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

def analyze_url(url):
    """Analyze a single URL and return issues found"""
    issues = []
    
    if not url:
        issues.append("Empty URL")
        return issues
    
    # Check if it's a valid URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            issues.append("Invalid URL format")
            return issues
    except Exception:
        issues.append("Malformed URL")
        return issues
    
    # Check if it's a Wikimedia Commons URL
    if 'wikimedia.org' not in parsed.netloc and 'wikipedia.org' not in parsed.netloc:
        issues.append("Not a Wikimedia URL")
    
    # Check for common problematic patterns
    if '/thumb/' in url:
        # Check if it's a proper thumbnail URL
        if not re.search(r'/\d+px-', url):
            issues.append("Thumbnail URL without size")
    
    # Check for missing file extensions
    if not re.search(r'\.(jpg|jpeg|png|gif|webp|svg)$', url, re.IGNORECASE):
        issues.append("No image file extension")
    
    # Check for very long URLs (might be truncated)
    if len(url) > 500:
        issues.append("Very long URL (might be truncated)")
    
    # Check for HTML entities or encoded characters
    if '&amp;' in url or '&lt;' in url or '&gt;' in url:
        issues.append("Contains HTML entities")
    
    # Check for spaces in URL
    if ' ' in url:
        issues.append("Contains spaces (should be URL encoded)")
    
    return issues

def main():
    files_to_check = [
        'data/paintings_merged.json',
        'data/paintings_appended.json'
    ]
    
    for filepath in files_to_check:
        print(f"\n🔍 Analyzing: {filepath}")
        print("=" * 60)
        
        paintings = load_json(filepath)
        if not paintings:
            continue
        
        print(f"📊 Total paintings: {len(paintings)}")
        
        # Analyze URLs
        url_issues = []
        domain_stats = Counter()
        extension_stats = Counter()
        problematic_urls = []
        
        for i, painting in enumerate(paintings):
            url = painting.get('url', '')
            if not url:
                continue
            
            # Get domain
            try:
                parsed = urlparse(url)
                domain_stats[parsed.netloc] += 1
            except:
                pass
            
            # Get file extension
            ext_match = re.search(r'\.([a-zA-Z0-9]+)$', url)
            if ext_match:
                extension_stats[ext_match.group(1).lower()] += 1
            
            # Check for issues
            issues = analyze_url(url)
            if issues:
                url_issues.extend(issues)
                problematic_urls.append({
                    'index': i,
                    'url': url,
                    'title': painting.get('title', 'Unknown'),
                    'artist': painting.get('artist', 'Unknown'),
                    'issues': issues
                })
        
        # Report results
        print(f"\n📈 URL Statistics:")
        print(f"   Total URLs analyzed: {len(paintings)}")
        print(f"   URLs with issues: {len(problematic_urls)}")
        print(f"   Issue rate: {len(problematic_urls)/len(paintings)*100:.1f}%")
        
        print(f"\n🌐 Domain Distribution:")
        for domain, count in domain_stats.most_common(5):
            print(f"   {domain}: {count}")
        
        print(f"\n📁 File Extension Distribution:")
        for ext, count in extension_stats.most_common(5):
            print(f"   .{ext}: {count}")
        
        print(f"\n⚠️  Issue Types:")
        issue_counts = Counter(url_issues)
        for issue, count in issue_counts.most_common():
            print(f"   {issue}: {count}")
        
        if problematic_urls:
            print(f"\n🚨 Sample Problematic URLs (first 10):")
            for item in problematic_urls[:10]:
                print(f"   [{item['index']}] {item['artist']} - {item['title'][:50]}...")
                print(f"       URL: {item['url'][:100]}...")
                print(f"       Issues: {', '.join(item['issues'])}")
                print()
        
        # Check for specific patterns
        print(f"\n🔍 URL Pattern Analysis:")
        
        # Check for thumbnails
        thumb_count = sum(1 for p in paintings if '/thumb/' in p.get('url', ''))
        print(f"   Thumbnail URLs: {thumb_count}")
        
        # Check for direct file URLs
        direct_count = sum(1 for p in paintings if '/wiki/File:' in p.get('url', ''))
        print(f"   Direct file URLs: {direct_count}")
        
        # Check for very short URLs (might be incomplete)
        short_urls = [p for p in paintings if len(p.get('url', '')) < 50]
        print(f"   Very short URLs (<50 chars): {len(short_urls)}")

if __name__ == '__main__':
    main() 