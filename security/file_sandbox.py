import hashlib
import os

SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".ps1", ".sh"]


def scan_file(file_path):

    result = {}

    if not os.path.exists(file_path):
        return {"status": "file not found"}

    size = os.path.getsize(file_path)

    ext = os.path.splitext(file_path)[1]

    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    result["size"] = size
    result["extension"] = ext
    result["sha256"] = file_hash

    if ext.lower() in SUSPICIOUS_EXTENSIONS:
        result["risk"] = "HIGH"
    else:
        result["risk"] = "LOW"

    return result