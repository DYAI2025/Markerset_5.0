# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: CLU_SUSTAINED_CONTACT
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
        routine = [
            r"\bimmer\b", r"\bjeden(s)?\b", r"\bregelmäßig\b", r"\bwöchentlich\b", r"\btäglich\b",
            r"\bwie\s+besprochen\b", r"\bwie\s+üblich\b", r"\bfix\b", r"\bvereinbart\b"
        ]
        when = [
            # weekdays/time anchors (DE/EN)
            r"\bmontags?\b", r"\bdienstags?\b", r"\bmittwochs?\b", r"\bdonnerstags?\b", r"\bfreitags?\b",
            r"\bsamstags?\b", r"\bsonntags?\b",
            r"\bmorgen\b", r"\bnächste\s*woche\b", r"\bübermorgen\b",
            r"\b\d{1,2}[:.]\d{2}\b", r"\b20\s*Uhr\b", r"\bpm\b", r"\bam\b"
        ]
        call_words = [r"\bcall\b", r"\btermin\b", r"\bmeeting\b", r"\bslot\b", r"\bcheck\-in\b"]

        patt_any = re.compile("|".join(routine+when+call_words), re.I)
        matches = list(patt_any.finditer(t))
        hits = []
        if not matches:
            return hits

        # Count signals and check if (>=2) OR (>=1 and has concrete time/weekday)
        count_total = len(matches)
        has_time = bool(re.search("|".join(when), t, re.I))
        label = "CLU_SUSTAINED_CONTACT"

        # Emit one consolidated hit plus small per-token hits for evidence density
        # Consolidated score
        if count_total >= 2 or (count_total>=1 and has_time):
            base = 0.45 + 0.15*min(4, count_total)  # 1→0.60, 2→0.75, 3→0.90, 4+→1.05 capped
            score = max(0.5, min(0.95, base))
            # consolidated
            hits.append(self._mk(None, label, score, "density:"+str(count_total)))

        # per-token evidences (lower score to avoid double-counting)
        for m in matches[:6]:  # cap evidences
            hits.append(self._mk((m.start(), m.end()), label, min(0.5, 0.3 + 0.05*count_total), m.group(0)))

        return hits
