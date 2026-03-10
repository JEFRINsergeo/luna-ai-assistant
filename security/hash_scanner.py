import hashlib
import os

from security.event_logger import log_event


# ---------- KNOWN MALWARE HASHES ----------
# Example hashes (for testing)
KNOWN_MALWARE_HASHES = {
    "44d88612fea8a8f36de82e1278abb02f": "EICAR Test Virus"
}


# ---------- HASH CALCULATOR ----------
def get_file_hash(file_path, algorithm="md5"):

    try:

        if algorithm == "md5":
            hash_func = hashlib.md5()

        elif algorithm == "sha256":
            hash_func = hashlib.sha256()

        else:
            return None

        with open(file_path, "rb") as f:

            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()

    except Exception as e:

        log_event("ERROR", f"Hash scan failed for {file_path}: {str(e)}")
        return None


# ---------- HASH CHECK ----------
def check_file_hash(file_path):

    if not os.path.exists(file_path):
        return None

    file_hash = get_file_hash(file_path, "md5")

    if not file_hash:
        return None

    if file_hash in KNOWN_MALWARE_HASHES:

        threat = KNOWN_MALWARE_HASHES[file_hash]

        log_event("HASH", f"Known malware detected: {file_path} ({threat})")

        return {
            "risk": "HIGH",
            "threat": threat,
            "hash": file_hash
        }

    return {
        "risk": "LOW",
        "hash": file_hash
    }