# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: ATO_REALITY_SHIFT
# DETECTOR_SPEC_VERSION: 3.0-lite
# Interface: class Detector with method detect(text: str, lang: str='de') -> List[dict]
# Notes: Evidence strings are short snippets; span positions refer to character offsets.
import re
from typing import List, Optional, Tuple

class Detector:
    @staticmethod
    def _mk(hit_span: Optional[Tuple[int,int]], label: str, score: float, evidence: str):
        return {"span": hit_span, "label": label, "score": max(0.0, min(1.0, float(score))), "evidence": evidence}


    def detect(self, text: str, lang: str='de') -> List[dict]:
        t = text
        patt = re.compile(r"(Realität|Wahrheit|Fakten\s*vs\.\s*Gefühle|Narrativ|du\s+konstruierst|das\s+entspricht\s+nicht\s+der\s+Wahrheit|reality|truth|your\s+narrative)", re.I)
        hits = []
        for m in patt.finditer(t):
            hits.append(self._mk((m.start(), m.end()), "ATO_REALITY_SHIFT", 0.5, m.group(0)))
        return hits
