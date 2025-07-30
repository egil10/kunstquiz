#!/usr/bin/env python3
"""
Visual Duplicate Detection for Norwegian Art Dataset

This script detects visual duplicates (same image, different URLs) using:
1. Perceptual hashing (pHash) - detects identical/similar images
2. Average hashing (aHash) - detects exact duplicates
3. Difference hashing (dHash) - detects rotated/scaled duplicates

Requirements:
pip install imagehash pillow requests numpy
"""

import json
import argparse
import os
import hashlib
from typing import List, Dict, Any, Tuple, Set
from collections import defaultdict
import requests
from io import BytesIO
from PIL import Image
import imagehash
import numpy as np
from urllib.parse import urlparse
import time

def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        return []

def download_image(url: str, timeout: int = 10) -> Image.Image:
    """Download and open image from URL"""
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img.convert('RGB')  # Convert to RGB for consistent processing
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def calculate_image_hashes(img: Image.Image) -> Dict[str, str]:
    """Calculate multiple hash types for an image"""
    try:
        return {
            'phash': str(imagehash.phash(img)),  # Perceptual hash (most reliable for duplicates)
            'ahash': str(imagehash.average_hash(img)),  # Average hash (exact duplicates)
            'dhash': str(imagehash.dhash(img)),  # Difference hash (rotation/scaling invariant)
            'whash': str(imagehash.whash(img))   # Wavelet hash (another perceptual variant)
        }
    except Exception as e:
        print(f"Failed to calculate hashes: {e}")
        return None

def hamming_distance(hash1: str, hash2: str) -> int:
    """Calculate Hamming distance between two hash strings"""
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def find_visual_duplicates(paintings: List[Dict[str, Any]], 
                          hash_threshold: int = 5,
                          max_images: int = None,
                          dry_run: bool = True) -> Tuple[List[Dict], List[Dict]]:
    """
    Find visual duplicates using image hashing
    
    Args:
        paintings: List of painting objects
        hash_threshold: Maximum Hamming distance for considering images similar
        max_images: Maximum number of images to process (for testing)
        dry_run: If True, don't download images, just analyze structure
    
    Returns:
        Tuple of (duplicate_groups, failed_downloads)
    """
    
    if max_images:
        paintings = paintings[:max_images]
    
    print(f"Processing {len(paintings)} paintings...")
    
    # Group paintings by hash
    hash_groups = defaultdict(list)
    failed_downloads = []
    
    for i, painting in enumerate(paintings):
        url = painting.get('url', '')
        if not url:
            continue
            
        print(f"Processing {i+1}/{len(paintings)}: {painting.get('title', 'Unknown')[:50]}...")
        
        if dry_run:
            # In dry run, just simulate hash calculation
            fake_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            hash_groups[fake_hash].append(painting)
            continue
        
        # Download and hash image
        img = download_image(url)
        if img is None:
            failed_downloads.append(painting)
            continue
        
        hashes = calculate_image_hashes(img)
        if hashes is None:
            failed_downloads.append(painting)
            continue
        
        # Use perceptual hash as primary key
        phash = hashes['phash']
        hash_groups[phash].append({
            'painting': painting,
            'hashes': hashes,
            'image': img
        })
        
        # Small delay to be respectful to servers
        time.sleep(0.1)
    
    # Find groups with multiple images (potential duplicates)
    duplicate_groups = []
    
    for phash, items in hash_groups.items():
        if len(items) > 1:
            # Check if these are actually similar using multiple hash types
            similar_items = []
            
            for i, item1 in enumerate(items):
                for j, item2 in enumerate(items[i+1:], i+1):
                    # Compare multiple hash types
                    hamming_phash = hamming_distance(item1['hashes']['phash'], item2['hashes']['phash'])
                    hamming_ahash = hamming_distance(item1['hashes']['ahash'], item2['hashes']['ahash'])
                    hamming_dhash = hamming_distance(item1['hashes']['dhash'], item2['hashes']['dhash'])
                    
                    # Consider similar if any hash type is close
                    if (hamming_phash <= hash_threshold or 
                        hamming_ahash <= hash_threshold or 
                        hamming_dhash <= hash_threshold):
                        
                        similar_items.append({
                            'item1': item1['painting'],
                            'item2': item2['painting'],
                            'hamming_distances': {
                                'phash': hamming_phash,
                                'ahash': hamming_ahash,
                                'dhash': hamming_dhash
                            }
                        })
            
            if similar_items:
                duplicate_groups.append({
                    'hash': phash,
                    'similar_pairs': similar_items,
                    'all_items': [item['painting'] for item in items]
                })
    
    return duplicate_groups, failed_downloads

