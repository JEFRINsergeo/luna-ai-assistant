import re

SUSPICIOUS_PATTERNS = [
    r"powershell.*download",
    r"cmd.exe.*curl",
    r"wget\s+http",
    r"base64\s+-d",
    r"chmod\s+\+x",
    r"nc\s+-e",
]

def detect_malware_patterns(text):

    threats = []

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text.lower()):
            threats.append(pattern)

    return threats