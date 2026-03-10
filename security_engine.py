import time
import threading

from download_monitor import start_download_monitor
from security.network_monitor import monitor_connections
from security.behavior_monitor import monitor_process_behavior
from security.ransomware_detector import monitor
from security.event_logger import log_event


engine_running = False


# ---------- NETWORK MONITOR ----------
def network_watch():

    while engine_running:

        try:

            alerts = monitor_connections()

            if alerts:
                for alert in alerts:
                    log_event("NETWORK", alert)

        except Exception as e:
            log_event("ERROR", f"Network monitor error: {str(e)}")

        time.sleep(5)


# ---------- PROCESS BEHAVIOR MONITOR ----------
def behavior_watch():

    while engine_running:

        try:

            alerts = monitor_process_behavior()

            if alerts:
                for alert in alerts:
                    log_event("BEHAVIOR", alert)

        except Exception as e:
            log_event("ERROR", f"Behavior monitor error: {str(e)}")

        time.sleep(10)


# ---------- RANSOMWARE MONITOR ----------
def ransomware_watch():

    try:

        log_event("SYSTEM", "Ransomware monitor started")

        monitor()

    except Exception as e:

        log_event("ERROR", f"Ransomware monitor error: {str(e)}")


# ---------- START ENGINE ----------
def start_security_engine():

    global engine_running

    engine_running = True

    log_event("SYSTEM", "Security engine started")

    # start download monitor
    start_download_monitor()

    # start monitors
    threading.Thread(target=network_watch, daemon=True).start()
    threading.Thread(target=behavior_watch, daemon=True).start()
    threading.Thread(target=ransomware_watch, daemon=True).start()


# ---------- STOP ENGINE ----------
def stop_security_engine():

    global engine_running

    engine_running = False

    log_event("SYSTEM", "Security engine stopped")