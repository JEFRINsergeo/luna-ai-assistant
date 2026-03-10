import os
import shutil

QUARANTINE_FOLDER = "quarantine"


def quarantine_file(file_path):

    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)

    filename = os.path.basename(file_path)

    new_path = os.path.join(QUARANTINE_FOLDER, filename)

    try:
        shutil.move(file_path, new_path)
        return f"File moved to quarantine: {filename}"

    except Exception as e:
        return str(e)