import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../components/AuthProvider";
import { register as apiRegister } from "../services/api";

export default function RegisterPage() {
  const { t, i18n } = useTranslation();
  const { setAuth } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [language, setLanguage] = useState(i18n.language);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const { token, user } = await apiRegister(
        email,
        password,
        language,
        displayName || undefined
      );
      setAuth(token, user);
      navigate("/");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(t("errors.generic"));
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 bg-green-800 text-white flex-col justify-center px-16">
        <h1 className="text-4xl font-bold mb-4">🇮🇹 {t("auth.welcomeTitle")}</h1>
        <p className="text-lg text-green-100">{t("auth.welcomeDescription")}</p>
      </div>

      <div className="flex-1 flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 lg:hidden">
            🇮🇹 {t("app.title")}
          </h2>
          <h3 className="text-xl font-semibold text-gray-800 mb-6">
            {t("auth.register")}
          </h3>

          {error && (
            <div role="alert" className="bg-red-50 text-red-700 px-4 py-3 rounded mb-4 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                {t("auth.email")}
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                {t("auth.password")}
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                {t("auth.passwordHint")}
              </p>
            </div>

            <div>
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

            <div>
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
                <option value="es">{t("languages.es")}</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 bg-green-700 text-white rounded-lg font-medium hover:bg-green-800 disabled:opacity-60 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400"
            >
              {submitting ? "…" : t("auth.register")}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-600">
            {t("auth.hasAccount")}{" "}
            <Link
              to="/login"
              className="text-green-700 font-medium hover:underline"
            >
              {t("auth.login")}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
