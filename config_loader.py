"""
config_loader.py – Lean-Deep 3.4 konformer Konfigurationslader für Marker-Definitionen.
"""

import json
import yaml
import re
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
import logging
from dataclasses import dataclass, field

# ----- Konstante Präfixe und Kategorisierung gemäß LD3.4 -----
PRFX_LEVELS = {
    "ATO_": "atomic",
    "SEM_": "semantic",
    "CLU_": "cluster",
    "MEMA_": "meta"
}

REQUIRED_FRAME_KEYS = ["signal", "concept", "pragmatics", "narrative"]

logger = logging.getLogger(__name__)

@dataclass
class Frame:
    signal: Union[str, List[str]]
    concept: str
    pragmatics: str
    narrative: str

@dataclass
class MarkerDefinition:
    id: str
    frame: Frame
    pattern: Optional[List[str]] = field(default=None)
    composed_of: Optional[List[str]] = field(default=None)
    detect_class: Optional[str] = None
    activation: Optional[Dict[str, Any]] = field(default=None)
    scoring: Optional[Dict[str, Any]] = field(default=None)
    tags: Optional[List[str]] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    window: Optional[Dict[str, Any]] = field(default=None)
    lang: Optional[str] = None
    description: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    active: bool = True

# --------- Präfix- und Kategorielogik ---------
def validate_marker_id(marker_id: str) -> str:
    if not marker_id or not any(marker_id.startswith(p) for p in PRFX_LEVELS):
        raise ValueError(f"Marker-ID '{marker_id}' fehlt 4-Letter-Präfix")
    return marker_id

def migrate_marker_id(old_id: str) -> str:
    if old_id.startswith(("A_", "S_", "C_", "MM_")):
        return {"A_":"ATO_", "S_":"SEM_", "C_":"CLU_", "MM_":"MEMA_"}[old_id[:2]] + old_id[2:]
    return old_id

def parse_category_from_id(marker_id: str) -> str:
    for prfx, category in PRFX_LEVELS.items():
        if marker_id.startswith(prfx):
            return category
    return "uncategorized"

def check_required_fields(data: dict):
    # id, frame und examples sind Pflicht (nach LD3.2)
    missing = []
    if not data.get('id'):
        missing.append("id")
    if not data.get('frame'):
        missing.append("frame")
    else:
        for key in REQUIRED_FRAME_KEYS:
            if key not in data['frame']:
                missing.append(f"frame.{key}")
    if not data.get('examples') or not isinstance(data.get('examples'), list) or len(data['examples']) < 1:
        missing.append("examples")
    if not (data.get('pattern') or data.get('composed_of') or data.get('detect_class')):
        missing.append("pattern|composed_of|detect_class (mind. eins)")
    if missing:
        raise ValueError(f"Pflichtfelder fehlen oder unvollständig: {', '.join(missing)}")

# --------- Haupt-Konfiguration ---------
@dataclass
class MarkerConfig:
    marker_directories: List[Path] = field(default_factory=lambda: [Path("markers")])
    auto_reload: bool = True
    cache_enabled: bool = True

class MarkerLoader:
    def __init__(self, config: Optional[MarkerConfig] = None):
        self.config = config or MarkerConfig()
        self._markers: Dict[str, MarkerDefinition] = {}

    def load_all_markers(self) -> Dict[str, MarkerDefinition]:
        self._markers.clear()
        for directory in self.config.marker_directories:
            if not directory.exists():
                logger.warning(f"Marker-Verzeichnis existiert nicht: {directory}")
                continue

            logger.info(f"Suche Marker in: {directory}")
            yaml_files = list(directory.glob("**/*.yaml"))
            json_files = list(directory.glob("**/*.json"))
            txt_files  = list(directory.glob("**/*.txt"))

            for f in yaml_files:
                try:
                    markers = self.load_yaml_markers(f)
                    self._merge_markers(markers)
                except Exception as e:
                    logger.error(f"Fehler beim Laden von {f}: {e}")
            for f in json_files:
                try:
                    markers = self.load_json_markers(f)
                    self._merge_markers(markers)
                except Exception as e:
                    logger.error(f"Fehler beim Laden von {f}: {e}")
            for f in txt_files:
                try:
                    markers = self.load_txt_markers(f)
                    self._merge_markers(markers)
                except Exception as e:
                    logger.error(f"Fehler beim Laden von {f}: {e}")
        logger.info(f"Gesamt {len(self._markers)} Marker geladen")
        return self._markers

    def load_yaml_markers(self, filepath: Path) -> List[MarkerDefinition]:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and 'markers' in data:
            marker_list = data['markers']
        elif isinstance(data, list):
            marker_list = data
        elif isinstance(data, dict):
            marker_list = [data]
        else:
            raise ValueError(f"Unerwartetes YAML-Format in {filepath}")

        return [self._parse_marker_data(md) for md in marker_list if md]

    def load_json_markers(self, filepath: Path) -> List[MarkerDefinition]:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'markers' in data:
            marker_list = data['markers']
        elif isinstance(data, list):
            marker_list = data
        elif isinstance(data, dict):
            marker_list = [data]
        else:
            raise ValueError(f"Unerwartetes JSON-Format in {filepath}")

        return [self._parse_marker_data(md) for md in marker_list if md]

    def load_txt_markers(self, filepath: Path) -> List[MarkerDefinition]:
        # Sehr einfacher Parser für Legacy-Formate!
        markers = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 4:
                    logger.warning(f"Zeile {line_num} in {filepath} hat ungültiges Format")
                    continue
                marker_id = migrate_marker_id(parts[0])
                validate_marker_id(marker_id)
                frame = Frame(signal=parts[2], concept="n/a", pragmatics="n/a", narrative="n/a")
                patterns = [p.strip() for p in parts[3].split(',')]
                m = MarkerDefinition(
                    id=marker_id, frame=frame, pattern=patterns, examples=[],
                    tags=[], description=f"TXT legacy Marker aus {filepath.name}"
                )
                markers.append(m)
        return markers

    def _parse_marker_data(self, data: Dict[str, Any]) -> MarkerDefinition:
        marker_id = migrate_marker_id(data.get('id', data.get('marker_id')))
        validate_marker_id(marker_id)

        # Pflichtfeld-Check (löst Fehler wenn etwas nicht stimmt)
        check_required_fields(data)

        # Frame konstruieren
        frame_data = data['frame']
        frame = Frame(
            signal=frame_data['signal'],
            concept=frame_da_
