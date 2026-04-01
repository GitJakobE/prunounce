import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { getHosts } from "../services/api";
import { useAuth } from "./AuthProvider";
import type { Host } from "../types";

export default function HostBanner() {
  const { i18n } = useTranslation();
  const { user } = useAuth();
  const [host, setHost] = useState<Host | null>(null);
  const lang = i18n.language;

  useEffect(() => {
    getHosts()
      .then(({ hosts }) => {
        const selected = hosts.find((h) => h.id === user?.hostId) || hosts[0];
        setHost(selected);
      })
      .catch(() => {});
  }, [user?.hostId]);

  if (!host) return null;

  return (
    <div className="flex items-center gap-4 mb-6 p-4 rounded-xl bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200">
      <img
        src={host.imageUrl}
        alt={host.name}
        className="w-14 h-14 rounded-full object-cover"
      />
      <div>
        <div className="font-bold text-gray-900 text-lg">{host.name}</div>
        <p className="text-gray-700 text-sm italic">
          "{lang === "it" ? host.greetingIt : lang === "da" ? host.greetingDa : host.greetingEn}"
        </p>
      </div>
    </div>
  );
}
