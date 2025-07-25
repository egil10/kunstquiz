#!/usr/bin/env python3
"""
Norwegian Art Collection Script
==============================

This script collects paintings from Wikimedia Commons and Wikipedia galleries.

USAGE EXAMPLES:
==============

# Collect from a single URL (recommended for testing)
python collect_art.py --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg" --max 50

# Collect from multiple URLs in a file
python collect_art.py --file urls.txt --max 30 --quiet --merge

# Collect from specific artist categories (gets ALL paintings from ALL museums automatically)
python collect_art.py --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_by_museum" --max 100

# Skip subcategories (only fetch from main category)
python collect_art.py --url "main_category_url" --no-subcategories

# Full workflow with diagnostics
python collect_art.py --file urls.txt --max 50 --quiet --merge --diagnose

URL STRATEGY:
============
- Use main categories for maximum coverage: "Category:Paintings_by_[Artist]"
- Use "by_museum" categories to get all museum collections automatically
- Script automatically follows subcategories and removes duplicates
- See category_strategy.md for detailed guidance

ARGUMENTS:
==========
--url: Single URL to collect from
--file: Text file with URLs (one per line, # for comments)
--max: Maximum paintings per URL
--quiet: Reduce verbose output
--no-subcategories: Skip subcategory processing
--merge: Run merge script after collection
--diagnose: Run diagnostics after merge
"""

import argparse
import json
import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
import subprocess

APPENDED_FILE = 'data/paintings_appended.json'
MANUAL_FILE = 'data/manual_paintings.json'
MERGE_SCRIPT = 'merge_artist_tags.py'
DIAGNOSE_SCRIPT = 'diagnostics.py'

# --- Manual collection logic (from collect_manual_art.py) ---


def fetch_wikipedia_gallery(url):
    images = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for gallery in soup.select('.gallery'):
        for imgdiv in gallery.select('.gallerybox'):
            img = imgdiv.find('img')
            if not img:
                continue
            img_url = 'https:' + img['src'] if img['src'].startswith('//') else img['src']
            caption = imgdiv.find(class_='gallerytext')
            title = caption.text.strip() if caption else ''
            year = None
            m = re.search(r'(\d{4})', title)
            if m:
                year = m.group(1)
            images.append({
                'url': img_url,
                'title': title,
                'year': year
            })
    return images

