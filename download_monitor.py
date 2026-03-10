import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from security.hash_scanner import check_file_hash
from security.event_logger import log_event


# ---------- DOWNLOAD FOLDER ----------
DOWNLOAD_FOLDER = os.path.expanduser("~/Downloads")


# ---------- DANGEROUS FILE TYPES ----------
dangerous_extensions = [
    ".exe",
    ".bat",
    ".ps1",
    ".vbs",
    ".scr",
    ".cmd"
]


# ---------- ALERT STORAGE ----------
alerts = []


class DownloadHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        try:

            file_path = event.src_path
            file_name = os.path.basename(file_path)

            ext = os.path.splitext(file_name)[1].lower()

            # ---------- EXECUTABLE DETECTION ----------
            if ext in dangerous_extensions:

                message = f"⚠ Executable file downloaded: {file_name}"
                alerts.append(message)

                log_event("DOWNLOAD", f"Executable download detected: {file_path}")

            # ---------- HASH SCAN ----------
            result = check_file_hash(file_path)

            if result and result.get("risk") == "HIGH":

                threat = result.get("threat", "Unknown malware")

                message = f"🚨 Malware detected: {file_name} ({threat})"

                alerts.append(message)

                log_event("MALWARE", f"{threat} detected in {file_path}")

            # ---------- LIMIT ALERT SIZE ----------
            if len(alerts) > 50:
                alerts.pop(0)

        except Exception as e:

            log_event("ERROR", f"Download monitor error: {str(e)}")


# ---------- START MONITOR ----------
def start_download_monitor():

    event_handler = DownloadHandler()
    observer = Observer()

    if os.path.exists(DOWNLOAD_FOLDER):

        observer.schedule(event_handler, DOWNLOAD_FOLDER, recursive=False)
        observer.start()

        log_event("SYSTEM", "Download monitor started")

    else:

        log_event("ERROR", "Downloads folder not found")

    return observer


# ---------- GET ALERTS ----------
def get_download_alerts():

    return alerts