import psutil


def check_usb_devices():

    devices = []

    for part in psutil.disk_partitions():

        if "removable" in part.opts:
            devices.append(part.device)

    return devices