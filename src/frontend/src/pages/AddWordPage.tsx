import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ArrowLeft } from "lucide-react";
import { contributeWord, getCategories, getHosts, ApiError } from "../services/api";
import { useAuth } from "../components/AuthProvider";

export default function AddWordPage() {
  const { t, i18n } = useTranslation();
  const { user } = useAuth();
  const refLang = user?.language || i18n.language;

  const [targetLangLabel, setTargetLangLabel] = useState("");
  const [categories, setCategories] = useState<{ id: string; name: string }[]>(
    []
  );

  const ALL_LANGS = ["en", "da", "it"] as const;
  const otherLangs = ALL_LANGS.filter((l) => l !== refLang);
  const langOrder = [refLang, ...otherLangs];

  const [word, setWord] = useState("");
  const [translations, setTranslations] = useState<Record<string, string>>({
    en: "",
    da: "",
    it: "",
  });
  const [phoneticHint, setPhoneticHint] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [difficulty, setDifficulty] = useState("beginner");
  const [example, setExample] = useState("");
  const [exampleTranslation, setExampleTranslation] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [duplicateId, setDuplicateId] = useState<string | null>(null);

  // Validation
  const wordError =
    word.length > 0 && word.trim().length === 0
      ? t("contribute.wordRequired")
      : word.length > 100
      ? t("contribute.wordTooLong")
      : "";
  const refTranslationError =
    translations[refLang].length > 0 && translations[refLang].trim().length === 0
      ? t("contribute.translationRequired")
      : "";
  const canSubmit =
    word.trim().length > 0 &&
    word.length <= 100 &&
    translations[refLang].trim().length > 0 &&
    !submitting;

  useEffect(() => {
    getCategories(refLang)
      .then(({ categories }) => setCategories(categories))
      .catch(() => {});
  }, [refLang]);

  useEffect(() => {
    if (!user?.hostId) return;
    getHosts().then(({ hosts }) => {
      const host = hosts.find((h) => h.id === user.hostId);
      if (host) {
        setTargetLangLabel(
          t(`languages.${host.language}`, { defaultValue: host.language })
        );
      }
    });
  }, [user?.hostId, t]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSubmit) return;

    setSubmitting(true);
    setError("");
    setDuplicateId(null);

    try {
      await contributeWord({
        word: word.trim(),
        translationEn: translations.en.trim() || undefined,
        translationDa: translations.da.trim() || undefined,
        translationIt: translations.it.trim() || undefined,
        phoneticHint: phoneticHint.trim() || undefined,
        categoryId: categoryId || undefined,
        difficulty,
        example: example.trim() || undefined,
        exampleTranslation: exampleTranslation.trim() || undefined,
      });
      setSuccess(true);
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        if (err.status === 409) {
          setError(t("contribute.duplicate"));
          setDuplicateId("exists");
        } else if (err.status === 400) {
          setError(err.message || t("errors.generic"));
        } else {
          setError(t("errors.generic"));
        }
      } else {
        setError(t("errors.generic"));
      }
    } finally {
      setSubmitting(false);
    }
  }

  function resetForm() {
    setWord("");
    setTranslations({ en: "", da: "", it: "" });
    setPhoneticHint("");
    setCategoryId("");
    setDifficulty("beginner");
    setExample("");
    setExampleTranslation("");
    setSuccess(false);
    setError("");
    setDuplicateId(null);
  }

  if (success) {
    return (
      <div className="max-w-lg mx-auto text-center py-12" role="status" aria-live="polite">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {t("contribute.success")}
        </h2>
        <div className="flex justify-center gap-4 mt-6">
          <button
            onClick={resetForm}
            className="px-6 py-2.5 bg-green-700 text-white rounded-lg font-medium hover:bg-green-800 transition-colors"
          >
            {t("contribute.addAnother")}
          </button>
          <Link
            to="/"
            className="px-6 py-2.5 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            {t("nav.categories")}
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Link
        to="/"
        className="inline-flex items-center gap-1.5 text-green-700 hover:underline mb-4 text-sm"
      >
        <ArrowLeft size={16} />
        {t("nav.categories")}
      </Link>

      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        {t("contribute.title")}
      </h1>

      <form
        onSubmit={handleSubmit}
        className="max-w-lg space-y-4"
        noValidate
      >
        {/* Word */}
        <div>
          <label htmlFor="word-input" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.word", { lang: targetLangLabel })} *
          </label>
          <input
            id="word-input"
            type="text"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            maxLength={100}
            required
            aria-describedby={wordError ? "word-error" : undefined}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
          {wordError && (
            <p id="word-error" className="text-red-600 text-sm mt-1" role="alert">{wordError}</p>
          )}
        </div>

        {/* Translations */}
        {langOrder.map((lang) => {
          const isRequired = lang === refLang;
          const langLabel = t(`languages.${lang}`, { defaultValue: lang });
          const inputId = `translation-${lang}`;
          const errorId = `translation-${lang}-error`;
          return (
            <div key={lang}>
              <label htmlFor={inputId} className="block text-sm font-medium text-gray-700 mb-1">
                {isRequired
                  ? t("contribute.translationRequired", { lang: langLabel })
                  : t("contribute.translationOptional", { lang: langLabel })}
                {isRequired && " *"}
              </label>
              <input
                id={inputId}
                type="text"
                value={translations[lang]}
                onChange={(e) =>
                  setTranslations((prev) => ({ ...prev, [lang]: e.target.value }))
                }
                required={isRequired}
                aria-describedby={isRequired && refTranslationError ? errorId : undefined}
                className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              {isRequired && refTranslationError && (
                <p id={errorId} className="text-red-600 text-sm mt-1" role="alert">{refTranslationError}</p>
              )}
            </div>
          );
        })}
        <p className="text-xs text-gray-500 -mt-2">
          {t("contribute.translationHelp")}
        </p>

        {/* Phonetic hint */}
        <div>
          <label htmlFor="phonetic-hint" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.phoneticHint")}
          </label>
          <input
            id="phonetic-hint"
            type="text"
            value={phoneticHint}
            onChange={(e) => setPhoneticHint(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        {/* Category */}
        <div>
          <label htmlFor="category-select" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.category")}
          </label>
          <select
            id="category-select"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
          >
            <option value="">{t("contribute.categoryDefault")}</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        {/* Difficulty */}
        <div>
          <label htmlFor="difficulty-select" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.difficulty")}
          </label>
          <select
            id="difficulty-select"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
          >
            <option value="beginner">{t("categories.beginner")}</option>
            <option value="intermediate">
              {t("categories.intermediate")}
            </option>
            <option value="advanced">{t("categories.advanced")}</option>
          </select>
        </div>

        {/* Example sentence */}
        <div>
          <label htmlFor="example-input" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.example")}
          </label>
          <input
            id="example-input"
            type="text"
            value={example}
            onChange={(e) => setExample(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        {/* Example translation */}
        <div>
          <label htmlFor="example-translation-input" className="block text-sm font-medium text-gray-700 mb-1">
            {t("contribute.exampleTranslation")}
          </label>
          <input
            id="example-translation-input"
            type="text"
            value={exampleTranslation}
            onChange={(e) => setExampleTranslation(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        {/* Error */}
        {error && (
          <div role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
            {error}
            {duplicateId && (
              <Link
                to={`/search?q=${encodeURIComponent(word)}`}
                className="ml-2 underline font-medium"
              >
                {t("contribute.viewExisting")}
              </Link>
            )}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={!canSubmit}
          className="w-full px-6 py-3 bg-green-700 text-white rounded-lg font-medium hover:bg-green-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          {submitting ? t("contribute.submitting") : t("contribute.submit")}
        </button>
      </form>
    </div>
  );
}
