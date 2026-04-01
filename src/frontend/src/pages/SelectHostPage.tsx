import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { getHosts, updateProfile } from "../services/api";
import { useAuth } from "../components/AuthProvider";
import type { Host } from "../types";

const LANG_SECTIONS = [
  { lang: "it", headingKey: "selectHost.learnItalian" },
  { lang: "da", headingKey: "selectHost.learnDanish" },
  { lang: "en", headingKey: "selectHost.learnEnglish" },
];

export default function SelectHostPage() {
  const { t, i18n } = useTranslation();
  const { user, token, setAuth } = useAuth();
  const navigate = useNavigate();
  const [hosts, setHosts] = useState<Host[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const lang = i18n.language;

  useEffect(() => {
    getHosts()
      .then(({ hosts }) => setHosts(hosts))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function selectHost(hostId: string) {
    if (!token || !user || saving) return;
    setSaving(true);
    try {
      const { user: updated } = await updateProfile({ hostId });
      setAuth(token, updated);
      navigate("/", { replace: true });
    } catch {
      setSaving(false);
    }
  }

  function getDescription(host: Host): string {
    if (lang === "it") return host.descriptionIt;
    if (lang === "da") return host.descriptionDa;
    return host.descriptionEn;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">
          {t("selectHost.title")}
        </h1>
        <p className="text-gray-600 text-center mb-8">
          {t("selectHost.subtitle")}
        </p>

        {LANG_SECTIONS.map(({ lang: sectionLang, headingKey }) => {
          const sectionHosts = hosts.filter((h) => h.language === sectionLang);
          if (sectionHosts.length === 0) return null;
          return (
            <div key={sectionLang} className="mb-10">
              <h2 className="text-xl font-semibold text-gray-800 mb-4 border-b pb-2">
                {t(headingKey)}
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {sectionHosts.map((host) => (
                  <button
                    key={host.id}
                    onClick={() => selectHost(host.id)}
                    disabled={saving}
                    className="p-5 rounded-xl border-2 border-gray-200 bg-white text-left transition-all hover:shadow-lg hover:border-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 disabled:opacity-50"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <img
                        src={host.imageUrl}
                        alt={host.name}
                        className="w-14 h-14 rounded-full object-cover"
                      />
                      <div>
                        <div className="font-bold text-gray-900">{host.name}</div>
                        <span className="text-xs text-gray-500">{host.emoji}</span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-3">
                      {getDescription(host)}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
