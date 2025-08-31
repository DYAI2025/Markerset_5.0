# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: SEM_MIRRORING_REQUEST
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
        lex = [
            r"\bbenenn(e|st)?\b", r"\bspiegle?\b",
            r"sag\s+mir,\s*was\s+du\s+(willst|fühlst|denkst)\b",
            r"kannst\s+du\s+das\s+klar\s+sagen\?",
            r"\btell\s+me\s+what\s+you\s+(want|feel|think)\b",
            r"\bname\s+it\b", r"\bbe\s+transparent\b"
        ]
        patt = re.compile("|".join(lex), re.I)
        matches = list(patt.finditer(t))
        hits = []
        if not matches:
            return hits
        # scoring: multiple prompts → higher
        s = 0.4 + 0.15*min(4, len(matches))  # 1→0.55, 2→0.70, 3→0.85, 4+→1.00→cap
        s = min(0.9, s)
        for m in matches:
            hits.append(self._mk((m.start(), m.end()), "SEM_MIRRORING_REQUEST", s if len(matches)>1 else 0.5, m.group(0)))
        return hits
