import os
import shutil


def add_to_startup(exe_path):

    startup_folder = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )

    try:

        if os.path.exists(startup_folder):

            file_name = os.path.basename(exe_path)
            destination = os.path.join(startup_folder, file_name)

            if not os.path.exists(destination):

                shutil.copy(exe_path, destination)
                print("Luna added to startup")

            else:

                print("Luna already in startup")

    except Exception as e:

        print("Startup error:", e)