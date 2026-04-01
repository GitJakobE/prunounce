import { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ArrowLeft } from "lucide-react";
import { getCategoryWords } from "../services/api";
import { useAuth } from "../components/AuthProvider";
import WordCard from "../components/WordCard";
import type { WordEntry } from "../types";

const DIFFICULTIES = ["all", "beginner", "intermediate", "advanced"] as const;

export default function CategoryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { t, i18n } = useTranslation();
  const { user, token } = useAuth();
  const lang = user?.language || i18n.language;

  const [words, setWords] = useState<WordEntry[]>([]);
  const [categoryName, setCategoryName] = useState("");
  const [difficulty, setDifficulty] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  const loadWords = useCallback(
    (diff: string) => {
      if (!id) return;
      setLoading(true);
      getCategoryWords(id, lang, diff === "all" ? undefined : diff)
        .then(({ category, words }) => {
          setCategoryName(category.name);
          setWords(words);
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    },
    [id, lang, user?.hostId]
  );

  useEffect(() => {
    loadWords(difficulty);
  }, [loadWords, difficulty]);

  function handleListened() {
    // Reload to update listened status
    loadWords(difficulty);
  }

  const diffLabel = (d: string) => {
    if (d === "all") return t("categories.all");
    return t(`categories.${d}`);
  };

  return (
    <div>
      <Link
        to="/"
        className="inline-flex items-center gap-1.5 text-green-700 hover:underline mb-4 text-sm"
      >
        <ArrowLeft size={16} />
        {t("categories.title")}
      </Link>

      <h1 className="text-2xl font-bold text-gray-900 mb-4">{categoryName}</h1>

      {/* Difficulty filter tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {DIFFICULTIES.map((d) => (
          <button
            key={d}
            onClick={() => setDifficulty(d)}
            className={`px-4 py-2.5 rounded-full text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 ${
              difficulty === d
                ? "bg-green-700 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
            aria-pressed={difficulty === d}
          >
            {diffLabel(d)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
        </div>
      ) : words.length === 0 ? (
        <p className="text-gray-500 text-center py-12">
          {t("words.noWords")}
        </p>
      ) : (
        <div className="space-y-3">
          {words.map((word) => (
            <WordCard
              key={word.id}
              word={word}
              token={token}
              hostId={user?.hostId}
              onListened={handleListened}
            />
          ))}
        </div>
      )}
    </div>
  );
}
