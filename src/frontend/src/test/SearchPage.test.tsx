import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import SearchPage from "../pages/SearchPage";

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
        "nav.search": "Search",
        "search.placeholder": "Search for a word…",
        "search.minChars": "Type at least 2 characters",
      };
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

vi.mock("../services/api", () => ({
  searchWords: vi.fn().mockResolvedValue({ results: [] }),
}));

describe("SearchPage", () => {
  it("renders search input with aria-label", () => {
    render(
      <MemoryRouter>
        <SearchPage />
      </MemoryRouter>
    );
    const input = screen.getByPlaceholderText("Search for a word…");
    expect(input).toHaveAttribute("aria-label", "Search for a word…");
  });
});
