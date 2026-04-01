import sys
sys.path.insert(0, ".")
from pathlib import Path
from app.services.tts import GttsTTSProvider

p = GttsTTSProvider()
out = Path("audio-cache/_test_gtts_it.mp3")
out.parent.mkdir(parents=True, exist_ok=True)

ok = p.generate("Ciao, come stai?", "it-IT-DiegoNeural", out)
print("Italian:", ok, "| size:", out.stat().st_size if out.exists() else 0)
if out.exists(): out.unlink()

out2 = Path("audio-cache/_test_gtts_da.mp3")
ok2 = p.generate("Hej, hvordan har du det?", "da-DK-JeppeNeural", out2)
print("Danish: ", ok2, "| size:", out2.stat().st_size if out2.exists() else 0)
if out2.exists(): out2.unlink()
