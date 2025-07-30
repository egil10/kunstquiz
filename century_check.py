#!/usr/bin/env python3
"""
Check century distribution in the dataset.
"""

import json
import os
from collections import Counter

def check_centuries():
    """Check the distribution of paintings by century."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Century Analysis")
    print(f"Total paintings: {len(data)}")
    print("-" * 50)
    
    # Count by century
    century_counts = Counter()
    year_counts = Counter()
    
    for item in data:
        century = item.get('century', 'Unknown')
        year = item.get('year', 'Unknown')
        
        century_counts[century] += 1
        year_counts[year] += 1
    
    print("📅 Centuries by number of paintings:")
    print()
    
    # Sort centuries by count (descending)
    sorted_centuries = sorted(century_counts.items(), key=lambda x: x[1], reverse=True)
    
    for century, count in sorted_centuries:
        percentage = (count / len(data)) * 100
        print(f"• {century}: {count:4d} paintings ({percentage:5.1f}%)")
    
    print()
    print("📅 Year distribution (top 20):")
    print()
    
    # Sort years by count (descending)
    sorted_years = sorted(year_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (year, count) in enumerate(sorted_years[:20], 1):
        percentage = (count / len(data)) * 100
        print(f"{i:2d}. {year}: {count:4d} paintings ({percentage:5.1f}%)")
    
    # Check for 18th, 19th, 20th century presence
    print()
    print("🔍 Century Coverage:")
    centuries_present = set(century_counts.keys())
    
    if '18' in centuries_present or '1800s' in centuries_present:
        print("✅ 18th century: Present")
    else:
        print("❌ 18th century: Missing")
    
    if '19' in centuries_present or '1900s' in centuries_present:
        print("✅ 19th century: Present")
    else:
        print("❌ 19th century: Missing")
    
    if '20' in centuries_present or '2000s' in centuries_present:
        print("✅ 20th century: Present")
    else:
        print("❌ 20th century: Missing")
    
    if '21' in centuries_present or '2100s' in centuries_present:
        print("✅ 21st century: Present")
    else:
        print("❌ 21st century: Missing")

def main():
    check_centuries()

if __name__ == '__main__':
    main() 