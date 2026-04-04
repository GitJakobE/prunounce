import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import ReviewDashboardPage from "../pages/ReviewDashboardPage";

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
    t: (key: string, params?: Record<string, unknown>) => {
      const map: Record<string, string> = {
        "review.title": "Content Review",
        "review.allStatuses": "All",
        "review.allTypes": "All types",
        "review.allCategories": "All categories",
        "review.allLanguages": "All languages",
        "review.status.new": "New",
        "review.status.reviewed": "Reviewed",
        "review.status.resolved": "Resolved",
        "review.status.dismissed": "Dismissed",
        "review.type.story": "Story",
        "review.type.word": "Word",
        "review.columns.type": "Type",
        "review.columns.category": "Category",
        "review.columns.description": "Description",
        "review.columns.status": "Status",
        "review.columns.date": "Date",
        "review.columns.actions": "Actions",
        "review.empty": "No reports match the current filters.",
        "review.reportDetail": "Report Details",
        "review.actions.markReviewed": "Mark Reviewed",
        "review.actions.resolve": "Resolve",
        "review.actions.dismiss": "Dismiss",
        "reports.categories.grammar_spelling": "Grammar / Spelling",
        "reports.categories.wrong_translation": "Wrong translation",
        "reports.categories.pronunciation": "Pronunciation issue",
        "reports.categories.formatting": "Formatting issue",
        "reports.categories.other": "Other",
        "reports.description": "Description",
        "review.resolutionNote": "Resolution note",
        "review.resolutionNotePlaceholder": "Add a note (optional)…",
      };
      if (key === "review.showing" && params) {
        return `Showing ${params.from}–${params.to} of ${params.total} reports`;
      }
      return map[key] || key;
    },
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

const mockGetReports = vi.fn();
const mockUpdateReport = vi.fn();

vi.mock("../services/api", () => ({
  getReports: (...args: unknown[]) => mockGetReports(...args),
  updateReport: (...args: unknown[]) => mockUpdateReport(...args),
}));

function renderPage() {
  return render(
    <MemoryRouter initialEntries={["/review/reports"]}>
      <Routes>
        <Route path="/review/reports" element={<ReviewDashboardPage />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("ReviewDashboardPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading then empty state when no reports", async () => {
    mockGetReports.mockResolvedValue({ items: [], total: 0 });
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("No reports match the current filters.")).toBeInTheDocument();
    });
  });

  it("renders reports from API", async () => {
    mockGetReports.mockResolvedValue({
      items: [
        {
          id: "r1",
          userId: "u1",
          contentType: "story",
          contentId: "s1",
          category: "grammar_spelling",
          description: "Typo in first paragraph",
          status: "new",
          resolutionNote: null,
          createdAt: "2025-01-15T10:00:00",
          updatedAt: "2025-01-15T10:00:00",
        },
      ],
      total: 1,
    });
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Content Review")).toBeInTheDocument();
      expect(screen.getAllByText("Typo in first paragraph").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows status filter tabs", async () => {
    mockGetReports.mockResolvedValue({ items: [], total: 0 });
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("All")).toBeInTheDocument();
      expect(screen.getByText("New")).toBeInTheDocument();
      expect(screen.getByText("Resolved")).toBeInTheDocument();
      expect(screen.getByText("Dismissed")).toBeInTheDocument();
    });
  });

  it("filters by status when clicking a tab", async () => {
    mockGetReports.mockResolvedValue({ items: [], total: 0 });
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Resolved")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Resolved"));

    await waitFor(() => {
      expect(mockGetReports).toHaveBeenCalledWith(
        expect.objectContaining({ status: "resolved" })
      );
    });
  });

  it("calls updateReport when resolving", async () => {
    mockGetReports.mockResolvedValue({
      items: [
        {
          id: "r1",
          userId: "u1",
          contentType: "story",
          contentId: "s1",
          category: "grammar_spelling",
          description: "Issue here",
          status: "new",
          resolutionNote: null,
          createdAt: "2025-01-15T10:00:00",
          updatedAt: "2025-01-15T10:00:00",
        },
      ],
      total: 1,
    });
    mockUpdateReport.mockResolvedValue({
      id: "r1",
      status: "resolved",
    });
    renderPage();

    // Wait for report to render, then expand it
    await waitFor(() => {
      expect(screen.getAllByText("Issue here").length).toBeGreaterThanOrEqual(1);
    });

    // Click on the row to expand (use the first matching element)
    fireEvent.click(screen.getAllByText("Issue here")[0]);

    await waitFor(() => {
      expect(screen.getByText("Resolve")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Resolve"));

    await waitFor(() => {
      expect(mockUpdateReport).toHaveBeenCalledWith("r1", {
        status: "resolved",
        resolutionNote: undefined,
      });
    });
  });
});
