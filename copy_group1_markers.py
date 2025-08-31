#!/usr/bin/env python3
"""
Copy Group 1 markers (FIXED_Marker_4.0) to local Downloads folder
"""
import os
import shutil
import pathlib
from pathlib import Path

# Source and destination paths
source_dir = "/Users/benjaminpoersch/:Users:benjaminpoersch:claude/_STARTING_/LeanDeep3.3_Marker_Backend/FIXED_Marker_4.0"
destination_dir = os.path.expanduser("~/Downloads/Group1_Markers")

def copy_group1_markers():
    """Copy all Group 1 markers to Downloads"""
    
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Zielordner: {destination_dir}")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"❌ Quellordner nicht gefunden: {source_dir}")
        return False
    
    # Find all .yaml files in source directory
    yaml_files = list(Path(source_dir).glob("*.yaml"))
    
    if not yaml_files:
        print(f"❌ Keine .yaml Dateien gefunden in: {source_dir}")
        return False
    
    print(f"📋 Gefunden: {len(yaml_files)} Group 1 Marker")
    
    # Copy each file
    copied_count = 0
    for yaml_file in yaml_files:
        try:
            destination_file = os.path.join(destination_dir, yaml_file.name)
            shutil.copy2(yaml_file, destination_file)
            print(f"✅ {yaml_file.name}")
            copied_count += 1
        except Exception as e:
            print(f"❌ Fehler beim Kopieren von {yaml_file.name}: {e}")
    
    print(f"\n🎉 {copied_count} Group 1 Marker erfolgreich kopiert!")
    print(f"📂 Ziel: {destination_dir}")
    
    # List copied files for verification
    print("\n📝 Kopierte Dateien:")
    for file in sorted(os.listdir(destination_dir)):
        if file.endswith('.yaml'):
            print(f"   • {file}")
    
    return True

if __name__ == "__main__":
    print("🚀 Kopiere Group 1 Marker (FIXED_Marker_4.0)...")
    success = copy_group1_markers()
    
    if success:
        print(f"\n✅ Vorgang abgeschlossen!")
        print(f"📁 Alle Group 1 Marker sind jetzt in: {destination_dir}")
    else:
        print(f"\n❌ Fehler beim Kopieren der Marker")
