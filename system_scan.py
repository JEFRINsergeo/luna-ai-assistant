import psutil
import os


def get_running_processes():

    processes = []

    for proc in psutil.process_iter(['name']):
        try:
            processes.append(proc.info['name'])
        except:
            pass

    return processes[:10]


def scan_downloads():

    downloads = os.path.expanduser("~/Downloads")

    suspicious = []

    dangerous_extensions = [".exe", ".bat", ".ps1", ".vbs"]

    for file in os.listdir(downloads):

        for ext in dangerous_extensions:
            if file.endswith(ext):
                suspicious.append(file)

    return suspicious


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