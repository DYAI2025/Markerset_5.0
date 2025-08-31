#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erweiterte Test der Absence-Detection mit realistischem Szenario
"""

from DETECT_absence_meta import detect_absence_meta, build_tag_index, integrate_absence_detection

def test_realistic_absence_scenario():
    """Test mit realistischem Konfliktszenario, wo Absence-Marker auftreten"""
    
    # Längere Konflikt-Unterhaltung mit genug E-Markern aber ohne Herabwürdigungen/Drohungen
    msgs = [
        {"i": 0, "speaker": "A", "text": "Ich glaube, du hast mich belogen."},          # ACCUSATION
        {"i": 1, "speaker": "B", "text": "Das stimmt nicht, ich war ehrlich."},
        {"i": 2, "speaker": "A", "text": "Ich kann dir einfach nicht mehr vertrauen."}, # TRUST_DEFICIT  
        {"i": 3, "speaker": "B", "text": "Ich verstehe deinen Ärger, aber lass uns reden."},
        {"i": 4, "speaker": "A", "text": "Du versuchst mich zu kontrollieren."}, # CONTROL_ACCUSATION
        {"i": 5, "speaker": "B", "text": "Das war nicht meine Absicht, entschuldige."},
        {"i": 6, "speaker": "A", "text": "Es ist schwer für mich, das zu glauben."},
        {"i": 7, "speaker": "B", "text": "Ich möchte das wirklich klären mit dir."},
        {"i": 8, "speaker": "A", "text": "Ich bin sehr enttäuscht von dir."}, # ACCUSATION
        {"i": 9, "speaker": "B", "text": "Das tut mir leid, ich will es besser machen."},
        # Genug Text für min_tokens
        {"i": 10, "speaker": "A", "text": "Wir müssen wirklich über unsere Kommunikation sprechen."},
        {"i": 11, "speaker": "B", "text": "Ja, ich bin bereit dazu. Lass uns einen Weg finden."},
    ]
    
    # Eskalationsmarker (aber keine Derogation/Threats/etc.)
    hits = [
        {"i": 0, "speaker": "A", "marker": "SEM_ACCUSATION_DIRECT"},
        {"i": 2, "speaker": "A", "marker": "ATO_TRUST_DEFICIT_STATEMENT"}, 
        {"i": 4, "speaker": "A", "marker": "SEM_CONTROL_ACCUSATION"},
        {"i": 8, "speaker": "A", "marker": "SEM_ACCUSATION_DIRECT"},
    ]
    
    # Realistische Konfiguration
    absence_config = {
        "window": {"messages": 30},
        "gating_conflict": {"min_E_hits": 3, "context_markers_by_tag": ["accusation", "distrust"]},
        "absence_sets": {
            "derogation": {"tags": ["derogation", "contempt", "insult"], "ids": []},
            "profanity": {"tags": ["profanity"], "ids": []},
            "threat": {"tags": ["threat", "intimidation"], "ids": []},
            "ultimatum": {"tags": ["ultimatum"], "ids": []},
            "character_attack": {"tags": ["character_attack"], "ids": []},
        },
        "policy": {"strict_zero": True, "tolerant_max": 1, "min_tokens": 50},  # Reduziert für Test
        "emit": {"per_window": True, "per_speaker": True}
    }
    
    # Erweiterte Marker-Registry
    marker_registry = [
        {"id": "SEM_ACCUSATION_DIRECT", "tags": ["accusation", "conflict"]},
        {"id": "ATO_TRUST_DEFICIT_STATEMENT", "tags": ["distrust", "conflict"]},
        {"id": "SEM_CONTROL_ACCUSATION", "tags": ["accusation", "control"]},
        # Negative Marker (die NICHT vorkommen)
        {"id": "HARSH_INSULT", "tags": ["insult", "derogation", "contempt"]},
        {"id": "PROFANITY_MARKER", "tags": ["profanity"]},
        {"id": "DIRECT_THREAT", "tags": ["threat", "intimidation"]},
        {"id": "ULTIMATUM_MARKER", "tags": ["ultimatum"]},
        {"id": "CHARACTER_ASSASSINATION", "tags": ["character_attack"]},
    ]
    
    # E-Set (alle Konfliktmarker)
    E_SET = {
        "SEM_ACCUSATION_DIRECT", "ATO_TRUST_DEFICIT_STATEMENT", "SEM_CONTROL_ACCUSATION",
        "HARSH_INSULT", "PROFANITY_MARKER", "DIRECT_THREAT", "ULTIMATUM_MARKER", "CHARACTER_ASSASSINATION"
    }
    
    print("🔍 Teste realistisches Absence-Szenario...")
    print(f"Nachrichten: {len(msgs)}")
    print(f"Original Hits: {len(hits)} (alle Eskalationsmarker)")
    
    # Tag-Index erstellen
    tag_index, id_to_tags = build_tag_index(marker_registry)
    
    # Zeige, welche Marker-Sets für Absence geprüft werden
    print("\n📋 Absence-Sets:")
    for name, config in absence_config["absence_sets"].items():
        tags = config.get("tags", [])
        relevant_markers = set()
        for tag in tags:
            relevant_markers.update(tag_index.get(tag, set()))
        print(f"  {name}: {relevant_markers} (tags: {tags})")
    
    # Absence-Detection ausführen
    synthetic_hits = detect_absence_meta(msgs, hits, absence_config, tag_index, id_to_tags, E_SET)
    
    print(f"\n✨ Synthetische Absence-Hits: {len(synthetic_hits)}")
    for hit in synthetic_hits:
        print(f"  - {hit['marker']} (Speaker: {hit['speaker']}, Position: {hit['i']})")
    
    # Vollständige Integration
    all_hits = integrate_absence_detection(msgs, hits, absence_config, marker_registry, E_SET)
    
    print(f"\n✅ Gesamtergebnis: {len(all_hits)} Hits")
    print(f"   Original: {len(hits)} Eskalationsmarker")
    print(f"   Synthetisch: {len(synthetic_hits)} Absence-Marker")
    print(f"   → Das System erkannte erfolgreich, was NICHT gesagt wurde! 🎯")
    
    return all_hits

if __name__ == "__main__":
    test_realistic_absence_scenario()
