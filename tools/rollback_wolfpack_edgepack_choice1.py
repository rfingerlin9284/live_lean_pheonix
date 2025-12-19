#!/usr/bin/env python3
"""
Wolfpack EdgePack Choice 1 - Rollback Script
Restores files from the last backup snapshot.
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
BACKUP_DIR = PROJECT_ROOT / "backups" / "edgepack_choice1"


def print_header(text):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def find_latest_backup():
    """Find the most recent backup"""
    if not BACKUP_DIR.exists():
        return None
    
    # List all backup directories
    backups = [d for d in BACKUP_DIR.iterdir() if d.is_dir()]
    
    if not backups:
        return None
    
    # Sort by name (timestamp) and get the latest
    backups.sort(reverse=True)
    return backups[0]


def restore_backup(backup_path):
    """Restore files from backup"""
    print_header(f"RESTORING FROM BACKUP: {backup_path}")
    
    # Load metadata
    metadata_file = backup_path / "metadata.json"
    if not metadata_file.exists():
        print("❌ Backup metadata not found. Cannot restore.")
        return False
    
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    backed_up_files = metadata.get('backed_up_files', [])
    
    # Restore each file
    restored_count = 0
    for file_path in backed_up_files:
        src = backup_path / file_path
        dst = PROJECT_ROOT / file_path
        
        if src.exists():
            # Create parent directory if needed
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Restore file
            shutil.copy2(src, dst)
            print(f"✅ Restored: {file_path}")
            restored_count += 1
        else:
            print(f"⚠️  Backup file not found (skipping): {file_path}")
    
    print(f"\n✅ Restored {restored_count} files from backup")
    return True


def disable_features():
    """Disable Choice 1 features in config"""
    print_header("DISABLING CHOICE 1 FEATURES")
    
    features_file = PROJECT_ROOT / "config" / "features.json"
    
    if features_file.exists():
        with open(features_file) as f:
            features = json.load(f)
        
        # Disable all Choice 1 features
        features['wolfpack_edgepack_choice1'] = False
        features['regime_gate'] = False
        features['ml_confidence_gate'] = False
        features['spread_guard'] = False
        features['cost_logging'] = False
        features['single_instance_guard'] = False
        features['quant_hedge_recovery'] = False
        features['surgeon_exit_harmony'] = False
        
        with open(features_file, 'w') as f:
            json.dump(features, f, indent=2)
        
        print("✅ All Choice 1 features disabled in config/features.json")
    else:
        print("⚠️  Features config not found (skipping)")
    
    return True


def main():
    """Main execution"""
    print_header("WOLFPACK EDGEPACK CHOICE 1 - ROLLBACK")
    
    # Find latest backup
    latest_backup = find_latest_backup()
    
    if not latest_backup:
        print("❌ No backups found. Cannot rollback.")
        print(f"   Backup directory: {BACKUP_DIR}")
        return 1
    
    print(f"📦 Latest backup found: {latest_backup.name}")
    
    # Ask for confirmation
    response = input("\n⚠️  This will restore files from backup. Continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Rollback cancelled.")
        return 0
    
    # Restore backup
    if not restore_backup(latest_backup):
        print("\n❌ Rollback failed.")
        return 1
    
    # Disable features
    disable_features()
    
    print_header("✅ ROLLBACK COMPLETE")
    print(f"Files restored from: {latest_backup}")
    print(f"\nChoice 1 features have been disabled.")
    print(f"Restart the trading engine for changes to take effect.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
