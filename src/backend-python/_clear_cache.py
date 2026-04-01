import pathlib
cache = pathlib.Path(r"c:\code\prunounce\src\backend-python\audio-cache")
files = [f for f in cache.glob("*.mp3") if not f.name.startswith("_test")]
print(f"Removing {len(files)} cached audio files...")
for f in files:
    f.unlink()
print("Done")
