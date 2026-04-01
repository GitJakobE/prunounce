import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Plus } from "lucide-react";
import { getCategories } from "../services/api";
import { useAuth } from "../components/AuthProvider";
import HostBanner from "../components/HostBanner";
import type { CategorySummary } from "../types";

export default function CategoriesPage() {
  const { t, i18n } = useTranslation();
  const { user } = useAuth();
  const [categories, setCategories] = useState<CategorySummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const lang = user?.language || i18n.language;
    setLoading(true);
    getCategories(lang)
      .then(({ categories }) => setCategories(categories))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user?.language, user?.hostId, i18n.language]);

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
      </div>
    );
  }

  return (
    <div>
      <HostBanner />

      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {t("categories.title")}
        </h1>
        <Link
          to="/add-word"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-green-700 text-white rounded-lg text-sm font-medium hover:bg-green-800 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          <Plus size={16} />
          {t("contribute.title")}
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {categories.map((cat) => (
          <Link
            key={cat.id}
            to={`/categories/${cat.id}`}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-green-400"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              {cat.name}
            </h2>

            {/* Progress bar */}
            <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all"
                style={{
                  width: `${
                    cat.totalWords > 0
                      ? (cat.listenedWords / cat.totalWords) * 100
                      : 0
                  }%`,
                }}
              />
            </div>
            <p className="text-sm text-gray-600">
              {t("categories.progress", {
                listened: cat.listenedWords,
                total: cat.totalWords,
              })}
            </p>

            {/* Difficulty breakdown */}
            <div className="flex gap-2 mt-3">
              {cat.progressByDifficulty.map((d) =>
                d.total > 0 ? (
                  <span
                    key={d.difficulty}
                    className={`text-xs px-2 py-0.5 rounded-full ${
                      d.difficulty === "beginner"
                        ? "bg-green-100 text-green-800"
                        : d.difficulty === "intermediate"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {d.listened}/{d.total}
                  </span>
                ) : null
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
