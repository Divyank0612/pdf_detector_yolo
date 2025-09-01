import os
from pathlib import Path

def create_folders():
    folders = [
        "data/my_pdfs",
        "outputs/predictions",
        "outputs/json",
        "weights"
    ]
    for f in folders:
        Path(f).mkdir(parents=True, exist_ok=True)
    print("✅ Folder structure created!")

if __name__ == "__main__":
    create_folders()
