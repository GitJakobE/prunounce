import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import WordCard from "../components/WordCard";
import type { WordEntry } from "../types";

// Mock i18n
vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

// Mock api
vi.mock("../services/api", () => ({
  markListened: vi.fn().mockResolvedValue(undefined),
}));

const baseWord: WordEntry = {
  id: "w-1",
  word: "bruschetta",
  phoneticHint: "broo-SKET-tah",
  translation: "toast with toppings",
  difficulty: "beginner",
  listened: false,
  example: "I love bruschetta",
  exampleTarget: "Adoro la bruschetta",
};

describe("WordCard", () => {
  it("renders word and translation", () => {
    render(<WordCard word={baseWord} token="tok" />);
    expect(screen.getByText("bruschetta")).toBeInTheDocument();
    expect(screen.getByText("toast with toppings")).toBeInTheDocument();
  });

  it("renders phonetic hint", () => {
    render(<WordCard word={baseWord} token="tok" />);
    expect(screen.getByText("broo-SKET-tah")).toBeInTheDocument();
  });

  it("renders difficulty badge", () => {
    render(<WordCard word={baseWord} token="tok" />);
    expect(screen.getByText("categories.beginner")).toBeInTheDocument();
  });

  it("shows listened checkmark when listened", () => {
    const listened = { ...baseWord, listened: true };
    render(<WordCard word={listened} token="tok" />);
    expect(screen.getByLabelText("words.listened")).toBeInTheDocument();
  });

  it("does not show checkmark when not listened", () => {
    render(<WordCard word={baseWord} token="tok" />);
    expect(screen.queryByLabelText("words.listened")).not.toBeInTheDocument();
  });

  it("renders audio play button", () => {
    render(<WordCard word={baseWord} token="tok" />);
    expect(screen.getByRole("button")).toBeInTheDocument();
  });
});
