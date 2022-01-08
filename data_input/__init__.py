from pathlib import Path

current_path = Path(".")
datafolder = current_path / "data"
imagefolder = current_path / "images"

if not datafolder.exists():
    print(f"Creating {datafolder}/...")
    datafolder.mkdir()

if not imagefolder.exists():
    print(f"Creating {imagefolder}/...")
    imagefolder.mkdir()

print("Scaning root folder...")
for child in current_path.iterdir():
    if child.name == 'data.zip':
        print(f"Moving {child.name} to data/...")
        child.replace(datafolder / child.name)
print()
