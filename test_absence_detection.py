#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test der Absence-Detection Integration
"""

import sys
from pathlib import Path
import yaml
import json

# Import der Module
from DETECT_absence_meta import detect_absence_meta, build_tag_index, integrate_absence_detection

def test_absence_detection():
    """Einfacher Test der Absence-Detection"""
    
    # Test-Nachrichten mit Konflikt
    msgs = [
        {"i": 0, "speaker": "A", "text": "Du lügst die ganze Zeit!"},
        {"i": 1, "speaker": "B", "text": "Das stimmt nicht, ich bin ehrlich."},
        {"i": 2, "speaker": "A", "text": "Ich kann dir nicht mehr vertrauen."},
        {"i": 3, "speaker": "B", "text": "Ich verstehe deine Sorge, lass uns darüber reden."},
        {"i": 4, "speaker": "A", "text": "Du manipulierst mich ständig."},
        {"i": 5, "speaker": "B", "text": "Das tut mir leid, ich möchte das klären."},
    ]
    
    # Test-Hits (simulierte Eskalationsmarker)
    hits = [
        {"i": 0, "speaker": "A", "marker": "SEM_ACCUSATION_DIRECT"},
        {"i": 2, "speaker": "A", "marker": "ATO_TRUST_DEFICIT_STATEMENT"},
        {"i": 4, "speaker": "A", "marker": "SEM_ACCUSATION_DIRECT"},
    ]
    
    # Test-Konfiguration
    absence_config = {
        "window": {"messages": 30},
        "gating_conflict": {"min_E_hits": 3},
        "absence_sets": {
            "derogation": {"tags": ["insult", "contempt"], "ids": ["HARSH_INSULT"]},
            "threat": {"tags": ["threat"], "ids": ["DIRECT_THREAT"]},
        },
        "policy": {"strict_zero": True, "min_tokens": 50},
        "emit": {"per_window": True, "per_speaker": True}
    }
    
    # Test-Marker-Registry
    marker_registry = [
        {"id": "SEM_ACCUSATION_DIRECT", "tags": ["accusation"]},
        {"id": "ATO_TRUST_DEFICIT_STATEMENT", "tags": ["distrust"]},
        {"id": "HARSH_INSULT", "tags": ["insult", "derogation"]},
        {"id": "DIRECT_THREAT", "tags": ["threat"]},
    ]
    
    # E-Set (Eskalationsmarker)
    E_SET = {"SEM_ACCUSATION_DIRECT", "ATO_TRUST_DEFICIT_STATEMENT", "HARSH_INSULT", "DIRECT_THREAT"}
    
    # Tag-Index erstellen
    tag_index, id_to_tags = build_tag_index(marker_registry)
    
    print("🔍 Teste Absence-Detection...")
    print(f"Tag-Index: {dict(tag_index)}")
    print(f"Original Hits: {len(hits)}")
    
    # Absence-Detection ausführen
    synthetic_hits = detect_absence_meta(msgs, hits, absence_config, tag_index, id_to_tags, E_SET)
    
    print(f"Synthetische Hits: {len(synthetic_hits)}")
    for hit in synthetic_hits:
        print(f"  - {hit['marker']} (Speaker: {hit['speaker']}, Position: {hit['i']})")
    
    # Vollständige Integration testen
    all_hits = integrate_absence_detection(msgs, hits, absence_config, marker_registry, E_SET)
    
    print(f"\n✅ Gesamtergebnis: {len(all_hits)} Hits ({len(hits)} original + {len(synthetic_hits)} synthetisch)")
    return all_hits

if __name__ == "__main__":
    test_absence_detection()
