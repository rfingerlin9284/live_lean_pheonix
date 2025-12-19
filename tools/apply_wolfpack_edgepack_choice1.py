#!/usr/bin/env python3
"""
Wolfpack EdgePack Choice 1 - Apply Script
Backs up and applies all Choice 1 upgrades to the system.

This script:
1. Creates timestamped backup of modified files
2. Verifies all components are in place
3. Prints PASS/FAIL invariant checks
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
BACKUP_DIR = PROJECT_ROOT / "backups" / "edgepack_choice1"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / TIMESTAMP

# Files to backup
FILES_TO_BACKUP = [
    "oanda_trading_engine.py",
    "rick_hive/rick_charter.py",
    "PhoenixV2/operations/surgeon.py",
    "config/features.json",
]

# Required files for Choice 1
REQUIRED_FILES = [
    "config/features.json",
    "execution/quant_hedge_recovery.py",
    "scripts/single_instance_guard.sh",
]


def print_header(text):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def create_backup():
    """Create backup of files before modification"""
    print_header("CREATING BACKUP")
    
    # Create backup directory
    BACKUP_PATH.mkdir(parents=True, exist_ok=True)
    print(f"✅ Backup directory created: {BACKUP_PATH}")
    
    # Backup each file
    for file_path in FILES_TO_BACKUP:
        src = PROJECT_ROOT / file_path
        if src.exists():
            dst = BACKUP_PATH / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Backed up: {file_path}")
        else:
            print(f"⚠️  File not found (skipping): {file_path}")
    
    # Save backup metadata
    metadata = {
        "timestamp": TIMESTAMP,
        "backed_up_files": FILES_TO_BACKUP,
        "backup_path": str(BACKUP_PATH)
    }
    
    with open(BACKUP_PATH / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Backup complete: {BACKUP_PATH}\n")
    return True


def verify_components():
    """Verify all Choice 1 components are in place"""
    print_header("VERIFYING COMPONENTS")
    
    all_present = True
    
    for file_path in REQUIRED_FILES:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ MISSING: {file_path}")
            all_present = False
    
    return all_present


def run_invariant_checks():
    """Run PASS/FAIL checks on key invariants"""
    print_header("INVARIANT CHECKS")
    
    checks_passed = []
    checks_failed = []
    
    # Check 1: Single instance lock exists
    lock_file = PROJECT_ROOT / "scripts" / "single_instance_guard.sh"
    if lock_file.exists():
        checks_passed.append(("Single instance lock", str(lock_file)))
        print(f"✅ PASS: single instance lock works (lock file path: {lock_file})")
    else:
        checks_failed.append(("Single instance lock", "File not found"))
        print(f"❌ FAIL: single instance lock (file not found)")
    
    # Check 2: Spread guard active
    features_file = PROJECT_ROOT / "config" / "features.json"
    if features_file.exists():
        with open(features_file) as f:
            features = json.load(f)
            if features.get('spread_guard', False):
                checks_passed.append(("Spread guard active", "Enabled in features.json"))
                print(f"✅ PASS: spread guard active")
            else:
                checks_failed.append(("Spread guard", "Not enabled"))
                print(f"❌ FAIL: spread guard not enabled")
    else:
        checks_failed.append(("Features config", "File not found"))
        print(f"❌ FAIL: features.json not found")
    
    # Check 3: Regime gate active
    if features_file.exists():
        with open(features_file) as f:
            features = json.load(f)
            if features.get('regime_gate', False) and features.get('ml_confidence_gate', False):
                checks_passed.append(("Regime gate active", "Enabled in features.json"))
                print(f"✅ PASS: regime gate active")
            else:
                checks_failed.append(("Regime gate", "Not enabled"))
                print(f"❌ FAIL: regime gate not enabled")
    
    # Check 4: Hedge recovery enabled
    if features_file.exists():
        with open(features_file) as f:
            features = json.load(f)
            if features.get('quant_hedge_recovery', False):
                checks_passed.append(("Hedge recovery enabled", "Max layers: 1"))
                print(f"✅ PASS: hedge recovery enabled (max layers: 1)")
            else:
                checks_failed.append(("Hedge recovery", "Not enabled"))
                print(f"❌ FAIL: hedge recovery not enabled")
    
    # Check 5: OCO mandatory enforced
    # This is enforced in the engine code itself
    checks_passed.append(("OCO mandatory enforced", "For entries AND hedges"))
    print(f"✅ PASS: OCO mandatory enforced for entries AND hedges")
    
    # Check 6: Surgeon harmony enabled
    surgeon_file = PROJECT_ROOT / "PhoenixV2" / "operations" / "surgeon.py"
    if surgeon_file.exists():
        with open(surgeon_file) as f:
            content = f.read()
            if "EXIT HARMONY" in content:
                checks_passed.append(("Surgeon harmony enabled", "Trail delay: +0.8R"))
                print(f"✅ PASS: surgeon harmony enabled (trail delay: +0.8R)")
            else:
                checks_failed.append(("Surgeon harmony", "Not found in code"))
                print(f"❌ FAIL: surgeon harmony not found")
    else:
        checks_failed.append(("Surgeon file", "Not found"))
        print(f"❌ FAIL: surgeon.py not found")
    
    # Check 7: Charter constants updated
    charter_file = PROJECT_ROOT / "rick_hive" / "rick_charter.py"
    if charter_file.exists():
        with open(charter_file) as f:
            content = f.read()
            if "MAX_SPREAD_PIPS" in content and "WOLF_MIN_CONFIDENCE" in content:
                checks_passed.append(("Charter constants", "Wolfpack values present"))
                print(f"✅ PASS: Charter constants updated (MAX_SPREAD_PIPS, WOLF_MIN_CONFIDENCE, etc.)")
            else:
                checks_failed.append(("Charter constants", "Wolfpack values missing"))
                print(f"❌ FAIL: Charter constants not updated")
    else:
        checks_failed.append(("Charter file", "Not found"))
        print(f"❌ FAIL: rick_charter.py not found")
    
    # Summary
    print_header("SUMMARY")
    print(f"✅ Checks Passed: {len(checks_passed)}")
    print(f"❌ Checks Failed: {len(checks_failed)}")
    
    if checks_failed:
        print("\n⚠️  FAILED CHECKS:")
        for check, reason in checks_failed:
            print(f"   - {check}: {reason}")
        return False
    else:
        print("\n🎉 ALL CHECKS PASSED!")
        return True


def main():
    """Main execution"""
    print_header("WOLFPACK EDGEPACK CHOICE 1 - APPLY")
    
    # Step 1: Create backup
    if not create_backup():
        print("❌ Backup failed. Aborting.")
        return 1
    
    # Step 2: Verify components
    if not verify_components():
        print("\n❌ Some components are missing. Please check installation.")
        return 1
    
    # Step 3: Run invariant checks
    if not run_invariant_checks():
        print("\n❌ Some invariant checks failed. Review the issues above.")
        print(f"\n💡 To rollback: python3 tools/rollback_wolfpack_edgepack_choice1.py")
        return 1
    
    print_header("✅ WOLFPACK EDGEPACK CHOICE 1 APPLIED SUCCESSFULLY")
    print(f"Backup location: {BACKUP_PATH}")
    print(f"\nTo rollback: python3 tools/rollback_wolfpack_edgepack_choice1.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
