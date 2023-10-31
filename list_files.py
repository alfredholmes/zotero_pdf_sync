from pathlib import Path


def get_files(dir_name, extension=".pdf"):
    files = list(Path(dir_name).rglob(f"*{extension}"))
    files = [f for f in files if '/.' not in str(f)]
    return files



