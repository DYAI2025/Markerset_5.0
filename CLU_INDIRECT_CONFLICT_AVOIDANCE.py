# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: CLU_INDIRECT_CONFLICT_AVOIDANCE
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
        shift = [r"\banderes\s+Thema\b", r"\begal\s+jetzt\b", r"\blass\s+gut\s+sein\b", r"\bnicht\s+der\s+richtige\s+Moment\b"]
        mini  = [r"\bkein\s+Drama\b", r"\bnicht\s+so\s+wichtig\b", r"\bhalb\s+so\s+wild\b"]
        defer = [r"\bspäter\b", r"\manderswann\b", r"\bnot\s+now\b"]

        patt_shift = re.compile("|".join(shift), re.I)
        patt_mini  = re.compile("|".join(mini), re.I)
        patt_defer = re.compile("|".join(defer), re.I)

        hits = []
        ms = list(patt_shift.finditer(t))
        mm = list(patt_mini.finditer(t))
        md = list(patt_defer.finditer(t))

        # Conditions: any shift → hit; OR minimization + defer → hit
        if ms:
            for m in ms:
                hits.append(self._mk((m.start(), m.end()), "CLU_INDIRECT_CONFLICT_AVOIDANCE", 0.7, m.group(0)))
        if mm and md:
            # combine into one consolidated hit
            hits.append(self._mk(None, "CLU_INDIRECT_CONFLICT_AVOIDANCE", 0.75, "minimization+defer"))

        # single weak signals
        if (mm and not md) or (md and not mm):
            for m in (mm or md):
                hits.append(self._mk((m.start(), m.end()), "CLU_INDIRECT_CONFLICT_AVOIDANCE", 0.45, m.group(0)))

        return hits
