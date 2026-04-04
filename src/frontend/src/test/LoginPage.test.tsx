import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import LoginPage from "../pages/LoginPage";

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
        "auth.login": "Log In",
        "auth.email": "Email",
        "auth.password": "Password",
        "auth.noAccount": "No account?",
        "auth.register": "Register",
        "auth.welcomeTitle": "Welcome",
        "auth.welcomeDescription": "Learn Italian",
        "auth.invalidCredentials": "Invalid credentials",
      };
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

import { login as apiLogin } from "../services/api";

vi.mock("../services/api", () => ({
  login: vi.fn().mockResolvedValue({
    token: "test-token",
    user: { id: "1", email: "test@test.com", language: "en", displayName: null, hostId: "marco" },
  }),
}));

describe("LoginPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders login form", () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByRole("heading", { name: "Log In" })).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  it("has a link to register page", () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Register")).toBeInTheDocument();
  });

  it("submits form and navigates on success", async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "test@test.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "Password1" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Log In" }));

    await waitFor(() => {
      expect(mockSetAuth).toHaveBeenCalledWith("test-token", expect.any(Object));
      expect(mockNavigate).toHaveBeenCalledWith("/");
    });
  });

  it("shows error with role='alert' on login failure", async () => {
    vi.mocked(apiLogin).mockRejectedValueOnce(new Error("fail"));
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "bad@test.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "wrongpass" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Log In" }));

    await waitFor(() => {
      const alert = screen.getByRole("alert");
      expect(alert).toHaveTextContent("Invalid credentials");
    });
  });
});
