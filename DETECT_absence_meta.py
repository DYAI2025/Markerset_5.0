# DETECT_absence_meta.py
import math
from collections import defaultdict, Counter

def _collect_by_window(msgs, hits, win):
    # einfache Blockfenster; ihr könnt euren Rolling-Mechanismus nutzen
    n = len(msgs); i = 0
    while i < n:
        j = min(n, i+win)
        seg_msgs = msgs[i:j]
        seg_hits = [h for h in hits if i <= h["i"] < j]
        yield (i, j, seg_msgs, seg_hits)
        i = j

def _by_speaker(hits):
    per = defaultdict(list)
    for h in hits: per[h["speaker"]].append(h)
    return per

def detect_absence_meta(msgs, hits, cfg, tag_index, id_to_tags, E_SET):
    """
    msgs: [{i, speaker, text}], hits: [{i, speaker, marker}]
    cfg: absence_meta_config (dict)
    tag_index: tag -> set(marker_ids)  (aus euren YAMLs/Bundle ableitbar)
    id_to_tags: marker_id -> set(tags)
    E_SET: set der Eskalationsmarker
    return: list synthetischer Hits [{i, speaker, marker}]
    """
    out = []
    W = int(cfg.get("window", {}).get("messages", 30))
    min_E = int(cfg.get("gating_conflict", {}).get("min_E_hits", 3))
    strict_zero = bool(cfg.get("policy", {}).get("strict_zero", True))
    tolerant_max = int(cfg.get("policy", {}).get("tolerant_max", 1))
    min_tokens = int(cfg.get("policy", {}).get("min_tokens", 200))

    # Vorbereitete Sets je Abwesenheitsgruppe
    def resolve_set(entry):
        s = set(entry.get("ids", []))
        for t in entry.get("tags", []):
            s |= set(tag_index.get(t, set()))
        return s

    ABS = {name: resolve_set(entry) for name, entry in (cfg.get("absence_sets") or {}).items()}

    for i, j, seg_msgs, seg_hits in _collect_by_window(msgs, hits, W):
        # Gating: Konfliktkontext aktiv?
        E_hits = [h for h in seg_hits if h["marker"] in E_SET]
        if len(E_hits) < min_E: 
            continue

        # genug Text?
        token_est = sum(len(m["text"].split()) for m in seg_msgs)
        if token_est < min_tokens:
            continue

        # markiere, dass dies ein Konfliktfenster war (für Cluster)
        out.append({"i": j-1, "speaker": "WINDOW", "marker": "CONFLICT_CONTEXT"})

        # Abwesenheiten prüfen (per Window)
        mcount = Counter([h["marker"] for h in seg_hits])
        for abs_name, abs_set in ABS.items():
            present = sum(mcount[m] for m in abs_set)
            ok = (present == 0) if strict_zero else (present <= tolerant_max)
            if ok:
                marker_id = f"MEMA_ABSENCE_OF_{abs_name.upper()}_IN_CONFLICT"
                out.append({"i": j-1, "speaker": "BOTH", "marker": marker_id})

        # Per-Speaker-Varianten
        if cfg.get("emit", {}).get("per_speaker", True):
            by_sp = _by_speaker(seg_hits)
            # Beteiligung: mind. 2 Nachrichten im Fenster
            participation = Counter([m["speaker"] for m in seg_msgs])
            min_participation = 2  # Default-Wert
            
            # Versuche min_participation aus verschiedenen Config-Pfaden zu lesen
            try:
                min_participation = int(cfg.get("meta", {}).get("min_participation_msgs", 2))
            except (KeyError, AttributeError, TypeError):
                try:
                    min_participation = int(cfg.get("policy", {}).get("min_participation_msgs", 2))
                except (KeyError, AttributeError, TypeError):
                    min_participation = 2
            
            for spk, shits in by_sp.items():
                if participation.get(spk, 0) < min_participation:
                    continue
                scount = Counter([h["marker"] for h in shits])
                for abs_name, abs_set in ABS.items():
                    present = sum(scount[m] for m in abs_set)
                    ok = (present == 0) if strict_zero else (present <= tolerant_max)
                    if ok:
                        marker_id = f"MEMA_SPKR_ABSENCE_OF_{abs_name.upper()}_IN_CONFLICT"
                        out.append({"i": j-1, "speaker": spk, "marker": marker_id})
    return out


def build_tag_index(marker_data):
    """
    Hilfsfunktion: Erstelle tag -> set(marker_ids) Index aus Marker-Daten
    marker_data: Liste von Marker-Dictionaries mit 'id' und 'tags' Feldern
    """
    tag_index = defaultdict(set)
    id_to_tags = {}
    
    for marker in marker_data:
        mid = marker.get("id")
        tags = marker.get("tags", [])
        if mid:
            id_to_tags[mid] = set(tags)
            for tag in tags:
                tag_index[tag].add(mid)
    
    return dict(tag_index), id_to_tags


def integrate_absence_detection(msgs, hits, absence_config, marker_registry, E_SET):
    """
    Vollständige Integration: lädt Config, erstellt Indices, führt Detection aus
    
    msgs: Liste der Chat-Nachrichten
    hits: Liste der bisherigen Marker-Hits
    absence_config: Dict aus absence_meta_config.yaml
    marker_registry: Dict/Liste aller verfügbaren Marker mit Tags
    E_SET: Set der Eskalations-Marker-IDs
    
    Returns: erweiterte hits-Liste mit synthetischen Absence-Markern
    """
    # Tag-Index erstellen
    if isinstance(marker_registry, dict):
        # Falls Registry als {id: marker_data} Dict vorliegt
        marker_list = list(marker_registry.values())
    else:
        # Falls bereits als Liste vorliegt
        marker_list = marker_registry
    
    tag_index, id_to_tags = build_tag_index(marker_list)
    
    # Absence-Detection durchführen
    synthetic_hits = detect_absence_meta(msgs, hits, absence_config, tag_index, id_to_tags, E_SET)
    
    # Originale und synthetische Hits kombinieren
    return hits + synthetic_hits