def fetch_commons_unified(url, max_images=None, follow_subcategories=True):
    """Unified function to fetch images from any Commons page (category, artist page, etc.)"""
    images = []
    session = requests.Session()
    print(f'Fetching: {url}')
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Check if this is a category page with subcategories
    if follow_subcategories and 'Category:' in url:
        subcategory_links = []
        
        # Look for subcategory links in the category page
        subcategory_selectors = [
            '.mw-category-group a[href*="/wiki/Category:"]',
            '.CategoryTreeItem a[href*="/wiki/Category:"]',
            '.mw-category a[href*="/wiki/Category:"]'
        ]
        
        for selector in subcategory_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href and '/wiki/Category:' in href:
                    subcategory_url = 'https://commons.wikimedia.org' + href
                    subcategory_title = link.get_text(strip=True)
                    # Skip meta-categories and administrative categories
                    if not any(skip in subcategory_title.lower() for skip in ['good pictures', 'featured pictures', 'quality images', 'valued images']):
                        subcategory_links.append((subcategory_url, subcategory_title))
        
        # If we found subcategories, fetch from them instead
        if subcategory_links:
            print(f'Found {len(subcategory_links)} subcategories, fetching from them...')
            total_found = 0
            
            for subcategory_url, subcategory_title in subcategory_links:
                if max_images and total_found >= max_images:
                    break
                    
                print(f'  Fetching subcategory: {subcategory_title}')
                remaining = max_images - total_found if max_images else None
                subcategory_images = fetch_commons_unified(subcategory_url, remaining, follow_subcategories=False)
                
                # Add subcategory images to our collection
                for img in subcategory_images:
                    if max_images and total_found >= max_images:
                        break
                    images.append(img)
                    total_found += 1
                
                if not args.quiet:
                    print(f'    Found {len(subcategory_images)} images from {subcategory_title}')
            
            # Remove duplicates and return
            seen_urls = set()
            unique_images = []
            for img in images:
                if img['url'] not in seen_urls:
                    seen_urls.add(img['url'])
                    unique_images.append(img)
            
            return unique_images

    # Strategy 1: Try category-style gallery first (most reliable for paintings)
    gallery_selectors = [
        '.gallery, .mw-category, .CategoryGallery',
        '.gallerybox, .CategoryGalleryItem, .mw-category-group, .gallerytext, .galleryfilename'
    ]
    
    gallery_images = []
    for container_selector in gallery_selectors:
        containers = soup.select(container_selector)
        if containers:
            for container in containers:
                if max_images and len(gallery_images) >= max_images:
                    break
                img = container.find('img')
                if not img:
                    continue
                img_url = 'https:' + img['src'] if img['src'].startswith('//') else img['src']
                title = container.get('title') or container.get('data-title') or container.text.strip()
                year = None
                m = re.search(r'(\d{4})', title)
                if m:
                    year = m.group(1)
                gallery_images.append({
                    'url': img_url,
                    'title': title,
                    'year': year
                })
        if max_images and len(gallery_images) >= max_images:
            break
    
    # Strategy 2: If no gallery found, try general Commons page layout
    if not gallery_images:
        general_selectors = [
            '.thumb',  # Standard Commons thumbnails
            '.gallerybox',  # Gallery boxes
            '.image',  # Image containers
            '.thumbinner',  # Thumbnail containers
            '.thumbcaption',  # Thumbnail captions
            '.fileinfo',  # File info sections
            '.mw-parser-output img',  # Any images in the main content
        ]
        
        for selector in general_selectors:
            if max_images and len(gallery_images) >= max_images:
                break
            elements = soup.select(selector)
            for element in elements:
                if max_images and len(gallery_images) >= max_images:
                    break
                # Find the actual image
                img = element.find('img') if element.name != 'img' else element
                if not img:
                    continue
                    
                # Get image URL
                img_src = img.get('src')
                if not img_src:
                    continue
                    
                img_url = 'https:' + img_src if img_src.startswith('//') else img_src
                
                # Get title/caption
                title = ''
                caption_element = element.find(class_='thumbcaption') or element.find(class_='fileinfo') or element
                if caption_element:
                    # Remove navigation and other non-title text
                    for unwanted in caption_element.select('.thumbcaption, .fileinfo, .metadata, .mw-editsection'):
                        unwanted.decompose()
                    title = caption_element.get_text(strip=True)
                
                # If no title from caption, try alt text or title attribute
                if not title:
                    title = img.get('alt') or img.get('title') or ''
                
                # Extract year from title
                year = None
                m = re.search(r'(\d{4})', title)
                if m:
                    year = m.group(1)
                
                # Only add if we have a meaningful title
                if title and len(title) > 3:
                    gallery_images.append({
                        'url': img_url,
                        'title': title,
                        'year': year
                    })
    
    # Strategy 3: Handle pagination for category pages
    if 'Category:' in url and gallery_images and not (max_images and len(gallery_images) >= max_images):
        # Look for next page links
        nextlink = soup.find('a', text=re.compile(r'next page', re.I))
        if nextlink and nextlink.get('href'):
            next_url = 'https://commons.wikimedia.org' + nextlink['href']
            print(f'Found next page, fetching: {next_url}')
            remaining = max_images - len(gallery_images) if max_images else None
            next_images = fetch_commons_unified(next_url, remaining)
            gallery_images.extend(next_images)
    
    # Remove duplicates based on URL
    seen_urls = set()
    unique_images = []
    for img in gallery_images:
        if img['url'] not in seen_urls:
            seen_urls.add(img['url'])
            unique_images.append(img)
    
    return unique_images

# --- Append logic (from append_manual_paintings.py) ---
def append_paintings(new_paintings, appended_file=APPENDED_FILE):
    if os.path.exists(appended_file):
        with open(appended_file, 'r', encoding='utf-8') as f:
            appended = json.load(f)
    else:
        appended = []
    existing_keys = set((p.get('artist'), p.get('title'), p.get('url')) for p in appended)
    added = 0
    for p in new_paintings:
        key = (p.get('artist'), p.get('title'), p.get('url'))
        if key not in existing_keys:
            appended.append(p)
            existing_keys.add(key)
            added += 1
    with open(appended_file, 'w', encoding='utf-8') as f:
        json.dump(appended, f, indent=2, ensure_ascii=False)
    print(f'Appended {added} new paintings to {appended_file}.')

