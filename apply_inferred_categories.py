#!/usr/bin/env python3
"""
Apply inferred categories to the paintings data so the quiz can use them.
"""

import json
import os
from collections import defaultdict

def apply_inferred_categories():
    """Apply inferred categories to paintings data."""
    data_file = 'data/paintings_merged.json'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    # Load the paintings data
    with open(data_file, 'r', encoding='utf-8') as f:
        paintings = json.load(f)
    
    print(f"🎨 Applying Inferred Categories to Paintings")
    print(f"Total paintings: {len(paintings)}")
    print("-" * 60)
    
    # Known movements from the inference analysis
    known_movements = {
        'Edvard Munch': 'Expressionism',
        'Rolf Nesch': 'Expressionism',
        'Christian Krohg': 'Realism',
        'Amaldus Nielsen': 'Realism',
        'Frits Thaulow': 'Impressionism',
        'Peder Severin Krøyer': 'Impressionism',
        'Adolph Tidemand': 'Romantic Nationalism',
        'Oda Krohg': 'Kristiania Bohemians',
        'Christian Skredsvig': 'Neo-Romanticism',
        'Halfdan Egedius': 'Symbolism',
        'Ludvig Karsten': 'Pointillism'
    }
    
    # Inferred movements from the analysis
    inferred_movements = {
        # Impressionism (10 artists)
        'Asta Nørregaard': 'Impressionism',
        'Harald Sohlberg': 'Impressionism', 
        'Henrik Lund': 'Impressionism',
        'Martin Aagaard': 'Impressionism',
        'Nikolai Astrup': 'Impressionism',
        'Oluf Wold-Torne': 'Impressionism',
        'Søren Onsager': 'Impressionism',
        'Theodor Kittelsen': 'Impressionism',
        'Thorolf Holmboe': 'Impressionism',
        'Thorvald Erichsen': 'Impressionism',
        
        # Modernism (10 artists)
        'Axel Revold': 'Modernism',
        'Bjarne Ness': 'Modernism',
        'Hans Dahl': 'Modernism',
        'Henrik Sørensen': 'Modernism',
        'Håkon Bleken': 'Modernism',
        'Håkon Gullvåg': 'Modernism',
        'Olaf Gulbransson': 'Modernism',
        'Oscar Wergeland': 'Modernism',
        'Per Krohg': 'Modernism',
        'Vebjørn Sand': 'Modernism',
        
        # Neo-Classicism (6 artists)
        'Bernt Lund': 'Neo-Classicism',
        'Johan Christian Dahl': 'Neo-Classicism',
        'Johannes Flintoe': 'Neo-Classicism',
        'Knud Baade': 'Neo-Classicism',
        'Peder Aadnes': 'Neo-Classicism',
        'Thomas Fearnley': 'Neo-Classicism',
        
        # Realism (13 artists)
        'Carl Sundt-Hansen': 'Realism',
        'Eilif Peterssen': 'Realism',
        'Erik Werenskiold': 'Realism',
        'Eyolf Soot': 'Realism',
        'Gerhard Munthe': 'Realism',
        'Gunnar Berg': 'Realism',
        'Gustav Wentzel': 'Realism',
        'Harriet Backer': 'Realism',
        'Jacob Gløersen': 'Realism',
        'Kitty Lange Kielland': 'Realism',
        'Nils Gude': 'Realism',
        'Nils Hansteen': 'Realism',
        'Otto Sinding': 'Realism',
        
        # Romantic Nationalism (9 artists)
        'Adelsteen Normann': 'Romantic Nationalism',
        'August Cappelen': 'Romantic Nationalism',
        'Hans Gude': 'Romantic Nationalism',
        'Joachim Frich': 'Romantic Nationalism',
        'Johan Fredrik Eckersberg': 'Romantic Nationalism',
        'Lars Hertervig': 'Romantic Nationalism',
        'Morten Müller': 'Romantic Nationalism',
        'Peder Balke': 'Romantic Nationalism',
        'Peter Nicolai Arbo': 'Romantic Nationalism'
    }
    
    # Combine known and inferred movements
    all_movements = {**known_movements, **inferred_movements}
    
    # Apply categories to paintings
    updated_count = 0
    category_stats = defaultdict(int)
    
    for painting in paintings:
        artist = painting.get('artist', '')
        if not artist:
            continue
        
        # Get the inferred movement for this artist
        inferred_movement = all_movements.get(artist)
        
        if inferred_movement:
            # Initialize categories list if it doesn't exist
            if 'categories' not in painting:
                painting['categories'] = []
            
            # Add the inferred movement to categories if not already present
            if inferred_movement not in painting['categories']:
                painting['categories'].append(inferred_movement)
                updated_count += 1
                category_stats[inferred_movement] += 1
    
    print(f"Updated {updated_count} paintings with inferred categories")
    print()
    
    print("📊 Applied Categories Distribution:")
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"• {category}: {count} paintings")
    
    print()
    
    # Count artists per category
    artist_counts = defaultdict(set)
    for painting in paintings:
        artist = painting.get('artist', '')
        categories = painting.get('categories', [])
        for category in categories:
            artist_counts[category].add(artist)
    
    print("👨‍🎨 Artists per Category:")
    for category, artists in sorted(artist_counts.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"• {category}: {len(artists)} artists")
        if len(artists) <= 10:  # Show artist names for smaller categories
            print(f"  Artists: {', '.join(sorted(artists))}")
    
    # Save the updated data
    output_file = 'data/paintings_with_inferred_categories.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(paintings, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"✅ Updated data saved to: {output_file}")
    print()
    print("🎯 Quiz Categories Now Available:")
    print("• Full Collection: All paintings")
    print("• Popular Painters: Top 10 artists by painting count")
    print("• Landscape: Landscape paintings")
    print("• Realism: Realist movement (13 artists)")
    print("• Impressionism: Impressionist paintings (12 artists)")
    print("• Romantic Nationalism: Norwegian romantic nationalism (9 artists)")
    print("• Modernism: Modern works (10 artists)")
    print("• Female Artists: Female painters")

def main():
    apply_inferred_categories()

if __name__ == '__main__':
    main() 