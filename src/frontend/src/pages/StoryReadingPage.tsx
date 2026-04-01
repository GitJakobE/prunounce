import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  ArrowLeft,
  Play,
  Pause,
  Square,
  Volume2,
  Loader2,
  X,
} from "lucide-react";
import { getStory, lookupWord, storyAudioUrl, audioUrl } from "../services/api";
import { useAuth } from "../components/AuthProvider";
import type { StoryDetail, WordLookupResult, StorySegment } from "../types";

// ── Speed settings ────────────────────────────────────────────────────────────

const SPEEDS = ["very_slow", "slow", "normal", "fast", "very_fast"] as const;
type Speed = (typeof SPEEDS)[number];

// ── Token helpers ─────────────────────────────────────────────────────────────

/** Split story body into sentence segments, each containing word tokens. */
function tokenise(text: string): string[][] {
  // Split on sentence-ending punctuation keeping the punctuation attached
  const sentences = text.match(/[^.!?]+[.!?]?\s*/g) ?? [text];
  return sentences.map((sentence) => {
    // Split each sentence into word/non-word tokens
    return sentence.match(/[\w\u00C0-\u024F]+|[^\w\u00C0-\u024F]+/g) ?? [sentence];
  });
}

function isWord(token: string): boolean {
  return /[\w\u00C0-\u024F]/.test(token);
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function StoryReadingPage() {
  const { id } = useParams<{ id: string }>();
  const { t, i18n } = useTranslation();
  const { user } = useAuth();

  const [story, setStory] = useState<StoryDetail | null>(null);
  const [loading, setLoading] = useState(true);

  // Translation panel
  const [selected, setSelected] = useState<WordLookupResult | null>(null);
  const [lookingUp, setLookingUp] = useState(false);
  const [wordAudioPlaying, setWordAudioPlaying] = useState(false);
  const wordAudioRef = useRef<HTMLAudioElement | null>(null);

  // Narration
  const [speed, setSpeed] = useState<Speed>("normal");
  const [narrationState, setNarrationState] = useState<"idle" | "loading" | "playing" | "paused">("idle");
  const narrationRef = useRef<HTMLAudioElement | null>(null);

  // ── Load story ──────────────────────────────────────────────────────────────

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getStory(id)
      .then(({ story }) => setStory(story))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  // ── Cleanup audio on unmount ────────────────────────────────────────────────

  useEffect(() => {
    return () => {
      narrationRef.current?.pause();
      wordAudioRef.current?.pause();
    };
  }, []);

  // ── Word click → lookup ─────────────────────────────────────────────────────

  const lang = user?.language || i18n.language;

  const handleWordClick = useCallback(
    (word: string) => {
      wordAudioRef.current?.pause();
      setWordAudioPlaying(false);
      setSelected(null);
      setLookingUp(true);
      lookupWord(word, lang)
        .then((result) => setSelected(result))
        .catch(() =>
          setSelected({ word, translation: null, phoneticHint: null, wordId: null })
        )
        .finally(() => setLookingUp(false));
    },
    [lang]
  );

  // ── Translation panel word audio ────────────────────────────────────────────

  const playWordAudio = useCallback(() => {
    if (!selected?.wordId) return;
    wordAudioRef.current?.pause();
    const audio = new Audio(audioUrl(selected.wordId));
    wordAudioRef.current = audio;
    setWordAudioPlaying(true);
    audio.onended = () => setWordAudioPlaying(false);
    audio.onerror = () => setWordAudioPlaying(false);
    audio.play().catch(() => setWordAudioPlaying(false));
  }, [selected]);

  // ── Narration controls ──────────────────────────────────────────────────────

  const startNarration = useCallback(() => {
    if (!id) return;
    narrationRef.current?.pause();
    setNarrationState("loading");
    const audio = new Audio(storyAudioUrl(id, speed));
    narrationRef.current = audio;
    audio.oncanplaythrough = () => {
      setNarrationState("playing");
      audio.play().catch(() => setNarrationState("idle"));
    };
    audio.onended = () => setNarrationState("idle");
    audio.onerror = () => setNarrationState("idle");
  }, [id, speed]);

  const togglePause = useCallback(() => {
    const audio = narrationRef.current;
    if (!audio) return;
    if (narrationState === "playing") {
      audio.pause();
      setNarrationState("paused");
    } else if (narrationState === "paused") {
      audio.play().catch(() => {});
      setNarrationState("playing");
    }
  }, [narrationState]);

  const stopNarration = useCallback(() => {
    narrationRef.current?.pause();
    narrationRef.current = null;
    setNarrationState("idle");
  }, []);

  // When speed changes while playing, restart narration
  const handleSpeedChange = useCallback(
    (newSpeed: Speed) => {
      setSpeed(newSpeed);
      if (narrationState === "playing" || narrationState === "paused") {
        stopNarration();
      }
    },
    [narrationState, stopNarration]
  );

  // ── Tokenised body ──────────────────────────────────────────────────────────

  const isDialogue = story?.format === "dialogue" || story?.format === "mixed";
  const segments: StorySegment[] = isDialogue && story?.segments?.length
    ? story.segments
    : [];
  const sentences = story && !isDialogue ? tokenise(story.body) : [];

  // ── Render ──────────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
      </div>
    );
  }

  if (!story) {
    return (
      <div className="text-center py-12 text-gray-500">{t("errors.notFound")}</div>
    );
  }

  const difficultyColor =
    story.difficulty === "beginner"
      ? "bg-green-100 text-green-800"
      : story.difficulty === "intermediate"
      ? "bg-yellow-100 text-yellow-800"
      : "bg-red-100 text-red-800";

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      {/* ── Main reading area ────────────────────────────────────────────────── */}
      <div className="flex-1 min-w-0">
        {/* Back link */}
        <Link
          to="/stories"
          className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4"
        >
          <ArrowLeft size={14} />
          {t("stories.backToStories")}
        </Link>

        {/* Story header */}
        <div className="mb-4">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-bold text-gray-900">{story.title}</h1>
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium shrink-0 ${difficultyColor}`}>
              {t(`stories.${story.difficulty}`)}
            </span>
          </div>
          <p className="text-sm text-gray-500">{story.description}</p>
        </div>

        {/* Narration controls */}
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 mb-6">
          {/* Speed selector */}
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="text-xs text-gray-500 font-medium">Speed:</span>
            {SPEEDS.map((s) => (
              <button
                key={s}
                onClick={() => handleSpeedChange(s)}
                className={`text-xs px-3 py-1 rounded-full border transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 ${
                  speed === s
                    ? "bg-green-700 text-white border-green-700"
                    : "bg-white text-gray-600 border-gray-300 hover:border-green-400"
                }`}
              >
                {t(`stories.speed.${s}`)}
              </button>
            ))}
          </div>

          {/* Play / Pause / Stop */}
          <div className="flex items-center gap-3">
            {narrationState === "idle" && (
              <button
                onClick={startNarration}
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-700 text-white rounded-lg text-sm font-medium hover:bg-green-800 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
              >
                <Play size={16} />
                {t("stories.playNarration")}
              </button>
            )}

            {narrationState === "loading" && (
              <button
                disabled
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-700/60 text-white rounded-lg text-sm font-medium cursor-wait"
              >
                <Loader2 size={16} className="animate-spin" />
                {t("stories.loadingAudio")}
              </button>
            )}

            {(narrationState === "playing" || narrationState === "paused") && (
              <>
                <button
                  onClick={togglePause}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-green-700 text-white rounded-lg text-sm font-medium hover:bg-green-800 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                  {narrationState === "playing" ? (
                    <>
                      <Pause size={16} />
                      {t("stories.pauseNarration")}
                    </>
                  ) : (
                    <>
                      <Play size={16} />
                      {t("stories.playNarration")}
                    </>
                  )}
                </button>
                <button
                  onClick={stopNarration}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                  <Square size={16} />
                  {t("stories.stopNarration")}
                </button>
              </>
            )}

            {narrationState === "playing" && (
              <span className="text-sm text-green-700 flex items-center gap-1">
                <Volume2 size={14} />
                {t("stories.narrating")}
              </span>
            )}
          </div>
        </div>

        {/* Story body — clickable words */}
        <div className="prose prose-lg max-w-none text-gray-800 leading-relaxed text-xl select-none">
          {isDialogue ? (
            /* Dialogue rendering */
            <div className="space-y-2">
              {segments.map((seg, sIdx) => {
                const tokens = tokenise(seg.text).flat();
                if (seg.type === "dialogue") {
                  const speakerIdx = (story?.speakers ?? []).indexOf(seg.speaker);
                  const colors = [
                    "text-blue-700",
                    "text-purple-700",
                    "text-orange-700",
                    "text-teal-700",
                  ];
                  const color = colors[speakerIdx >= 0 ? speakerIdx % colors.length : 0];
                  return (
                    <div key={sIdx} className="flex gap-2">
                      <span className={`font-bold shrink-0 ${color}`} aria-label={t("stories.speaker", { name: seg.speaker })}>
                        {seg.speaker}:
                      </span>
                      <span>
                        {tokens.map((token, tIdx) =>
                          isWord(token) ? (
                            <button
                              key={tIdx}
                              onClick={() => handleWordClick(token)}
                              className={`cursor-pointer rounded px-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 hover:bg-green-100 hover:text-green-900 ${
                                selected?.word.toLowerCase() === token.toLowerCase()
                                  ? "bg-green-200 text-green-900"
                                  : ""
                              }`}
                            >
                              {token}
                            </button>
                          ) : (
                            <span key={tIdx}>{token}</span>
                          )
                        )}
                      </span>
                    </div>
                  );
                }
                /* Narration segment in mixed stories */
                return (
                  <p key={sIdx} className="italic text-gray-600">
                    {tokens.map((token, tIdx) =>
                      isWord(token) ? (
                        <button
                          key={tIdx}
                          onClick={() => handleWordClick(token)}
                          className={`cursor-pointer rounded px-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 hover:bg-green-100 hover:text-green-900 ${
                            selected?.word.toLowerCase() === token.toLowerCase()
                              ? "bg-green-200 text-green-900"
                              : ""
                          }`}
                        >
                          {token}
                        </button>
                      ) : (
                        <span key={tIdx}>{token}</span>
                      )
                    )}
                  </p>
                );
              })}
            </div>
          ) : (
            /* Narrative rendering (original) */
            sentences.map((sentence, sIdx) => (
              <span key={sIdx}>
                {sentence.map((token, tIdx) =>
                  isWord(token) ? (
                    <button
                      key={tIdx}
                      onClick={() => handleWordClick(token)}
                      className={`cursor-pointer rounded px-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 hover:bg-green-100 hover:text-green-900 ${
                        selected?.word.toLowerCase() === token.toLowerCase()
                          ? "bg-green-200 text-green-900"
                          : ""
                      }`}
                    >
                      {token}
                    </button>
                  ) : (
                    <span key={tIdx}>{token}</span>
                  )
                )}
              </span>
            ))
          )}
        </div>
      </div>

      {/* ── Translation panel ────────────────────────────────────────────────── */}
      {/* Desktop: fixed right sidebar */}
      <aside className="hidden lg:block w-72 shrink-0">
        <div className="sticky top-6 bg-white border border-gray-200 rounded-xl shadow-sm p-5">
          <TranslationPanel
            lookingUp={lookingUp}
            selected={selected}
            wordAudioPlaying={wordAudioPlaying}
            onPlayWord={playWordAudio}
            onClose={() => setSelected(null)}
            t={t}
          />
        </div>
      </aside>

      {/* Mobile: slide-up panel when a word is selected */}
      {(selected || lookingUp) && (
        <div className="lg:hidden fixed inset-x-0 bottom-0 z-40 bg-white border-t border-gray-200 rounded-t-2xl shadow-xl p-5 pb-safe">
          <TranslationPanel
            lookingUp={lookingUp}
            selected={selected}
            wordAudioPlaying={wordAudioPlaying}
            onPlayWord={playWordAudio}
            onClose={() => setSelected(null)}
            t={t}
          />
        </div>
      )}
    </div>
  );
}

// ── Translation Panel Sub-component ─────────────────────────────────────────

interface TranslationPanelProps {
  lookingUp: boolean;
  selected: WordLookupResult | null;
  wordAudioPlaying: boolean;
  onPlayWord: () => void;
  onClose: () => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  t: (key: string) => string;
}

function TranslationPanel({
  lookingUp,
  selected,
  wordAudioPlaying,
  onPlayWord,
  onClose,
  t,
}: TranslationPanelProps) {
  if (lookingUp) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-gray-400 gap-2">
        <Loader2 size={20} className="animate-spin" />
        <span className="text-sm">Looking up…</span>
      </div>
    );
  }

  if (!selected) {
    return (
      <p className="text-sm text-gray-400 text-center py-8">
        {t("stories.clickToTranslate")}
      </p>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <span className="text-2xl font-bold text-gray-900">{selected.word}</span>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-green-400 rounded"
          aria-label="Close"
        >
          <X size={18} />
        </button>
      </div>

      {/* Phonetic hint */}
      {selected.phoneticHint && (
        <p className="text-sm text-gray-500 mb-3 italic">{selected.phoneticHint}</p>
      )}

      {/* Translation */}
      <div className="mb-4">
        <span className="text-xs text-gray-400 uppercase tracking-wide font-medium">
          {t("stories.translation")}
        </span>
        <p className="text-base text-gray-800 mt-1">
          {selected.translation ?? (
            <span className="text-gray-400 italic">
              {t("stories.translationUnavailable")}
            </span>
          )}
        </p>
      </div>

      {/* Play button */}
      {selected.wordId && (
        <button
          onClick={onPlayWord}
          disabled={wordAudioPlaying}
          className="inline-flex items-center gap-2 px-4 py-2 w-full justify-center bg-green-700 text-white rounded-lg text-sm font-medium hover:bg-green-800 transition-colors disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          {wordAudioPlaying ? (
            <Loader2 size={14} className="animate-spin" />
          ) : (
            <Volume2 size={14} />
          )}
          {t("stories.playWord")}
        </button>
      )}
    </div>
  );
}