# --- Main unified logic ---
def main():
    parser = argparse.ArgumentParser(description='Unified Norwegian Art Collection Script')
    parser.add_argument('--artist', action='append', help='Artist name to collect paintings for (can be used multiple times)')
    parser.add_argument('--url', action='append', help='URL to Wikimedia Commons or Wikipedia page to collect paintings from (can be used multiple times)')
    parser.add_argument('--file', help='File with artist names or URLs (one per line)')
    parser.add_argument('--max', type=int, help='Maximum number of paintings to collect per URL')
    parser.add_argument('--quiet', action='store_true', help='Reduce verbose output')
    parser.add_argument('--no-subcategories', action='store_true', help='Skip subcategories and only fetch from main category')
    parser.add_argument('--merge', action='store_true', help='Run merge script after appending')
    parser.add_argument('--diagnose', action='store_true', help='Run diagnostics after merge')
    args = parser.parse_args()

    # Collect all sources
    artists = args.artist or []
    urls = args.url or []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                if line.startswith('http'):
                    urls.append(line)
                else:
                    artists.append(line)

    all_new_paintings = []

    # --- Manual mode: URLs ---
    for url in urls:
        if 'commons.wikimedia.org' in url:
            follow_subcategories = not args.no_subcategories
            imgs = fetch_commons_unified(url, args.max, follow_subcategories)
        elif 'wikipedia.org' in url:
            imgs = fetch_wikipedia_gallery(url)
        else:
            print(f'Unknown URL type: {url}')
            continue
        # Optionally, you could prompt for artist name or infer from URL
        for img in imgs:
            if not img.get('artist'):
                # Try to infer artist from URL
                m = re.search(r'Category:Paintings_by_([^/]+)', url)
                if m:
                    artist_name = m.group(1).replace('_', ' ')
                    # Handle museum-specific URLs by extracting just the artist name
                    if ' in ' in artist_name:
                        # Extract the artist name before " in "
                        artist_name = artist_name.split(' in ')[0]
                    img['artist'] = artist_name
                else:
                    # Try other category patterns
                    m = re.search(r'Category:([^/]+)', url)
                    if m:
                        category_name = m.group(1).replace('_', ' ')
                        # Extract artist name from various category patterns
                        if ' by ' in category_name:
                            artist_name = category_name.split(' by ')[-1]
                        elif ' from ' in category_name:
                            artist_name = category_name.split(' from ')[0]
                        else:
                            artist_name = category_name
                        img['artist'] = artist_name
                    else:
                        # Extract artist name from main Commons page URL
                        m = re.search(r'wiki/([^/]+)$', url)
                        if m:
                            artist_name = m.group(1).replace('_', ' ')
                            # Handle museum-specific URLs
                            if ' in ' in artist_name:
                                artist_name = artist_name.split(' in ')[0]
                            # Handle "Artworks by" patterns
                            elif artist_name.startswith('Artworks_by_'):
                                artist_name = artist_name.replace('Artworks_by_', '')
                            # Handle life and works patterns
                            elif ', ' in artist_name and '_life_and_works' in artist_name:
                                artist_name = artist_name.split(', ')[0]
                            img['artist'] = artist_name
                        else:
                            img['artist'] = 'Unknown'
        all_new_paintings.extend(imgs)
        
        # Show results for this URL
        if not args.quiet:
            # Extract a clean URL name for display
            url_name = url.split('/')[-1].replace('_', ' ')
            if len(imgs) > 0:
                print(f'  ✅ Found {len(imgs)} paintings from {url_name}')
            else:
                print(f'  ⚠️  No paintings found in {url_name}')

    # --- Artist name mode (stub: you can expand this to use your current Wikidata/Commons logic) ---
    for artist in artists:
        print(f'[TODO] Would collect paintings for artist: {artist} (implement Wikidata/Commons logic here)')
        # You can integrate your current collect_norwegian_art.py logic here
        # For now, just skip

    # --- Append all new paintings ---
    if all_new_paintings:
        append_paintings(all_new_paintings)
        if not args.quiet:
            print(f'\n🎨 COLLECTION SUMMARY:')
            print(f'Total new paintings collected: {len(all_new_paintings)}')
            
            # Show breakdown by artist
            artist_counts = {}
            for painting in all_new_paintings:
                artist = painting.get('artist', 'Unknown')
                artist_counts[artist] = artist_counts.get(artist, 0) + 1
            
            if artist_counts:
                print(f'Breakdown by artist:')
                for artist, count in sorted(artist_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f'  • {artist}: {count} paintings')
    else:
        print('No new paintings to append.')

    # --- Optionally run merge and diagnostics ---
    if args.merge:
        if not args.quiet:
            print('Running merge script...')
        subprocess.run([sys.executable, MERGE_SCRIPT])
    if args.diagnose:
        if not args.quiet:
            print('Running diagnostics script...')
        subprocess.run([sys.executable, DIAGNOSE_SCRIPT])

if __name__ == '__main__':
    main() 