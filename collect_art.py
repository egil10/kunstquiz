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
DIAGNOSE_SCRIPT = 'diagnose_art.py'

# --- Manual collection logic (from collect_manual_art.py) ---
def fetch_commons_category(url):
    images = []
    session = requests.Session()
    while url:
        print(f'Fetching: {url}')
        r = session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        gallery = soup.select('.gallery, .mw-category, .CategoryGallery')
        if not gallery:
            gallery = [soup]
        for g in gallery:
            for imgdiv in g.select('.gallerybox, .CategoryGalleryItem, .mw-category-group, .gallerytext, .galleryfilename'):
                img = imgdiv.find('img')
                if not img:
                    continue
                img_url = 'https:' + img['src'] if img['src'].startswith('//') else img['src']
                title = imgdiv.get('title') or imgdiv.get('data-title') or imgdiv.text.strip()
                year = None
                m = re.search(r'(\d{4})', title)
                if m:
                    year = m.group(1)
                images.append({
                    'url': img_url,
                    'title': title,
                    'year': year
                })
        nextlink = soup.find('a', text=re.compile(r'next page', re.I))
        if nextlink and nextlink.get('href'):
            url = 'https://commons.wikimedia.org' + nextlink['href']
        else:
            break
    return images

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
            imgs = fetch_commons_category(url)
        elif 'wikipedia.org' in url:
            imgs = fetch_wikipedia_gallery(url)
        else:
            print(f'Unknown URL type: {url}')
            continue
        print(f'Found {len(imgs)} images in {url}')
        # Optionally, you could prompt for artist name or infer from URL
        for img in imgs:
            if not img.get('artist'):
                # Try to infer artist from URL or prompt user
                m = re.search(r'Category:Paintings_by_([^/]+)', url)
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
    else:
        print('No new paintings to append.')

    # --- Optionally run merge and diagnostics ---
    if args.merge:
        print('Running merge script...')
        subprocess.run([sys.executable, MERGE_SCRIPT])
    if args.diagnose:
        print('Running diagnostics script...')
        subprocess.run([sys.executable, DIAGNOSE_SCRIPT])

if __name__ == '__main__':
    main() 