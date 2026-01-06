"""
Privacy Guard
Handles PII detection, masking, and audit logging
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple


class PrivacyGuard:
    def __init__(self):
        self.patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "XXX-XX-XXXX"),
            (r"\b\d{9}\b", "XXXXXXXXX"),
            (r"\b(?:\d{4}[- ]?){3}\d{4}\b", "XXXX-XXXX-XXXX-XXXX"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.\w+\b", "[EMAIL REDACTED]"),
            (r"\b\d{10}\b", "XXXXXXXXXX")
        ]

        self.blocked_terms = [
            "hack", "steal", "bypass", "unauthorized", "exploit"
        ]

    def clean_input(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def scan_query(self, text: str, context: Dict) -> List[Dict]:
        findings = []
        for word in self.blocked_terms:
            if word in text.lower():
                findings.append({"severity": "critical", "term": word})
        return findings

    def mask_sensitive_data(self, text: str, role: str) -> Tuple[str, List[Dict]]:
        log = []
        output = text
        for pattern, replacement in self.patterns:
            matches = list(re.finditer(pattern, output))
            if matches:
                for m in matches:
                    log.append({"value": m.group(), "mask": replacement})
                output = re.sub(pattern, replacement, output)
        return output, log

    def log_event(self, context: Dict, query: str, response: str, redactions: List[Dict]) -> Dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "user": context.get("user_id"),
            "query_hash": self._hash(query),
            "response_hash": self._hash(response),
            "redactions": len(redactions)
        }

    def apply_disclaimers(self, response: str, context: Dict) -> str:
        return response + "\n\n*This information is confidential and for authorized use only.*"

    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()[:16]
