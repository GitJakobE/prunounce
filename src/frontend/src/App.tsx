import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./components/AuthProvider";
import ProtectedRoute from "./components/ProtectedRoute";
import RouteAnnouncer from "./components/RouteAnnouncer";
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import SelectHostPage from "./pages/SelectHostPage";
import CategoriesPage from "./pages/CategoriesPage";
import CategoryDetailPage from "./pages/CategoryDetailPage";
import SearchPage from "./pages/SearchPage";
import ProfilePage from "./pages/ProfilePage";
import AddWordPage from "./pages/AddWordPage";
import StoriesPage from "./pages/StoriesPage";
import StoryReadingPage from "./pages/StoryReadingPage";
import ReviewDashboardPage from "./pages/ReviewDashboardPage";
import "./i18n";

function RequireHost({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  if (!user?.hostId) return <Navigate to="/select-host" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <RouteAnnouncer />
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Host selection (protected, but no host required) */}
          <Route
            path="/select-host"
            element={
              <ProtectedRoute>
                <SelectHostPage />
              </ProtectedRoute>
            }
          />

          {/* Protected routes requiring a host */}
          <Route
            element={
              <ProtectedRoute>
                <RequireHost>
                  <Layout />
                </RequireHost>
              </ProtectedRoute>
            }
          >
            <Route index element={<CategoriesPage />} />
            <Route path="/categories/:id" element={<CategoryDetailPage />} />
            <Route path="/stories" element={<StoriesPage />} />
            <Route path="/stories/:id" element={<StoryReadingPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/add-word" element={<AddWordPage />} />
            <Route path="/review/reports" element={<ReviewDashboardPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>

          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
