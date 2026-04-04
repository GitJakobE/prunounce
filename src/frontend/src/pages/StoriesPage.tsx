import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { BookOpen, Clock, Plus, Trash2, X } from "lucide-react";
import { getStories, createStory, deleteStory } from "../services/api";
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

  // Add-story form state
  const [showForm, setShowForm] = useState(false);
  const [formTitle, setFormTitle] = useState("");
  const [formBody, setFormBody] = useState("");
  const [formDifficulty, setFormDifficulty] = useState("beginner");
  const [formDescription, setFormDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const loadStories = () => {
    setLoading(true);
    getStories()
      .then(({ stories }) => setStories(stories))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadStories();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    if (!formTitle.trim() || !formBody.trim()) {
      setFormError(t("stories.addStoryRequired"));
      return;
    }
    setSubmitting(true);
    try {
      await createStory({
        title: formTitle.trim(),
        body: formBody.trim(),
        difficulty: formDifficulty,
        description: formDescription.trim(),
      });
      setFormTitle("");
      setFormBody("");
      setFormDifficulty("beginner");
      setFormDescription("");
      setShowForm(false);
      loadStories();
    } catch {
      setFormError(t("stories.addStoryError"));
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (storyId: string) => {
    try {
      await deleteStory(storyId);
      loadStories();
    } catch {
      // ignore
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
      </div>
    );
  }

  const hasAny = DIFFICULTY_ORDER.some((d) => (stories[d]?.length ?? 0) > 0);

  // Collect user stories across all difficulties
  const userStories = DIFFICULTY_ORDER.flatMap((d) =>
    (stories[d] ?? []).filter((s) => s.isUserStory),
  );
  // Filter user stories out from the main groups so they show in their own section
  const globalStories: Record<string, StoryListItem[]> = {};
  for (const d of DIFFICULTY_ORDER) {
    globalStories[d] = (stories[d] ?? []).filter((s) => !s.isUserStory);
  }

  return (
    <div>
      <HostBanner />

      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <BookOpen size={24} className="text-green-700" />
          {t("stories.title")}
        </h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg bg-green-700 text-white hover:bg-green-800 transition-colors"
        >
          {showForm ? <X size={16} /> : <Plus size={16} />}
          {showForm ? t("stories.cancel") : t("stories.addStory")}
        </button>
      </div>

      {/* ── Add Story Form ────────────────────────────────────────────── */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8 space-y-4"
        >
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("stories.formTitle")}
            </label>
            <input
              type="text"
              value={formTitle}
              onChange={(e) => setFormTitle(e.target.value)}
              maxLength={200}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-green-400 focus:border-green-400"
              placeholder={t("stories.formTitlePlaceholder")}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("stories.formDescription")}
            </label>
            <input
              type="text"
              value={formDescription}
              onChange={(e) => setFormDescription(e.target.value)}
              maxLength={500}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-green-400 focus:border-green-400"
              placeholder={t("stories.formDescriptionPlaceholder")}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("stories.formDifficulty")}
            </label>
            <select
              value={formDifficulty}
              onChange={(e) => setFormDifficulty(e.target.value)}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-green-400 focus:border-green-400"
            >
              {DIFFICULTY_ORDER.map((d) => (
                <option key={d} value={d}>
                  {t(`stories.${d}`)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("stories.formBody")}
            </label>
            <textarea
              value={formBody}
              onChange={(e) => setFormBody(e.target.value)}
              rows={8}
              maxLength={10000}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-green-400 focus:border-green-400"
              placeholder={t("stories.formBodyPlaceholder")}
            />
          </div>

          {formError && (
            <p className="text-sm text-red-600">{formError}</p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="px-5 py-2 text-sm font-medium rounded-lg bg-green-700 text-white hover:bg-green-800 disabled:opacity-50 transition-colors"
          >
            {submitting ? t("stories.submitting") : t("stories.submitStory")}
          </button>
        </form>
      )}

      {!hasAny && (
        <p className="text-gray-500 text-center py-12">{t("stories.noStories")}</p>
      )}

      {/* ── My Stories ────────────────────────────────────────────────── */}
      {userStories.length > 0 && (
        <section className="mb-10">
          <h2 className="text-lg font-semibold text-gray-700 mb-4 uppercase tracking-wide">
            {t("stories.myStories")}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {userStories.map((story) => (
              <div
                key={story.id}
                className="bg-white rounded-lg shadow-sm border border-purple-200 p-5 flex flex-col relative"
              >
                <button
                  onClick={() => handleDelete(story.id)}
                  className="absolute top-2 right-2 p-1 text-gray-400 hover:text-red-600 transition-colors"
                  title={t("stories.deleteStory")}
                >
                  <Trash2 size={16} />
                </button>
                <Link to={`/stories/${story.id}`} className="flex-1 flex flex-col">
                  <div className="flex items-start justify-between gap-2 mb-2 pr-6">
                    <h3 className="text-base font-semibold text-gray-900 leading-snug">
                      {story.title}
                    </h3>
                    <span
                      className={`shrink-0 text-xs px-2 py-0.5 rounded-full font-medium ${DIFFICULTY_COLORS[story.difficulty] ?? "bg-gray-100 text-gray-700"}`}
                    >
                      {t(`stories.${story.difficulty}`)}
                    </span>
                  </div>
                  {story.description && (
                    <p className="text-sm text-gray-600 line-clamp-3 flex-1">
                      {story.description}
                    </p>
                  )}
                  <div className="mt-3 flex items-center gap-1 text-xs text-gray-400">
                    <Clock size={12} />
                    {t("stories.readingTime", { count: story.estimatedReadingTime })}
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ── Global Stories ────────────────────────────────────────────── */}
      <div className="space-y-10">
        {DIFFICULTY_ORDER.map((difficulty) => {
          const items = globalStories[difficulty] ?? [];
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
