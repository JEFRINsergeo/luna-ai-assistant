import os


def create_file(path, content):

    folder = os.path.dirname(path)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(path, "w") as f:
        f.write(content)

    return f"File created: {path}"