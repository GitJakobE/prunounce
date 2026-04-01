import { useTranslation } from "react-i18next";
import { updateProfile } from "../services/api";
import { useAuth } from "./AuthProvider";

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "da", label: "Dansk" },
  { code: "it", label: "Italiano" },
];

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();
  const { user, setAuth } = useAuth();
  const token = localStorage.getItem("token");

  async function handleChange(lang: string) {
    i18n.changeLanguage(lang);
    localStorage.setItem("language", lang);
    if (token && user) {
      try {
        const { user: updated } = await updateProfile({ language: lang });
        setAuth(token, updated);
      } catch {
        // Still change UI language even if API fails
      }
    }
  }

  return (
    <div className="flex gap-1">
      {LANGUAGES.map((l) => (
        <button
          key={l.code}
          onClick={() => handleChange(l.code)}
          className={`px-3 py-2 text-sm rounded transition-colors focus:outline-none focus:ring-2 focus:ring-white/50 ${
            i18n.language === l.code
              ? "bg-green-700 text-white"
              : "bg-white/20 text-white hover:bg-white/30"
          }`}
          aria-label={l.label}
        >
          {l.label}
        </button>
      ))}
    </div>
  );
}
