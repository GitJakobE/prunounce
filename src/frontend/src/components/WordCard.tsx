import { Check } from "lucide-react";
import { useTranslation } from "react-i18next";
import AudioButton from "./AudioButton";
import type { WordEntry } from "../types";

interface WordCardProps {
  word: WordEntry;
  token: string | null;
  hostId?: string | null;
  onListened?: () => void;
}

export default function WordCard({ word, token, hostId, onListened }: WordCardProps) {
  const { t, i18n } = useTranslation();
  const hasExample = !!(word.exampleTarget && word.exampleTarget.length > 0);
  const refLangLabel = t(`languages.${i18n.language}`, { defaultValue: i18n.language });

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center gap-4">
        <AudioButton
          wordId={word.id}
          wordText={word.word}
          token={token}
          hostId={hostId}
          hasExample={hasExample}
          onListened={onListened}
        />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold text-gray-900">
              {word.word}
            </span>
            {word.listened && (
              <Check
                size={16}
                className="text-green-600 flex-shrink-0"
                aria-label={t("words.listened")}
              />
            )}
          </div>
          <p className="text-sm text-gray-500 italic">{word.phoneticHint}</p>
          {word.translation ? (
            <p className="text-sm text-gray-700">{word.translation}</p>
          ) : (
            <p className="text-sm text-gray-400 italic">
              {t("words.noTranslation", { lang: refLangLabel })}
            </p>
          )}
        </div>
        <span
          className={`text-xs px-2 py-1 rounded-full flex-shrink-0 ${
            word.difficulty === "beginner"
              ? "bg-green-100 text-green-800"
              : word.difficulty === "intermediate"
              ? "bg-yellow-100 text-yellow-800"
              : "bg-red-100 text-red-800"
          }`}
        >
          {t(`categories.${word.difficulty}`)}
        </span>
      </div>
      {hasExample && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <p className="text-sm text-gray-800 italic">
            &ldquo;{word.exampleTarget}&rdquo;
          </p>
          <p className="text-xs text-gray-500 mt-1">{word.example}</p>
        </div>
      )}
    </div>
  );
}
