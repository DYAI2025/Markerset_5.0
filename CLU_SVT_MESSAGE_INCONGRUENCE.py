# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: CLU_SVT_MESSAGE_INCONGRUENCE
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
        claim = re.compile(r"(selten|kaum|1[\-–]2\s*[x×/]\s*monat|einmal\s+im\s+monat|rarely|seldom)", re.I)
        ritual = re.compile(r"(wie\s+üblich|wie\s+immer|fix|vereinbart|wöchentlich|regelmäßig|morgen|nächste\s*woche|call|termin|meeting)", re.I)

        has_claim = bool(claim.search(t))
        ritual_hits = list(ritual.finditer(t))

        hits = []
        if has_claim and len(ritual_hits) >= 2:
            # Emit one strong hit
            hits.append(self._mk(None, "CLU_SVT_MESSAGE_INCONGRUENCE", 0.9, "claim+>=2 ritual signals"))
        return hits
