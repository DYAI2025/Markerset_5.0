#!/usr/bin/env python3
"""
LeanDeep 3.3 Enhanced Bundle Demonstration
Shows the corrected marker structure with _id, display_title, conflict_gating, etc.
"""

import json
import yaml
from pathlib import Path

def demonstrate_corrected_markers():
    """Show the corrected marker structure following your specifications."""
    
    print("=== LeanDeep 3.3 Enhanced Marker Structure ===")
    print()
    
    # Load a corrected marker example
    corrected_files = [
        "markers/ato/ATO_CARE_PING_corrected.yaml",
        "markers/sem/SEM_MAINTENANCE_RITUAL_corrected.yaml", 
        "markers/clu/CLU_NEEDINESS_GUILT_BIND_corrected.yaml",
        "markers/mema/MEMA_ABSENCE_OF_DEROGATION_IN_CONFLICT_corrected.yaml"
    ]
    
    for file_path in corrected_files:
        if Path(file_path).exists():
            print(f"📄 {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                marker = yaml.safe_load(f)
            
            print(f"   ID: {marker.get('id', 'N/A')}")
            print(f"   Display Title: {marker.get('display_title', 'N/A')}")
            print(f"   Category: {marker.get('id', '').split('_')[0] if marker.get('id') else 'N/A'}")
            print(f"   Detection Class: {marker.get('detect_class', 'pattern')}")
            print(f"   Tags: {marker.get('tags', [])}")
            
            # Show key improvements
            if marker.get('pattern'):
                print(f"   Pattern Count: {len(marker['pattern'])}")
                print(f"   Pattern Sample: {marker['pattern'][0][:50]}...")
            elif marker.get('composed_of'):
                print(f"   Composed Of: {marker['composed_of']}")
            elif marker.get('detect_class') == 'absence_meta':
                print(f"   Absence Target: {marker.get('criteria', {}).get('target_set', 'N/A')}")
            
            print()

def demonstrate_conflict_gating():
    """Show the conflict_gating configuration."""
    
    print("=== Conflict Gating Configuration ===")
    
    # Load the generated sets config
    sets_config_path = "out_bundle/sets_config.json"
    if Path(sets_config_path).exists():
        with open(sets_config_path, 'r', encoding='utf-8') as f:
            sets_config = json.load(f)
        
        conflict_gating = sets_config.get('conflict_gating', {})
        print(f"Window: {conflict_gating.get('window', {}).get('messages', 'N/A')} messages")
        print(f"Min E-hits: {conflict_gating.get('min_E_hits', 'N/A')}")
        print(f"Purpose: SOFORT konflikt-gated Omission rechnen")
        print()
        
        # Show marker classification examples
        print("Marker Classification Examples:")
        print("E (Escalation):")
        print("  - SEM_VICTIM_OFFENDER_REVERSAL")
        print("  - CLU_NEEDINESS_GUILT_BIND") 
        print("  - SEM_GUILT_APPEAL_NEEDINESS")
        print()
        print("D (Deescalation):")
        print("  - MEMA_ABSENCE_OF_DEROGATION_IN_CONFLICT")
        print("  - ATO_CARE_PING")
        print("  - SEM_MAINTENANCE_RITUAL")
        print()

def demonstrate_enhanced_features():
    """Show the enhanced features implemented."""
    
    print("=== Enhanced Features Implemented ===")
    print()
    
    features = [
        ("✅ Robust YAML Processing", "Gracefully handles syntax errors with --skip-bad-yaml"),
        ("✅ Flexible Pattern Recognition", "Accepts pattern/patterns/pattern_examples variants"),
        ("✅ Auto-Derived Display Titles", "Creates display_title from frame.concept → frame.signal[0] → id"),
        ("✅ Version Normalization", "Supports 3.3.x versions with --accept-version-prefix 3.3"),
        ("✅ MongoDB Compatibility", "Supports _id field alongside id"),
        ("✅ Conflict Gating", "Includes conflict_gating configuration for MEMA markers"),
        ("✅ Enhanced CLI", "Multiple validation modes and configuration options"),
        ("✅ Updated Timestamps", "Automatic updated_at field generation"),
        ("✅ Improved Regex Patterns", "Word boundaries \\b, hyphen variants, additional synonyms"),
        ("✅ Better Examples", "Multi-line examples for CLU markers showing component interaction")
    ]
    
    for feature, description in features:
        print(f"{feature}")
        print(f"   {description}")
        print()

def show_bundle_stats():
    """Show current bundle statistics."""
    
    print("=== Current Bundle Statistics ===")
    
    schema_bundle_path = "out_bundle/schema_full_bundle.json"
    if Path(schema_bundle_path).exists():
        with open(schema_bundle_path, 'r', encoding='utf-8') as f:
            bundle = json.load(f)
        
        metadata = bundle.get('metadata', {})
        markers = bundle.get('markers', {})
        
        print(f"Bundle Type: {metadata.get('bundle_type')}")
        print(f"Version: {metadata.get('version')}")
        print(f"Total Markers: {metadata.get('total_markers')}")
        print(f"Bundle Hash: {metadata.get('bundle_hash')}")
        print(f"LeanDeep 3.3 Compliant: {bundle.get('validation', {}).get('leandeep33_compliant', False)}")
        print()
        
        # Count by category
        by_category = {}
        for marker_id in markers.keys():
            category = marker_id.split('_')[0]
            by_category[category] = by_category.get(category, 0) + 1
        
        print("Markers by Category:")
        for category, count in sorted(by_category.items()):
            print(f"  {category}: {count}")
        print()

def main():
    """Main demonstration function."""
    
    print("🎯 LeanDeep 3.3 Enhanced Bundle System")
    print("=" * 50)
    print()
    
    demonstrate_enhanced_features()
    demonstrate_corrected_markers()
    demonstrate_conflict_gating()
    show_bundle_stats()
    
    print("🎉 All requested improvements have been implemented!")
    print()
    print("Key Changes:")
    print("- Added conflict_gating to sets_config for MEMA omission detection")
    print("- Enhanced marker structure with display_title and _id support")
    print("- Improved regex patterns with word boundaries and hyphen variants")
    print("- Better examples for CLU markers showing component interactions")
    print("- MongoDB-compatible field structure")
    print("- Robust validation with graceful error handling")

if __name__ == "__main__":
    main()
