import { useRef, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Volume2 } from "lucide-react";
import { markListened } from "../services/api";

// Single audio instance shared across all AudioButton instances
let currentAudio: HTMLAudioElement | null = null;
let currentWordId: string | null = null;
const EXAMPLE_GAP_MS = 250;
const MAX_WORD_TO_EXAMPLE_BREAK_MS = 1000;

// Notify all buttons to re-sync their state
const listeners = new Set<() => void>();
function notifyAll() {
  listeners.forEach((fn) => fn());
}

type PlayState = "idle" | "loading" | "playing";

interface AudioButtonProps {
  wordId: string;
  wordText: string;
  token: string | null;
  hostId?: string | null;
  hasExample?: boolean;
  onListened?: () => void;
}

export default function AudioButton({
  wordId,
  wordText,
  token,
  hostId,
  hasExample,
  onListened,
}: AudioButtonProps) {
  const { t } = useTranslation();
  const [playState, setPlayState] = useState<PlayState>("idle");
  const stateRef = useRef<PlayState>("idle");

  const updateState = useCallback((s: PlayState) => {
    stateRef.current = s;
    setPlayState(s);
  }, []);

  const stopPlayback = useCallback(() => {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    currentWordId = null;
    updateState("idle");
    notifyAll();
  }, [updateState]);

  // Reset to idle whenever another button takes over
  useCallback(() => {
    const sync = () => {
      if (currentWordId !== wordId && stateRef.current !== "idle") {
        updateState("idle");
      }
    };
    listeners.add(sync);
    return () => listeners.delete(sync);
  }, [wordId, updateState])();

  const play = useCallback(async () => {
    const wasPlaying = currentWordId === wordId && stateRef.current !== "idle";

    // Stop whatever is currently playing (possibly ourselves)
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    currentWordId = null;
    notifyAll();
    updateState("idle");

    if (wasPlaying) return; // toggle off

    currentWordId = wordId;
    updateState("loading");
    notifyAll();

    const hostParam = hostId ? `&host=${hostId}` : "";
    const exampleUrl = `/api/audio/${encodeURIComponent(wordId)}/example?token=${token}${hostParam}`;

    const preloadExampleAudio = (): Promise<HTMLAudioElement | null> =>
      new Promise((resolve) => {
        if (!hasExample) {
          resolve(null);
          return;
        }

        const exAudio = new Audio(exampleUrl);
        exAudio.preload = "auto";

        const cleanup = () => {
          exAudio.oncanplay = null;
          exAudio.onerror = null;
        };

        exAudio.oncanplay = () => {
          cleanup();
          resolve(exAudio);
        };
        exAudio.onerror = () => {
          cleanup();
          resolve(null);
        };

        exAudio.load();
      });

    const exampleAudioPromise = preloadExampleAudio();

    const playAudio = (audio: HTMLAudioElement): Promise<boolean> =>
      new Promise((resolve) => {
        audio.oncanplay = () => {
          if (currentWordId === wordId) updateState("playing");
        };
        audio.onended = () => resolve(true);
        audio.onerror = () => resolve(false);
        audio.play().catch(() => resolve(false));
      });

    const wordAudio = new Audio(
      `/api/audio/${encodeURIComponent(wordId)}?token=${token}${hostParam}`
    );
    currentAudio = wordAudio;
    const wordPlayed = await playAudio(wordAudio);

    if (wordPlayed && hasExample && currentWordId === wordId) {
      await new Promise((r) => setTimeout(r, EXAMPLE_GAP_MS));
      if (currentWordId === wordId) {
        const remainingWaitMs = Math.max(
          0,
          MAX_WORD_TO_EXAMPLE_BREAK_MS - EXAMPLE_GAP_MS
        );
        const exAudio = await Promise.race<HTMLAudioElement | null>([
          exampleAudioPromise,
          new Promise((resolve) => {
            setTimeout(() => resolve(null), remainingWaitMs);
          }),
        ]);
        if (exAudio) {
          currentAudio = exAudio;
          await playAudio(exAudio);
        }
      }
    }

    if (currentWordId === wordId) {
      markListened(wordId).catch(() => {});
      onListened?.();
      stopPlayback();
    }
  }, [wordId, token, hostId, hasExample, onListened, stopPlayback, updateState]);

  const isActive = playState !== "idle";
  const isLoading = playState === "loading";

  return (
    <button
      onClick={play}
      className="relative p-3 rounded-full bg-green-600 text-white hover:bg-green-700 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
      aria-label={t("words.playAudio", { word: wordText })}
      title={t("words.playAudio", { word: wordText })}
    >
      <Volume2 size={20} />

      {/* Spinner / progress ring — visible while loading or playing */}
      {isActive && (
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          viewBox="0 0 46 46"
        >
          <circle
            cx="23"
            cy="23"
            r="21"
            fill="none"
            stroke="white"
            strokeWidth="2.5"
            strokeOpacity="0.3"
          />
          <circle
            cx="23"
            cy="23"
            r="21"
            fill="none"
            stroke="white"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeDasharray={isLoading ? "33 99" : "132 0"}
            strokeDashoffset="33"
            className={isLoading ? "animate-spin origin-center" : "transition-all duration-300"}
            style={{ transformOrigin: "23px 23px" }}
          />
        </svg>
      )}
    </button>
  );
}
