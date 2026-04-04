import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import RegisterPage from "../pages/RegisterPage";

const mockSetAuth = vi.fn();
const mockNavigate = vi.fn();

vi.mock("../components/AuthProvider", () => ({
  useAuth: () => ({
    user: null,
    token: null,
    loading: false,
    setAuth: mockSetAuth,
    logout: vi.fn(),
  }),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return { ...actual, useNavigate: () => mockNavigate };
});

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => {
      const map: Record<string, string> = {
        "auth.register": "Register",
        "auth.email": "Email",
        "auth.password": "Password",
        "auth.passwordHint": "At least 8 characters",
        "auth.displayName": "Display name",
        "auth.hasAccount": "Have an account?",
        "auth.login": "Log In",
        "auth.welcomeTitle": "Welcome",
        "auth.welcomeDescription": "Learn Italian",
        "profile.language": "Language",
        "languages.en": "English",
        "languages.da": "Danish",
        "errors.generic": "Something went wrong",
      };
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

import { register as apiRegister } from "../services/api";

vi.mock("../services/api", () => ({
  register: vi.fn().mockResolvedValue({
    token: "test-token",
    user: { id: "1", email: "test@test.com", language: "en", displayName: null, hostId: null },
  }),
}));

describe("RegisterPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders registration form", () => {
    render(
      <MemoryRouter>
        <RegisterPage />
      </MemoryRouter>
    );
    expect(screen.getByRole("heading", { name: "Register" })).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
    expect(screen.getByLabelText("Display name")).toBeInTheDocument();
  });

  it("shows error with role='alert' on registration failure", async () => {
    vi.mocked(apiRegister).mockRejectedValueOnce(new Error("Something went wrong"));
    render(
      <MemoryRouter>
        <RegisterPage />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "test@test.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "Password1" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Register" }));

    await waitFor(() => {
      const alert = screen.getByRole("alert");
      expect(alert).toHaveTextContent("Something went wrong");
    });
  });
});
