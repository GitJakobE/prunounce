import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import { getMe } from "../services/api";
import type { User } from "../types";
import i18n from "../i18n";

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [loading, setLoading] = useState(!!token);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    getMe()
      .then(({ user }) => {
        setUser(user);
        i18n.changeLanguage(user.language);
        localStorage.setItem("language", user.language);
      })
      .catch(() => {
        localStorage.removeItem("token");
        setToken(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  function setAuth(newToken: string, newUser: User) {
    localStorage.setItem("token", newToken);
    localStorage.setItem("language", newUser.language);
    i18n.changeLanguage(newUser.language);
    setToken(newToken);
    setUser(newUser);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, setAuth, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}
