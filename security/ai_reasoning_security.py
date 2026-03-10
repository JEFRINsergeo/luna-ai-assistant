def analyze_behavior(process_list):

    suspicious_keywords = [
        "miner",
        "keylogger",
        "rat",
        "trojan",
        "inject"
    ]

    alerts = []

    for proc in process_list:

        name = proc.lower()

        for keyword in suspicious_keywords:

            if keyword in name:
                alerts.append(f"Suspicious process behavior: {proc}")

    return alerts