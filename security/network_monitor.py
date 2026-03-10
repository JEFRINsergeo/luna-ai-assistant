import psutil


def monitor_connections():

    suspicious = []

    for conn in psutil.net_connections(kind="inet"):

        if conn.raddr:

            ip = conn.raddr.ip
            port = conn.raddr.port

            if port in [4444, 5555, 6666, 1337]:
                suspicious.append(f"Suspicious port connection: {ip}:{port}")

    return suspicious