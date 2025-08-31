# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: ATO_SLANG_TOKEN
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
        t_norm = re.sub(r"[’`´]", "'", text)  # normalize apostrophes
        t = t_norm
        tokens = [r"\bey\b", r"\balter\b", r"\blol\b", r"\bwtf\b", r"\bkp\b",
                  r"\bna\s*ja\b|\bnaja\b", r"\bbro\b", r"\btbh\b", r"\bidk\b",
                  r"\byikes\b", r"\bmeh\b", r"\bk'?\\b"]
        patt = re.compile("|".join(tokens), re.I)
        hits = []
        matches = list(patt.finditer(t))
        if not matches:
            return hits
        score = 0.4 if len(matches)==1 else min(0.8, 0.7 + 0.05*(len(matches)-2))
        for m in matches:
            hits.append(self._mk((m.start(), m.end()), "ATO_SLANG_TOKEN", score, m.group(0)))
        return hits
