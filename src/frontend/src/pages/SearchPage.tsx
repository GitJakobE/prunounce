import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Search } from "lucide-react";
import { searchWords } from "../services/api";
import { useAuth } from "../components/AuthProvider";
import WordCard from "../components/WordCard";
import type { WordEntry } from "../types";

export default function SearchPage() {
  const { t, i18n } = useTranslation();
  const { user, token } = useAuth();
  const lang = user?.language || i18n.language;

  const [query, setQuery] = useState("");
  const [results, setResults] = useState<WordEntry[]>([]);
  const [message, setMessage] = useState("");
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const q = query.trim();
    if (q.length < 2) {
      setMessage(t("search.minChars"));
      setResults([]);
      setSearched(true);
      return;
    }

    setLoading(true);
    setMessage("");
    try {
      const data = await searchWords(q, lang);
      setResults(data.results);
      if (data.results.length === 0) {
        setMessage(t("search.noResults", { term: q }));
      }
    } catch {
      setMessage(t("errors.generic"));
      setResults([]);
    } finally {
      setLoading(false);
      setSearched(true);
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        {t("nav.search")}
      </h1>

      <form onSubmit={handleSearch} className="flex gap-2 mb-6">
        <div className="relative flex-1">
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t("search.placeholder")}
            aria-label={t("search.placeholder")}
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2.5 bg-green-700 text-white rounded-lg font-medium hover:bg-green-800 disabled:opacity-60 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          {t("nav.search")}
        </button>
      </form>

      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
        </div>
      )}

      {!loading && message && (
        <p className="text-gray-500 text-center py-8">{message}</p>
      )}

      {!loading && results.length > 0 && (
        <div className="space-y-3">
          {results.map((word) => (
            <WordCard key={word.id} word={word} token={token} hostId={user?.hostId} />
          ))}
        </div>
      )}

      {!loading && !searched && (
        <p className="text-gray-400 text-center py-12">
          {t("search.minChars")}
        </p>
      )}
    </div>
  );
}
