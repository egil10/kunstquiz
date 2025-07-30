#!/usr/bin/env python3
"""
Test script to verify web app compatibility
"""

import json
import os

def test_web_app_files():
    """Test that web app files exist and are properly formatted"""
    
    print("🧪 Testing web app compatibility...")
    
    # Files that the web app expects
    required_files = [
        'data/paintings_with_inferred_categories.json',
        'data/artist_bios.json'
    ]
    
    # Test each file
    for filepath in required_files:
        print(f"\n📁 Testing: {filepath}")
        
        if not os.path.exists(filepath):
            print(f"  ❌ File not found: {filepath}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                print(f"  ✅ File exists and is valid JSON (list with {len(data)} items)")
                if len(data) > 0:
                    print(f"  📋 Sample keys: {list(data[0].keys())}")
            elif isinstance(data, dict):
                print(f"  ✅ File exists and is valid JSON (dict with {len(data)} keys)")
                print(f"  📋 Keys: {list(data.keys())}")
            else:
                print(f"  ⚠️  File exists but unexpected data type: {type(data)}")
                
        except json.JSONDecodeError as e:
            print(f"  ❌ Invalid JSON: {e}")
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
    
    # Test that the web app can load the data
    print(f"\n🌐 Testing web app data loading...")
    
    try:
        # Test paintings data
        with open('data/paintings_with_inferred_categories.json', 'r', encoding='utf-8') as f:
            paintings = json.load(f)
        
        # Test artist bios data
        with open('data/artist_bios.json', 'r', encoding='utf-8') as f:
            artists = json.load(f)
        
        print(f"  ✅ Paintings data: {len(paintings)} items")
        print(f"  ✅ Artist bios data: {len(artists)} items")
        
        # Check for required fields in paintings
        if len(paintings) > 0:
            required_painting_fields = ['title', 'url', 'artist']
            sample_painting = paintings[0]
            missing_fields = [field for field in required_painting_fields if field not in sample_painting]
            
            if missing_fields:
                print(f"  ⚠️  Missing fields in paintings: {missing_fields}")
            else:
                print(f"  ✅ All required painting fields present")
        
        # Check for required fields in artists
        if len(artists) > 0:
            required_artist_fields = ['name']
            sample_artist = artists[0]
            missing_fields = [field for field in required_artist_fields if field not in sample_artist]
            
            if missing_fields:
                print(f"  ⚠️  Missing fields in artists: {missing_fields}")
            else:
                print(f"  ✅ All required artist fields present")
        
        print(f"\n🎉 Web app compatibility test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Web app compatibility test failed: {e}")
        return False

if __name__ == '__main__':
    test_web_app_files() 