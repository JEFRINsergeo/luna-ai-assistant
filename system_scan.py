import psutil
import os
from pathlib import Path


def get_running_processes():

    processes = []

    for proc in psutil.process_iter(['name']):
        try:
            processes.append(proc.info['name'])
        except:
            pass

    return processes[:10]


def scan_downloads():

    try:
        downloads = str(Path.home() / "Downloads")

        if not os.path.exists(downloads):
            return []

        suspicious = []

        for file in os.listdir(downloads):

            if file.endswith(".exe") or file.endswith(".bat"):
                suspicious.append(file)

        return suspicious

    except Exception:
        return []


def scan_installed_apps():

    programs = []

    program_paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]

    for path in program_paths:

        if os.path.exists(path):

            for app in os.listdir(path):
                programs.append(app)

    return programs[:15]


def run_full_scan():

    return {
        "running_processes": get_running_processes(),
        "suspicious_downloads": scan_downloads(),
        "installed_apps": scan_installed_apps()
    }