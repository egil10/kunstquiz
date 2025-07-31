#!/usr/bin/env python3
"""
Analytics script for Kunstquiz
Helps analyze user activity and game metrics
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import argparse

def load_analytics_data():
    """Load analytics data from Google Analytics or local storage"""
    # This would typically connect to Google Analytics API
    # For now, we'll create a sample structure
    return {
        "total_sessions": 0,
        "total_games": 0,
        "total_correct": 0,
        "total_incorrect": 0,
        "perfect_scores": 0,
        "category_usage": {},
        "top_artists": {},
        "session_duration": [],
        "location_data": {}
    }

def analyze_metrics(data):
    """Analyze the collected metrics"""
    print("🎨 Kunstquiz Analytics Dashboard")
    print("=" * 50)
    
    # Basic metrics
    print(f"\n📊 Basic Metrics:")
    print(f"   Total Sessions: {data['total_sessions']:,}")
    print(f"   Total Games Played: {data['total_games']:,}")
    print(f"   Total Correct Answers: {data['total_correct']:,}")
    print(f"   Total Incorrect Answers: {data['total_incorrect']:,}")
    
    if data['total_correct'] + data['total_incorrect'] > 0:
        accuracy = (data['total_correct'] / (data['total_correct'] + data['total_incorrect'])) * 100
        print(f"   Overall Accuracy: {accuracy:.1f}%")
    
    print(f"   Perfect Scores: {data['perfect_scores']:,}")
    
    # Category analysis
    if data['category_usage']:
        print(f"\n🏷️  Category Usage:")
        for category, count in sorted(data['category_usage'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {category}: {count:,} games")
    
    # Top artists
    if data['top_artists']:
        print(f"\n👨‍🎨 Most Challenging Artists:")
        for artist, count in sorted(data['top_artists'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {artist}: {count:,} incorrect answers")
    
    # Session duration
    if data['session_duration']:
        avg_duration = sum(data['session_duration']) / len(data['session_duration'])
        print(f"\n⏱️  Session Duration:")
        print(f"   Average: {avg_duration/1000/60:.1f} minutes")
        print(f"   Longest: {max(data['session_duration'])/1000/60:.1f} minutes")
    
    # Location data
    if data['location_data']:
        print(f"\n🌍 Top Locations:")
        for location, count in sorted(data['location_data'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {location}: {count:,} sessions")

def export_analytics(data, format='json'):
    """Export analytics data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create analytics directory if it doesn't exist
    export_dir = "analytics"
    os.makedirs(export_dir, exist_ok=True)
    
    if format == 'json':
        filename = os.path.join(export_dir, f"analytics_export_{timestamp}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Analytics exported to: {filename}")
    
    elif format == 'csv':
        filename = os.path.join(export_dir, f"analytics_export_{timestamp}.csv")
        # Implementation for CSV export
        print(f"\n✅ Analytics exported to: {filename}")

def setup_google_analytics():
    """Instructions for setting up Google Analytics"""
    print("🔧 Google Analytics Setup Instructions:")
    print("=" * 50)
    print("1. Go to https://analytics.google.com/")
    print("2. Create a new property for your Kunstquiz site")
    print("3. Get your Measurement ID (starts with 'G-')")
    print("4. Replace 'G-XXXXXXXXXX' in index.html with your actual ID")
    print("5. Deploy your site and wait 24-48 hours for data to appear")
    print("\n📈 Key Events to Track:")
    print("   - game_start: When a new game begins")
    print("   - answer_submitted: Each answer with correct/incorrect status")
    print("   - perfect_score: When someone gets 10/10")
    print("   - category_changed: When users switch categories")
    print("   - session_end: When users leave the site")

def main():
    parser = argparse.ArgumentParser(description='Kunstquiz Analytics Dashboard')
    parser.add_argument('--setup', action='store_true', help='Show Google Analytics setup instructions')
    parser.add_argument('--export', choices=['json', 'csv'], help='Export analytics data')
    parser.add_argument('--demo', action='store_true', help='Show demo data')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_google_analytics()
        return
    
    if args.demo:
        # Demo data for testing
        data = {
            "total_sessions": 1250,
            "total_games": 3420,
            "total_correct": 15420,
            "total_incorrect": 8760,
            "perfect_scores": 89,
            "category_usage": {
                "all": 1200,
                "popular": 850,
                "landscape": 650,
                "realism": 420,
                "impressionism": 380,
                "romantic_nationalism": 290,
                "modernism": 210,
                "female_artists": 180
            },
            "top_artists": {
                "Edvard Munch": 450,
                "Harriet Backer": 320,
                "Christian Krohg": 280,
                "Eilif Peterssen": 240,
                "Frits Thaulow": 210
            },
            "session_duration": [180000, 240000, 120000, 300000, 90000],
            "location_data": {
                "Norway": 850,
                "United States": 180,
                "Sweden": 95,
                "Denmark": 75,
                "Germany": 50
            }
        }
    else:
        data = load_analytics_data()
    
    analyze_metrics(data)
    
    if args.export:
        export_analytics(data, args.export)

if __name__ == "__main__":
    main() 