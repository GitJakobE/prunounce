import sys
sys.path.insert(0, ".")
from pathlib import Path
from app.services.tts import EdgeTTSProvider

p = EdgeTTSProvider()
out = Path("audio-cache/_test_figurati_slow.mp3")
out.parent.mkdir(exist_ok=True)
ok = p.generate("figurati", "it-IT-GiuseppeMultilingualNeural", out, slow=True)
print("figurati (slow):", ok, "| size:", out.stat().st_size if out.exists() else 0)
if out.exists(): out.unlink()
