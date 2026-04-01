import fs from "fs";
import path from "path";
import { MsEdgeTTS, OUTPUT_FORMAT } from "msedge-tts";
import { config } from "../config.js";

const DEFAULT_VOICE = "it-IT-DiegoNeural";

// Ensure cache directory exists
if (!fs.existsSync(config.audioCacheDir)) {
  fs.mkdirSync(config.audioCacheDir, { recursive: true });
}

function sanitizeFilename(word: string): string {
  return word.toLowerCase().replace(/[^a-z0-9àèéìòùæøåäöüß]/g, "_");
}

export async function getAudioPath(
  filenameKey: string,
  text?: string,
  hostId?: string,
  voiceName?: string
): Promise<string | null> {
  const hostSuffix = hostId ? `_${hostId}` : "";
  const filename = `${sanitizeFilename(filenameKey)}${hostSuffix}.mp3`;
  const filePath = path.join(config.audioCacheDir, filename);

  if (fs.existsSync(filePath)) {
    return filePath;
  }

  try {
    const voice = voiceName || DEFAULT_VOICE;
    const tts = new MsEdgeTTS();
    await tts.setMetadata(voice, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);
    // msedge-tts v2 toFile() takes a directory and creates audio.mp3 inside it
    const tempDir = path.join(config.audioCacheDir, `_tmp_${Date.now()}`);
    fs.mkdirSync(tempDir, { recursive: true });
    await tts.toFile(tempDir, text || filenameKey);
    tts.close();
    const generatedFile = path.join(tempDir, "audio.mp3");
    if (fs.existsSync(generatedFile)) {
      fs.renameSync(generatedFile, filePath);
      fs.rmSync(tempDir, { recursive: true, force: true });
      return filePath;
    }
    fs.rmSync(tempDir, { recursive: true, force: true });
    return null;
  } catch (error) {
    console.error(`TTS generation failed for "${filenameKey}" (voice: ${voiceName}):`, error);
    // Clean up partial file
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
    return null;
  }
}

export function getAudioPathSync(word: string): string | null {
  const filename = `${sanitizeFilename(word)}.mp3`;
  const filePath = path.join(config.audioCacheDir, filename);
  return fs.existsSync(filePath) ? filePath : null;
}
