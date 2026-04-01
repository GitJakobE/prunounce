import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Trash2 } from "lucide-react";
import {
  getProfile,
  updateProfile,
  deleteAccount,
} from "../services/api";
import { useAuth } from "../components/AuthProvider";

export default function ProfilePage() {
  const { t, i18n } = useTranslation();
  const { user, setAuth, logout } = useAuth();
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [displayName, setDisplayName] = useState(user?.displayName || "");
  const [language, setLanguage] = useState(user?.language || "en");
  const [totalWords, setTotalWords] = useState(0);
  const [listenedWords, setListenedWords] = useState(0);
  const [saved, setSaved] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    getProfile()
      .then(({ user: u, progress }) => {
        setDisplayName(u.displayName || "");
        setLanguage(u.language);
        setTotalWords(progress.totalWords);
        setListenedWords(progress.listenedWords);
      })
      .catch(() => {});
  }, [user?.hostId]);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setSaved(false);

    try {
      const { user: updated } = await updateProfile({
        displayName,
        language,
      });
      if (token) {
        setAuth(token, updated);
      }
      i18n.changeLanguage(language);
      localStorage.setItem("language", language);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      // Ignore
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    try {
      await deleteAccount();
      logout();
      navigate("/login");
    } catch {
      // Ignore
    }
  }

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        {t("profile.title")}
      </h1>

      {/* Progress */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">
          {t("profile.progress")}
        </h2>
        <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
          <div
            className="bg-green-600 h-3 rounded-full transition-all"
            style={{
              width: `${
                totalWords > 0 ? (listenedWords / totalWords) * 100 : 0
              }%`,
            }}
          />
        </div>
        <p className="text-sm text-gray-600">
          {t("profile.progressSummary", {
            listened: listenedWords,
            total: totalWords,
          })}
        </p>
      </div>

      {/* Settings form */}
      <form
        onSubmit={handleSave}
        className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 mb-6"
      >
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t("auth.email")}
          </label>
          <input
            type="email"
            value={user?.email || ""}
            disabled
            className="w-full px-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-gray-500"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="displayName"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            {t("auth.displayName")}
          </label>
          <input
            id="displayName"
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="language"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            {t("profile.language")}
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="en">{t("languages.en")}</option>
            <option value="da">{t("languages.da")}</option>
            <option value="it">{t("languages.it")}</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full py-2.5 bg-green-700 text-white rounded-lg font-medium hover:bg-green-800 disabled:opacity-60 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          {saving ? "…" : t("profile.save")}
        </button>

        {saved && (
          <p className="text-green-600 text-sm text-center mt-2">
            {t("profile.saved")}
          </p>
        )}
      </form>

      {/* Danger zone */}
      <div className="bg-white rounded-lg shadow-sm border border-red-200 p-5">
        <h2 className="text-lg font-semibold text-red-700 mb-2 flex items-center gap-2">
          <Trash2 size={18} />
          {t("profile.deleteAccount")}
        </h2>

        {!confirmDelete ? (
          <button
            onClick={() => setConfirmDelete(true)}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-400"
          >
            {t("profile.deleteAccount")}
          </button>
        ) : (
          <div>
            <p className="text-sm text-gray-700 mb-3">
              {t("profile.deleteConfirm")}
            </p>
            <div className="flex gap-2">
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-400"
              >
                {t("profile.deleteAccount")}
              </button>
              <button
                onClick={() => setConfirmDelete(false)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm hover:bg-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-400"
              >
                {t("profile.cancel")}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
