# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: ATO_ORGANISATION_ENTITY
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
        patt = re.compile(r"\b(GmbH|UG|AG|HRB)\b|(?:\bFirma\b|\bHolding\b|\bAmtsgericht\b|\bXING\b|\bLinkedIn\b)|\b[a-z0-9\-]+\.(de|com|org|io)\b", re.I)
        hits = []
        for m in patt.finditer(t):
            hits.append(self._mk((m.start(), m.end()), "ATO_ORGANISATION_ENTITY", 0.5, m.group(0)))
        return hits
