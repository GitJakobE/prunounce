import sys
sys.path.insert(0, ".")
from pathlib import Path
from app.services.tts import EdgeTTSProvider

p = EdgeTTSProvider()
out = Path("audio-cache/_test_ciao.mp3")
out.parent.mkdir(parents=True, exist_ok=True)
ok = p.generate("ciao", "it-IT-DiegoNeural", out)
print("generated:", ok, "| size:", out.stat().st_size if out.exists() else 0)
if out.exists():
    out.unlink()
print("done")
