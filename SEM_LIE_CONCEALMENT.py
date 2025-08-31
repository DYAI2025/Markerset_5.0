# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: SEM_LIE_CONCEALMENT
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
        # hedges / minimizers / avoidance (DE + EN)
        hedges = [
            r"\beigentlich\b", r"\bsozusagen\b", r"\bim\s*Grunde\b",
            r"\bnur\b", r"\bkaum\b", r"\bnicht\s*wirklich\b",
            r"\bvielleicht\b", r"\bungefähr\b", r"\bso\sbisschen\b",
            r"\bwenn\s*du\s*willst\b", r"\broughly\b", r"\bkinda\b", r"\bsort of\b"
        ]
        avoidance = [
            r"\bspäter\b", r"\bkein[e]? Details\b", r"\bkeine\s*Details\b",
            r"\bwill\s*nicht\s*(reden|darüber sprechen)\b", r"\bdarüber\s*möchte\s*ich\s*nicht\s*reden\b",
            r"\blass(\s*das)?\s*(Thema)?\b", r"\blass uns (nicht|mal)\b", r"\bchange of topic\b",
            r"\bdon't want to talk\b"
        ]
        patt = re.compile("|".join(hedges+avoidance), flags=re.I)
        hits = []
        for m in patt.finditer(t):
            ev = m.group(0)
            hits.append(self._mk((m.start(), m.end()), "SEM_LIE_CONCEALMENT", 0.4, ev))

        # Proximity boost: if 2+ matches within 80 chars, upgrade nearby scores
        positions = [ (h["span"][0], h["span"][1]) for h in hits if h["span"] ]
        for i in range(len(hits)):
            s_i = hits[i]["span"][0] if hits[i]["span"] else 0
            # check neighbors within 80 chars
            close = 0
            for j in range(len(hits)):
                if i==j or hits[j]["span"] is None: 
                    continue
                s_j = hits[j]["span"][0]
                if abs(s_i - s_j) <= 80:
                    close += 1
            if close >= 1:  # at least two within window total
                hits[i]["score"] = max(hits[i]["score"], 0.7 + min(0.25, 0.05*close))

        return hits
