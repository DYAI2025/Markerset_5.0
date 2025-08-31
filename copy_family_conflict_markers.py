#!/usr/bin/env python3
"""
Copy all Family/Conflict markers from project/markers/ to local Downloads folder
"""
import os
import shutil
import pathlib
from pathlib import Path

# Source and destination paths
project_markers_dir = "/Users/benjaminpoersch/:Users:benjaminpoersch:claude/_STARTING_/LeanDeep3.3_Marker_Backend/project/markers"
destination_dir = os.path.expanduser("~/Downloads/Family_Conflict_Markers")

def copy_family_conflict_markers():
    """Copy all Family/Conflict markers from project/markers to Downloads"""
    
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Zielordner: {destination_dir}")
    
    # Check if source directory exists
    if not os.path.exists(project_markers_dir):
        print(f"❌ Quellordner nicht gefunden: {project_markers_dir}")
        return False
    
    # Find all .yaml files in all subdirectories
    yaml_files = []
    for subdir in ['ato', 'sem', 'clu', 'mema']:
        subdir_path = Path(project_markers_dir) / subdir
        if subdir_path.exists():
            yaml_files.extend(list(subdir_path.glob("*.yaml")))
    
    if not yaml_files:
        print(f"❌ Keine .yaml Dateien gefunden in: {project_markers_dir}")
        return False
    
    print(f"📋 Gefunden: {len(yaml_files)} Familie/Konflikt-Marker")
    
    # Create subdirectories in destination
    for subdir in ['ato', 'sem', 'clu', 'mema']:
        os.makedirs(os.path.join(destination_dir, subdir), exist_ok=True)
    
    # Copy each file maintaining directory structure
    copied_count = 0
    copied_by_category = {'ato': 0, 'sem': 0, 'clu': 0, 'mema': 0}
    
    for yaml_file in yaml_files:
        try:
            # Determine category from parent directory
            category = yaml_file.parent.name
            destination_file = os.path.join(destination_dir, category, yaml_file.name)
            
            shutil.copy2(yaml_file, destination_file)
            print(f"✅ {category}/{yaml_file.name}")
            copied_count += 1
            copied_by_category[category] += 1
        except Exception as e:
            print(f"❌ Fehler beim Kopieren von {yaml_file.name}: {e}")
    
    print(f"\n🎉 {copied_count} Familie/Konflikt-Marker erfolgreich kopiert!")
    print(f"📂 Ziel: {destination_dir}")
    
    # Show summary by category
    print(f"\n📊 Übersicht nach Kategorien:")
    for category, count in copied_by_category.items():
        if count > 0:
            print(f"   • {category.upper()}: {count} Marker")
    
    # List some example files for verification
    print(f"\n📝 Beispiel-Dateien:")
    for subdir in ['ato', 'sem', 'clu', 'mema']:
        subdir_path = os.path.join(destination_dir, subdir)
        if os.path.exists(subdir_path):
            files = [f for f in os.listdir(subdir_path) if f.endswith('.yaml')]
            if files:
                print(f"   📂 {subdir.upper()}:")
                for file in sorted(files)[:3]:  # Show first 3 files
                    print(f"      • {file}")
                if len(files) > 3:
                    print(f"      ... und {len(files) - 3} weitere")
    
    return True

if __name__ == "__main__":
    print("🚀 Kopiere Familie/Konflikt-Marker aus project/markers/...")
    success = copy_family_conflict_markers()
    
    if success:
        print(f"\n✅ Vorgang abgeschlossen!")
        print(f"📁 Alle Familie/Konflikt-Marker sind jetzt in: {destination_dir}")
        print(f"📁 Group 1 Marker sind in: ~/Downloads/Group1_Markers")
    else:
        print(f"\n❌ Fehler beim Kopieren der Marker")
