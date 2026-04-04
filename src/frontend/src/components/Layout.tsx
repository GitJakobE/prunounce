import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { LayoutGrid, BookOpen, UserCircle, LogOut } from "lucide-react";
import { useAuth } from "./AuthProvider";
import LanguageSwitcher from "./LanguageSwitcher";
import { useEffect, useState } from "react";
import { getHosts } from "../services/api";

export default function Layout() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [hostEmoji, setHostEmoji] = useState<string>("");
  const [hostName, setHostName] = useState<string>("");

  useEffect(() => {
    if (!user?.hostId) return;
    getHosts().then(({ hosts }) => {
      const host = hosts.find((h) => h.id === user.hostId);
      if (host) {
        setHostEmoji(host.emoji);
        setHostName(host.name);
      }
    });
  }, [user?.hostId]);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-1.5 px-3 py-2.5 rounded text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-white/50 ${
      isActive
        ? "bg-white/20 text-white font-semibold"
        : "text-white/80 hover:text-white hover:bg-white/10"
    }`;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-green-800 text-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4 flex-wrap">
          <NavLink to="/" className="text-xl font-bold tracking-tight mr-4">
            🇮🇹 {t("app.title")}
          </NavLink>

          <nav className="flex items-center gap-1 flex-1">
            <NavLink to="/" end className={linkClass}>
              <LayoutGrid size={16} />
              {t("nav.categories")}
            </NavLink>
            <NavLink to="/stories" className={linkClass}>
              <BookOpen size={16} />
              {t("nav.stories")}
            </NavLink>
            <NavLink to="/profile" className={linkClass}>
              <UserCircle size={16} />
              {t("nav.profile")}
            </NavLink>
          </nav>

          <LanguageSwitcher />

          {user?.hostId && (
            <button
              onClick={() => navigate("/select-host")}
              className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-lg hover:bg-white/30 transition-colors focus:outline-none focus:ring-2 focus:ring-white/50"
              title={hostName || undefined}
              aria-label={t("nav.changeHost")}
            >
              {hostEmoji || "👤"}
            </button>
          )}

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3 py-2.5 rounded text-sm text-white/80 hover:text-white hover:bg-white/10 transition-colors focus:outline-none focus:ring-2 focus:ring-white/50"
          >
            <LogOut size={16} />
            {t("nav.logout")}
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