def analyze_duplicate_groups(duplicate_groups: List[Dict]) -> None:
    """Analyze and display duplicate information"""
    print(f"\n🔍 Found {len(duplicate_groups)} duplicate groups:")
    
    for i, group in enumerate(duplicate_groups):
        print(f"\n--- Group {i+1} ---")
        print(f"Hash: {group['hash']}")
        print(f"Total items: {len(group['all_items'])}")
        
        for j, pair in enumerate(group['similar_pairs']):
            item1 = pair['item1']
            item2 = pair['item2']
            distances = pair['hamming_distances']
            
            print(f"\n  Similar Pair {j+1}:")
            print(f"    A: {item1.get('artist', 'Unknown')} - {item1.get('title', 'Unknown')[:50]}")
            print(f"       URL: {item1.get('url', '')[:80]}...")
            print(f"    B: {item2.get('artist', 'Unknown')} - {item2.get('title', 'Unknown')[:50]}")
            print(f"       URL: {item2.get('url', '')[:80]}...")
            print(f"    Hamming distances: pHash={distances['phash']}, aHash={distances['ahash']}, dHash={distances['dhash']}")

def save_duplicate_report(duplicate_groups: List[Dict], output_file: str = 'visual_duplicates_report.json'):
    """Save duplicate analysis to JSON file"""
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_groups': len(duplicate_groups),
        'duplicate_groups': []
    }
    
    for group in duplicate_groups:
        group_data = {
            'hash': group['hash'],
            'total_items': len(group['all_items']),
            'similar_pairs': []
        }
        
        for pair in group['similar_pairs']:
            pair_data = {
                'item1': {
                    'artist': pair['item1'].get('artist', ''),
                    'title': pair['item1'].get('title', ''),
                    'url': pair['item1'].get('url', '')
                },
                'item2': {
                    'artist': pair['item2'].get('artist', ''),
                    'title': pair['item2'].get('title', ''),
                    'url': pair['item2'].get('url', '')
                },
                'hamming_distances': pair['hamming_distances']
            }
            group_data['similar_pairs'].append(pair_data)
        
        report['duplicate_groups'].append(group_data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Detect visual duplicates in paintings dataset')
        parser.add_argument('--input', default='data/paintings.json',
                        help='Input JSON file (default: data/paintings.json)')
    parser.add_argument('--threshold', type=int, default=5,
                       help='Hash similarity threshold (0-64, lower = more strict)')
    parser.add_argument('--max-images', type=int, default=None,
                       help='Maximum number of images to process (for testing)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Dry run - analyze structure without downloading images')
    parser.add_argument('--output', default='visual_duplicates_report.json',
                       help='Output report file (default: visual_duplicates_report.json)')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    paintings = load_json(args.input)
    if not paintings:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(paintings)} paintings")
    
    # Find duplicates
    duplicate_groups, failed_downloads = find_visual_duplicates(
        paintings, 
        hash_threshold=args.threshold,
        max_images=args.max_images,
        dry_run=args.dry_run
    )
    
    # Report results
    print(f"\n📊 Analysis Summary:")
    print(f"- Total paintings processed: {len(paintings)}")
    print(f"- Failed downloads: {len(failed_downloads)}")
    print(f"- Duplicate groups found: {len(duplicate_groups)}")
    
    if duplicate_groups:
        analyze_duplicate_groups(duplicate_groups)
        save_duplicate_report(duplicate_groups, args.output)
        
        # Summary of duplicates
        total_duplicates = sum(len(group['similar_pairs']) for group in duplicate_groups)
        print(f"\n🎯 Total duplicate pairs found: {total_duplicates}")
        print(f"💡 Consider removing {total_duplicates} duplicate images to clean up your dataset")
    else:
        print("✅ No visual duplicates found!")
    
    if failed_downloads:
        print(f"\n⚠️ Failed downloads ({len(failed_downloads)}):")
        for painting in failed_downloads[:5]:  # Show first 5
            print(f"  - {painting.get('title', 'Unknown')}: {painting.get('url', '')[:80]}...")

if __name__ == "__main__":
    main() 