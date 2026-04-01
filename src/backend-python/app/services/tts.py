from abc import ABC, abstractmethod
import asyncio
from pathlib import Path
import re
import time
from typing import Final

import edge_tts

from ..config import settings


class TTSProvider(ABC):
    @abstractmethod
    def generate(self, text: str, voice_name: str, output_path: Path, *, slow: bool = False, rate: str | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def generate_bytes(self, text: str, voice_name: str, *, slow: bool = False, rate: str | None = None) -> bytes | None:
        raise NotImplementedError


class EdgeTTSProvider(TTSProvider):
    """Microsoft Edge neural TTS — high-quality, no API key required."""

    _MAX_RETRIES = 4
    _RETRY_DELAYS = (0.5, 1.0, 2.0, 4.0)

    def generate(
        self,
        text: str,
        voice_name: str,
        output_path: Path,
        *,
        slow: bool = False,
        rate: str | None = None,
    ) -> bool:
        try:
            audio_bytes = self.generate_bytes(text, voice_name, slow=slow, rate=rate)
            if not audio_bytes:
                output_path.unlink(missing_ok=True)
                return False
            output_path.write_bytes(audio_bytes)
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as exc:
            print(f"EdgeTTS generation failed for '{text}' (voice={voice_name}): {exc}")
            output_path.unlink(missing_ok=True)
            return False

    def generate_bytes(
        self,
        text: str,
        voice_name: str,
        *,
        slow: bool = False,
        rate: str | None = None,
    ) -> bytes | None:
        effective_rate = rate if rate is not None else ("-30%" if slow else "+0%")
        last_error: Exception | None = None
        for attempt in range(self._MAX_RETRIES):
            try:
                async def _run() -> bytes:
                    communicate = edge_tts.Communicate(text, voice_name, rate=effective_rate)
                    chunks = bytearray()
                    async for message in communicate.stream():
                        if message["type"] == "audio":
                            chunks.extend(message["data"])
                    return bytes(chunks)

                audio_bytes = asyncio.run(_run())
                return audio_bytes or None
            except Exception as exc:
                last_error = exc
                if attempt < self._MAX_RETRIES - 1:
                    time.sleep(self._RETRY_DELAYS[min(attempt, len(self._RETRY_DELAYS) - 1)])

        print(f"EdgeTTS generation failed for '{text}' (voice={voice_name}): {last_error}")
        return None


DEFAULT_VOICE: Final[str] = "it-IT-GiuseppeMultilingualNeural"
PROVIDER: TTSProvider = EdgeTTSProvider()


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^a-z0-9àèéìòùæøåäöüß]", "_", value.lower())


def get_audio_path(filename_key: str, text: str | None = None, host_id: str | None = None, voice_name: str | None = None) -> Path | None:
    host_suffix = f"_{host_id}" if host_id else ""
    filename = f"{sanitize_filename(filename_key)}{host_suffix}.mp3"
    cache_dir = Path(settings.audio_cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    file_path = cache_dir / filename

    if file_path.exists():
        return file_path

    # Single-word pronunciations (text is None) are slowed down for learner clarity.
    # Example sentences (text is provided) play at normal speed.
    is_word = text is None
    ok = PROVIDER.generate(
        text or filename_key,
        voice_name or DEFAULT_VOICE,
        file_path,
        slow=is_word,
    )
    return file_path if ok and file_path.exists() else None
