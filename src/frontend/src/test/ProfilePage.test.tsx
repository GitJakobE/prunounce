import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import ProfilePage from "../pages/ProfilePage";

vi.mock("../components/AuthProvider", () => ({
  useAuth: () => ({
    user: { id: "1", email: "test@test.com", language: "en", displayName: "Test", hostId: "marco" },
    token: "test-token",
    loading: false,
    setAuth: vi.fn(),
    logout: vi.fn(),
  }),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return { ...actual, useNavigate: () => vi.fn() };
});

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => {
      const map: Record<string, string> = {
        "profile.title": "Profile",
        "profile.progress": "Progress",
        "profile.progressSummary": "0 / 0",
        "profile.language": "Language",
        "profile.save": "Save",
        "profile.deleteAccount": "Delete account",
        "profile.deleteConfirm": "Are you sure?",
        "profile.cancel": "Cancel",
        "auth.email": "Email",
        "auth.displayName": "Display name",
        "languages.en": "English",
        "languages.da": "Danish",
        "languages.it": "Italian",
      };
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

vi.mock("../services/api", () => ({
  getProfile: vi.fn().mockResolvedValue({
    user: { id: "1", email: "test@test.com", displayName: "Test", language: "en", hostId: "marco" },
    progress: { totalWords: 10, listenedWords: 5 },
  }),
  updateProfile: vi.fn(),
  deleteAccount: vi.fn(),
}));

describe("ProfilePage", () => {
  it("renders email label with htmlFor matching input id", () => {
    render(
      <MemoryRouter>
        <ProfilePage />
      </MemoryRouter>
    );
    const emailInput = screen.getByLabelText("Email");
    expect(emailInput).toHaveAttribute("id", "email");
    expect(emailInput).toBeDisabled();
  });
});
