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

def fetch_commons_unified(url, max_images=None):
    """Unified function to fetch images from any Commons page (category, artist page, etc.)"""
    images = []
    session = requests.Session()
    print(f'Fetching: {url}')
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
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
                if not line:
                    continue
                if line.startswith('http'):
                    urls.append(line)
                else:
                    artists.append(line)

    all_new_paintings = []

    # --- Manual mode: URLs ---
    for url in urls:
        if 'commons.wikimedia.org' in url:
            imgs = fetch_commons_unified(url, args.max)
        elif 'wikipedia.org' in url:
            imgs = fetch_wikipedia_gallery(url)
        else:
            print(f'Unknown URL type: {url}')
            continue
        if not args.quiet:
            print(f'Found {len(imgs)} images in {url}')
        # Optionally, you could prompt for artist name or infer from URL
        for img in imgs:
            if not img.get('artist'):
                # Try to infer artist from URL
                m = re.search(r'Category:Paintings_by_([^/]+)', url)
                if m:
                    img['artist'] = m.group(1).replace('_', ' ')
                else:
                    # Extract artist name from main Commons page URL
                    m = re.search(r'wiki/([^/]+)$', url)
                    if m:
                        img['artist'] = m.group(1).replace('_', ' ')
                    else:
                        img['artist'] = 'Unknown'
        all_new_paintings.extend(imgs)

    # --- Artist name mode (stub: you can expand this to use your current Wikidata/Commons logic) ---
    for artist in artists:
        print(f'[TODO] Would collect paintings for artist: {artist} (implement Wikidata/Commons logic here)')
        # You can integrate your current collect_norwegian_art.py logic here
        # For now, just skip

    # --- Append all new paintings ---
    if all_new_paintings:
        append_paintings(all_new_paintings)
        if not args.quiet:
            print(f'Total new paintings collected: {len(all_new_paintings)}')
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