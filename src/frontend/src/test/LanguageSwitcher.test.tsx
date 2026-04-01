import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import LanguageSwitcher from "../components/LanguageSwitcher";

const mockChangeLanguage = vi.fn();
const mockSetAuth = vi.fn();

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "en", changeLanguage: mockChangeLanguage },
  }),
}));

vi.mock("../components/AuthProvider", () => ({
  useAuth: () => ({
    user: { id: "1", email: "test@test.com", language: "en", displayName: null, hostId: "marco" },
    setAuth: mockSetAuth,
  }),
}));

vi.mock("../services/api", () => ({
  updateProfile: vi.fn().mockResolvedValue({
    user: { id: "1", email: "test@test.com", language: "da", displayName: null, hostId: "marco" },
  }),
}));

describe("LanguageSwitcher", () => {
  it("renders language buttons", () => {
    render(<LanguageSwitcher />);
    expect(screen.getByText("English")).toBeInTheDocument();
    expect(screen.getByText("Dansk")).toBeInTheDocument();
    expect(screen.getByText("Italiano")).toBeInTheDocument();
  });

  it("calls changeLanguage when button is clicked", async () => {
    render(<LanguageSwitcher />);
    fireEvent.click(screen.getByText("Dansk"));
    expect(mockChangeLanguage).toHaveBeenCalledWith("da");
  });
});
