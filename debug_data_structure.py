#!/usr/bin/env python3
"""
Debug script to examine the data structure and find why categories are Unknown.
"""

import json
import os

def debug_data_structure():
    """Examine the data structure to understand the category issue."""
    data_file = 'data/paintings_appended.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Data Structure Analysis")
    print(f"Total paintings: {len(data)}")
    print("-" * 50)
    
    # Examine first few items
    print("🔍 First 3 items structure:")
    for i, item in enumerate(data[:3], 1):
        print(f"\nItem {i}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
    
    # Check what fields exist
    print(f"\n📋 All available fields in the dataset:")
    all_fields = set()
    for item in data:
        all_fields.update(item.keys())
    
    for field in sorted(all_fields):
        print(f"  • {field}")
    
    # Check for category-like fields
    print(f"\n🎨 Looking for category-related fields:")
    category_fields = [field for field in all_fields if 'category' in field.lower() or 'type' in field.lower() or 'genre' in field.lower()]
    
    if category_fields:
        for field in category_fields:
            unique_values = set()
            for item in data:
                value = item.get(field, '')
                if value:
                    unique_values.add(str(value))
            
            print(f"  • {field}: {len(unique_values)} unique values")
            if len(unique_values) <= 10:
                print(f"    Values: {sorted(unique_values)}")
    else:
        print("  No obvious category fields found!")
    
    # Check for any field that might contain category info
    print(f"\n🔍 Checking all fields for potential category data:")
    for field in sorted(all_fields):
        if field not in ['artist', 'title', 'url', 'year', 'image_url']:  # Skip obvious non-category fields
            unique_values = set()
            for item in data:
                value = item.get(field, '')
                if value and str(value).strip():
                    unique_values.add(str(value).strip())
            
            if 1 < len(unique_values) <= 20:  # Reasonable number for categories
                print(f"  • {field}: {len(unique_values)} values - {sorted(unique_values)}")

def main():
    debug_data_structure()

if __name__ == '__main__':
    main() 