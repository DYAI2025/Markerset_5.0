# Auto-generated on 2025-08-14T05:18:20Z
# Detector ID: SEM_IDEALIZATION_DEVALUATION
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
        pos = re.compile(r"(perfekt|einzigartig|bester\s+mensch|so\s+gut\s+für\s+mich|am\s+besten|wundervoll|amazing|perfect|the\s+best)", re.I)
        neg = re.compile(r"(lächerlich|absurd|schrecklich|hasse|furchtbar|disgusting|ridiculous|hate)", re.I)

        hits = []
        for m_pos in pos.finditer(t):
            s0 = m_pos.start()
            window = (max(0, s0-120), min(len(t), s0+120))
            m_neg = neg.search(t[window[0]:window[1]])
            if m_neg:
                # compute global span
                ngs = window[0] + m_neg.start()
                nge = window[0] + m_neg.end()
                ev = t[m_pos.start():m_pos.end()] + " … " + t[ngs:nge]
                hits.append(self._mk((min(m_pos.start(), ngs), max(m_pos.end(), nge)), "SEM_IDEALIZATION_DEVALUATION", 0.85, ev))
        return hits
