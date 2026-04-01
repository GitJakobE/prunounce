import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { getHosts, updateProfile } from "../services/api";
import { useAuth } from "./AuthProvider";
import type { Host } from "../types";

const COLOR_MAP: Record<string, string> = {
  red: "border-red-400 bg-red-50",
  blue: "border-blue-400 bg-blue-50",
  purple: "border-purple-400 bg-purple-50",
  amber: "border-amber-400 bg-amber-50",
  teal: "border-teal-400 bg-teal-50",
  indigo: "border-indigo-400 bg-indigo-50",
  cyan: "border-cyan-400 bg-cyan-50",
  rose: "border-rose-400 bg-rose-50",
  slate: "border-slate-400 bg-slate-50",
  emerald: "border-emerald-400 bg-emerald-50",
  orange: "border-orange-400 bg-orange-50",
  violet: "border-violet-400 bg-violet-50",
};

const COLOR_SELECTED: Record<string, string> = {
  red: "ring-red-400 border-red-500 bg-red-100",
  blue: "ring-blue-400 border-blue-500 bg-blue-100",
  purple: "ring-purple-400 border-purple-500 bg-purple-100",
  amber: "ring-amber-400 border-amber-500 bg-amber-100",
  teal: "ring-teal-400 border-teal-500 bg-teal-100",
  indigo: "ring-indigo-400 border-indigo-500 bg-indigo-100",
  cyan: "ring-cyan-400 border-cyan-500 bg-cyan-100",
  rose: "ring-rose-400 border-rose-500 bg-rose-100",
  slate: "ring-slate-400 border-slate-500 bg-slate-100",
  emerald: "ring-emerald-400 border-emerald-500 bg-emerald-100",
  orange: "ring-orange-400 border-orange-500 bg-orange-100",
  violet: "ring-violet-400 border-violet-500 bg-violet-100",
};

export default function HostSelector() {
  const { t, i18n } = useTranslation();
  const { user, token, setAuth } = useAuth();
  const [hosts, setHosts] = useState<Host[]>([]);
  const [loading, setLoading] = useState(true);
  const lang = i18n.language;

  useEffect(() => {
    getHosts()
      .then(({ hosts }) => setHosts(hosts))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function selectHost(hostId: string) {
    if (!token || !user) return;
    try {
      const { user: updated } = await updateProfile({ hostId });
      setAuth(token, updated);
    } catch {
      // ignore
    }
  }

  if (loading || hosts.length === 0) return null;

  return (
    <div className="mb-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-3">
        {t("host.title")}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
        {hosts.map((host) => {
          const isSelected = user?.hostId === host.id;
          return (
            <button
              key={host.id}
              onClick={() => selectHost(host.id)}
              className={`p-4 rounded-xl border-2 text-left transition-all focus:outline-none focus:ring-2 focus:ring-green-400 ${
                isSelected
                  ? `ring-2 ${COLOR_SELECTED[host.color] || "ring-green-400 border-green-500 bg-green-100"}`
                  : `${COLOR_MAP[host.color] || "border-gray-200 bg-gray-50"} hover:shadow-md`
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <img
                  src={host.imageUrl}
                  alt={host.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div className="font-semibold text-gray-900">{host.name}</div>
              </div>
              <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                {lang === "it" ? host.descriptionIt : lang === "da" ? host.descriptionDa : host.descriptionEn}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
