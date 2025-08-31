# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: ATO_EMO_HIGH_VALENCE_MARKER
# DETECTOR_SPEC_VERSION: 3.0-lite
# Interface: class Detector with method detect(text: str, lang: str='de') -> List[dict]
# Notes: Evidence strings are short snippets; span positions refer to character offsets.
import re
from typing import List, Optional, Tuple

class Detector:
    @staticmethod
    def _mk(hit_span: Optional[Tuple[int,int]], label: str, score: float, evidence: str):
        return {"span": hit_span, "label": label, "score": max(0.0, min(1.0, float(score))), "evidence": evidence}


def _allcaps_tokens(text: str):
    toks = re.findall(r"[A-ZÄÖÜ]{3,}", text)
    return toks

    def detect(self, text: str, lang: str='de') -> List[dict]:
        t = text
        hits = []
        exclam = list(re.finditer(r"!{2,}", t))
        caps = _allcaps_tokens(t)
        intens = list(re.finditer(r"\b(extrem|unglaublich|absolut|vollkommen|mega|heftig)\b", t, re.I))

        signals = len(exclam) + len(caps) + len(intens)
        if signals == 0:
            return hits

        # Consolidated score + per-signal evidences
        score = 0.4 if signals==1 else 0.7 + 0.05*min(5, signals-2)  # cap ~0.95
        score = min(0.95, score)
        hits.append(self._mk(None, "ATO_EMO_HIGH_VALENCE_MARKER", score, f"signals={signals}"))

        for m in exclam[:4]:
            hits.append(self._mk((m.start(), m.end()), "ATO_EMO_HIGH_VALENCE_MARKER", min(0.5, score), m.group(0)))
        for w in caps[:4]:
            pos = t.find(w)
            hits.append(self._mk((pos, pos+len(w)), "ATO_EMO_HIGH_VALENCE_MARKER", min(0.5, score), w))
        for m in intens[:4]:
            hits.append(self._mk((m.start(), m.end()), "ATO_EMO_HIGH_VALENCE_MARKER", min(0.5, score), m.group(0)))
        return hits
