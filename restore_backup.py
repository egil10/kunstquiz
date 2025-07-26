#!/usr/bin/env python3
"""
Backup Restoration Script for Kunstquiz Data

This script helps restore data from backups if the filtering was too aggressive.
"""

import json
import os
import shutil
from datetime import datetime

def create_backup():
    """Create a backup of current data files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    files_to_backup = [
        'data/paintings_merged.json',
        'data/paintings_appended.json',
        'data/artist_bios.json',
        'data/artist_tags.json',
        'data/artist_tags_appended.json'
    ]
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backed up {file_path} to {backup_path}")
    
    return backup_dir

def list_backups():
    """List available backups"""
    backups = []
    for item in os.listdir('.'):
        if item.startswith('backup_') and os.path.isdir(item):
            backups.append(item)
    
    return sorted(backups, reverse=True)

def restore_backup(backup_dir):
    """Restore data from a backup"""
    if not os.path.exists(backup_dir):
        print(f"❌ Backup directory {backup_dir} not found")
        return False
    
    files_to_restore = [
        'paintings_merged.json',
        'paintings_appended.json',
        'artist_bios.json',
        'artist_tags.json',
        'artist_tags_appended.json'
    ]
    
    restored_count = 0
    for filename in files_to_restore:
        backup_path = os.path.join(backup_dir, filename)
        target_path = os.path.join('data', filename)
        
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, target_path)
            print(f"✅ Restored {filename}")
            restored_count += 1
        else:
            print(f"⚠️  {filename} not found in backup")
    
    return restored_count > 0

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup and restore Kunstquiz data')
    parser.add_argument('--create-backup', action='store_true',
                       help='Create a backup of current data')
    parser.add_argument('--list-backups', action='store_true',
                       help='List available backups')
    parser.add_argument('--restore', type=str,
                       help='Restore from backup directory (e.g., backup_20231201_143022)')
    
    args = parser.parse_args()
    
    if args.create_backup:
        backup_dir = create_backup()
        print(f"\n✅ Backup created: {backup_dir}")
        print("💡 To restore later, use: python restore_backup.py --restore " + backup_dir)
    
    elif args.list_backups:
        backups = list_backups()
        if backups:
            print("📁 Available backups:")
            for backup in backups:
                print(f"   {backup}")
        else:
            print("📁 No backups found")
    
    elif args.restore:
        if restore_backup(args.restore):
            print(f"\n✅ Successfully restored from {args.restore}")
            print("💡 Run diagnostics.py to check the restored data")
        else:
            print(f"\n❌ Failed to restore from {args.restore}")
    
    else:
        print("🔧 Usage:")
        print("  Create backup:  python restore_backup.py --create-backup")
        print("  List backups:   python restore_backup.py --list-backups")
        print("  Restore:        python restore_backup.py --restore backup_20231201_143022")

if __name__ == '__main__':
    main() 