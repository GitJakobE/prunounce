import sys
sys.path.insert(0, ".")
from pathlib import Path
from app.services.tts import EdgeTTSProvider

p = EdgeTTSProvider()
voices = [
    ("marco",  "it-IT-DiegoNeural"),
    ("giulia", "it-IT-IsabellaNeural"),
    ("luca",   "it-IT-GiuseppeMultilingualNeural"),
    ("sofia",  "it-IT-ElsaNeural"),
    ("anders", "da-DK-JeppeNeural"),
    ("freja",  "da-DK-ChristelNeural"),
]
for host, voice in voices:
    out = Path(f"audio-cache/_test_{host}.mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    ok = p.generate("ciao", voice, out)
    size = out.stat().st_size if out.exists() else 0
    print(f"{host:8} {voice}: ok={ok} size={size}")
    if out.exists(): out.unlink()
