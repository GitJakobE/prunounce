import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { BookOpen, Clock } from "lucide-react";
import { getStories } from "../services/api";
import HostBanner from "../components/HostBanner";
import type { StoryListItem } from "../types";

const DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"] as const;
const LENGTH_ORDER = ["short", "medium", "long"] as const;

const DIFFICULTY_COLORS: Record<string, string> = {
  beginner: "bg-green-100 text-green-800",
  intermediate: "bg-yellow-100 text-yellow-800",
  advanced: "bg-red-100 text-red-800",
};

const LENGTH_COLORS: Record<string, string> = {
  short: "bg-blue-50 text-blue-700",
  medium: "bg-teal-50 text-teal-700",
  long: "bg-orange-50 text-orange-700",
};

export default function StoriesPage() {
  const { t } = useTranslation();
  const [stories, setStories] = useState<Record<string, StoryListItem[]>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getStories()
      .then(({ stories }) => setStories(stories))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
      </div>
    );
  }

  const hasAny = DIFFICULTY_ORDER.some((d) => (stories[d]?.length ?? 0) > 0);

  return (
    <div>
      <HostBanner />

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <BookOpen size={24} className="text-green-700" />
          {t("stories.title")}
        </h1>
      </div>

      {!hasAny && (
        <p className="text-gray-500 text-center py-12">{t("stories.noStories")}</p>
      )}

      <div className="space-y-10">
        {DIFFICULTY_ORDER.map((difficulty) => {
          const items = stories[difficulty] ?? [];
          if (items.length === 0) return null;

          // Group items by length
          const byLength: Record<string, StoryListItem[]> = {};
          for (const item of items) {
            const len = item.length || "short";
            (byLength[len] ??= []).push(item);
          }

          return (
            <section key={difficulty}>
              <h2 className="text-lg font-semibold text-gray-700 mb-4 uppercase tracking-wide">
                {t(`stories.${difficulty}`)}
              </h2>

              {LENGTH_ORDER.map((len) => {
                const lengthItems = byLength[len];
                if (!lengthItems || lengthItems.length === 0) return null;

                return (
                  <div key={len} className="mb-6">
                    <h3 className="text-sm font-medium text-gray-500 mb-3 flex items-center gap-2">
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${LENGTH_COLORS[len] ?? "bg-gray-100 text-gray-600"}`}>
                        {t(`stories.${len}`)}
                      </span>
                    </h3>

                    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                      {lengthItems.map((story) => (
                        <Link
                          key={story.id}
                          to={`/stories/${story.id}`}
                          className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-green-400 flex flex-col"
                        >
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <h3 className="text-base font-semibold text-gray-900 leading-snug">
                              {story.title}
                            </h3>
                            <span
                              className={`shrink-0 text-xs px-2 py-0.5 rounded-full font-medium ${DIFFICULTY_COLORS[story.difficulty] ?? "bg-gray-100 text-gray-700"}`}
                            >
                              {t(`stories.${story.difficulty}`)}
                            </span>
                          </div>

                          <p className="text-sm text-gray-600 line-clamp-3 flex-1">
                            {story.description}
                          </p>

                          <div className="mt-3 flex items-center gap-1 text-xs text-gray-400">
                            <Clock size={12} />
                            {t("stories.readingTime", { count: story.estimatedReadingTime })}
                          </div>
                        </Link>
                      ))}
                    </div>
                  </div>
                );
              })}
            </section>
          );
        })}
      </div>
    </div>
  );
}
