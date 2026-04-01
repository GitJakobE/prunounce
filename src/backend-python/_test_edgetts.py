import sys
sys.path.insert(0, ".")
from pathlib import Path
from app.services.tts import EdgeTTSProvider

p = EdgeTTSProvider()
tests = [
    ("figurati", "it-IT-GiuseppeMultilingualNeural"),
    ("ciao", "it-IT-DiegoNeural"),
    ("hyggelig", "da-DK-JeppeNeural"),
]
for word, voice in tests:
    out = Path(f"audio-cache/_test_{word}.mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    ok = p.generate(word, voice, out)
    print(f"{word!s:20} [{voice}]: ok={ok} size={out.stat().st_size if out.exists() else 0}")
    if out.exists():
        out.unlink()
