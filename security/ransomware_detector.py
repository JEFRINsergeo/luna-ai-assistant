import os
import time

from security.event_logger import log_event


# ---------- CONFIG ----------
WATCH_FOLDER = os.path.expanduser("~/Documents")

SUSPICIOUS_EXTENSIONS = [
    ".locked",
    ".encrypted",
    ".crypto",
    ".crypt",
    ".locky",
    ".enc",
    ".aes",
    ".vault"
]

# Folders to ignore
IGNORE_FOLDERS = [
    "AppData",
    "Windows",
    "Program Files",
    "Program Files (x86)"
]

# Mass change threshold
MASS_CHANGE_LIMIT = 40


# ---------- FILE SNAPSHOT ----------
def scan_files():

    file_data = {}

    for root, dirs, files in os.walk(WATCH_FOLDER):

        # Skip ignored folders
        if any(ignore.lower() in root.lower() for ignore in IGNORE_FOLDERS):
            continue

        for file in files:

            path = os.path.join(root, file)

            try:
                file_data[path] = os.path.getmtime(path)
            except:
                continue

    return file_data


# ---------- MASS CHANGE DETECTOR ----------
def detect_mass_changes(old, new):

    changes = 0

    for file in new:

        if file not in old:
            changes += 1

        elif new[file] != old[file]:
            changes += 1

    if changes > MASS_CHANGE_LIMIT:

        log_event(
            f"Mass file modification detected ({changes} files changed)",
            level="RANSOMWARE"
        )

        return True

    return False


# ---------- EXTENSION DETECTOR ----------
def detect_suspicious_extensions(files):

    suspicious = []

    for file in files:

        for ext in SUSPICIOUS_EXTENSIONS:

            if file.lower().endswith(ext):
                suspicious.append(file)

    if suspicious:

        log_event(
            f"Suspicious encrypted files detected: {len(suspicious)}",
            level="RANSOMWARE"
        )

    return suspicious


# ---------- ALERT ----------
def alert_user(message):

    print("\n⚠️  RANSOMWARE ALERT ⚠️")
    print(message)
    print("Take action immediately!\n")

    log_event(message, level="RANSOMWARE")


# ---------- MAIN MONITOR ----------
def monitor():

    global previous_files

    print("🛡 Luna Ransomware Protection Started")
    print("Monitoring:", WATCH_FOLDER)

    previous_files = scan_files()

    while True:

        try:

            time.sleep(5)

            current_files = scan_files()

            # Detect mass file modifications
            if detect_mass_changes(previous_files, current_files):

                alert_user("Large number of file changes detected!")

            # Detect suspicious extensions
            suspicious = detect_suspicious_extensions(current_files.keys())

            if len(suspicious) > 5:

                alert_user("Multiple encrypted files detected!")

                for s in suspicious[:5]:
                    print("Detected:", s)

            previous_files = current_files

        except Exception as e:

            log_event(
                f"Ransomware monitor error: {str(e)}",
                level="ERROR"
            )


# ---------- RUN ----------
if __name__ == "__main__":
    monitor()