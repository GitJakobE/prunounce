import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import CategoriesPage from "../pages/CategoriesPage";

vi.mock("../components/AuthProvider", () => ({
  useAuth: () => ({
    user: { id: "1", email: "test@test.com", language: "en", displayName: null, hostId: "marco" },
    token: "test-token",
    loading: false,
    setAuth: vi.fn(),
    logout: vi.fn(),
  }),
}));

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => {
      const map: Record<string, string> = {
        "categories.title": "Word Categories",
        "categories.progress": "{{listened}} / {{total}} words",
        "categories.beginner": "Beginner",
        "categories.intermediate": "Intermediate",
        "categories.advanced": "Advanced",
      };
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

vi.mock("../services/api", () => ({
  getCategories: vi.fn().mockResolvedValue({
    categories: [
      {
        id: "cat-1",
        name: "Food & Drink",
        totalWords: 25,
        listenedWords: 5,
        progressByDifficulty: [
          { difficulty: "beginner", total: 10, listened: 3 },
          { difficulty: "intermediate", total: 10, listened: 2 },
          { difficulty: "advanced", total: 5, listened: 0 },
        ],
      },
    ],
  }),
  getHosts: vi.fn().mockResolvedValue({ hosts: [] }),
  updateProfile: vi.fn().mockResolvedValue({ user: { id: "1", email: "test@test.com", language: "en", displayName: null, hostId: "marco" } }),
}));

describe("CategoriesPage", () => {
  it("renders categories after loading", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route path="/" element={<CategoriesPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("Food & Drink")).toBeInTheDocument();
    });
  });

  it("shows page title", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route path="/" element={<CategoriesPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("Word Categories")).toBeInTheDocument();
    });
  });
});
