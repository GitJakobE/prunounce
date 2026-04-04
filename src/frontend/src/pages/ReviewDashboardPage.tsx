import { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { ChevronLeft, ChevronRight, CheckCircle, XCircle, Eye } from "lucide-react";
import { getReports, updateReport } from "../services/api";
import type { ContentReport } from "../types";

const CATEGORIES = [
  "grammar_spelling",
  "wrong_translation",
  "pronunciation",
  "formatting",
  "other",
] as const;

const STATUSES = ["new", "reviewed", "resolved", "dismissed"] as const;
const PAGE_SIZE = 20;

export default function ReviewDashboardPage() {
  const { t } = useTranslation();

  // Filters
  const [statusFilter, setStatusFilter] = useState<string>("new");
  const [contentTypeFilter, setContentTypeFilter] = useState<string>("");
  const [categoryFilter, setCategoryFilter] = useState<string>("");
  const [languageFilter, setLanguageFilter] = useState<string>("");

  // Data
  const [reports, setReports] = useState<ContentReport[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);

  // Expanded report
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [resolutionNote, setResolutionNote] = useState("");
  const [actionLoading, setActionLoading] = useState(false);

  const fetchReports = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string | number> = { limit: PAGE_SIZE, offset };
      if (statusFilter) params.status = statusFilter;
      if (contentTypeFilter) params.content_type = contentTypeFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (languageFilter) params.language = languageFilter;
      const data = await getReports(params as Parameters<typeof getReports>[0]);
      setReports(data.items);
      setTotal(data.total);
    } catch {
      // silently handle
    } finally {
      setLoading(false);
    }
  }, [statusFilter, contentTypeFilter, categoryFilter, languageFilter, offset]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  // Reset offset when filters change
  useEffect(() => {
    setOffset(0);
  }, [statusFilter, contentTypeFilter, categoryFilter, languageFilter]);

  const handleAction = async (reportId: string, newStatus: string) => {
    setActionLoading(true);
    try {
      await updateReport(reportId, {
        status: newStatus,
        resolutionNote: resolutionNote || undefined,
      });
      setResolutionNote("");
      setExpandedId(null);
      await fetchReports();
    } catch {
      // silently handle
    } finally {
      setActionLoading(false);
    }
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);
  const currentPage = Math.floor(offset / PAGE_SIZE) + 1;

  const statusColor = (status: string) => {
    switch (status) {
      case "new": return "bg-blue-100 text-blue-800";
      case "reviewed": return "bg-yellow-100 text-yellow-800";
      case "resolved": return "bg-green-100 text-green-800";
      case "dismissed": return "bg-gray-100 text-gray-600";
      default: return "bg-gray-100 text-gray-600";
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">{t("review.title")}</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        {/* Status filter tabs */}
        <div className="flex gap-1">
          <button
            onClick={() => setStatusFilter("")}
            className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
              !statusFilter ? "bg-green-700 text-white border-green-700" : "bg-white text-gray-600 border-gray-300 hover:border-green-400"
            }`}
          >
            {t("review.allStatuses")}
          </button>
          {STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                statusFilter === s ? "bg-green-700 text-white border-green-700" : "bg-white text-gray-600 border-gray-300 hover:border-green-400"
              }`}
            >
              {t(`review.status.${s}`)}
            </button>
          ))}
        </div>

        {/* Content type filter */}
        <select
          value={contentTypeFilter}
          onChange={(e) => setContentTypeFilter(e.target.value)}
          className="text-xs border border-gray-300 rounded-lg px-3 py-1.5"
        >
          <option value="">{t("review.allTypes")}</option>
          <option value="story">{t("review.type.story")}</option>
          <option value="word">{t("review.type.word")}</option>
        </select>

        {/* Category filter */}
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="text-xs border border-gray-300 rounded-lg px-3 py-1.5"
        >
          <option value="">{t("review.allCategories")}</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{t(`reports.categories.${c}`)}</option>
          ))}
        </select>

        {/* Language filter */}
        <select
          value={languageFilter}
          onChange={(e) => setLanguageFilter(e.target.value)}
          className="text-xs border border-gray-300 rounded-lg px-3 py-1.5"
        >
          <option value="">{t("review.allLanguages")}</option>
          <option value="it">Italian</option>
          <option value="da">Danish</option>
          <option value="en">English</option>
          <option value="es">Spanish</option>
        </select>
      </div>

      {/* Report list */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700" />
        </div>
      ) : reports.length === 0 ? (
        <div className="text-center py-12 text-gray-500">{t("review.empty")}</div>
      ) : (
        <>
          {/* Desktop table */}
          <div className="hidden md:block">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 text-left text-xs text-gray-500 uppercase tracking-wide">
                  <th className="pb-2 pr-4">{t("review.columns.type")}</th>
                  <th className="pb-2 pr-4">{t("review.columns.category")}</th>
                  <th className="pb-2 pr-4">{t("review.columns.description")}</th>
                  <th className="pb-2 pr-4">{t("review.columns.status")}</th>
                  <th className="pb-2 pr-4">{t("review.columns.date")}</th>
                  <th className="pb-2">{t("review.columns.actions")}</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report) => (
                  <tr
                    key={report.id}
                    className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer"
                    onClick={() => setExpandedId(expandedId === report.id ? null : report.id)}
                  >
                    <td className="py-3 pr-4">
                      <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-700">
                        {report.contentType === "story" ? "📖" : "📝"} {t(`review.type.${report.contentType}`)}
                      </span>
                    </td>
                    <td className="py-3 pr-4 text-gray-700">{t(`reports.categories.${report.category}`)}</td>
                    <td className="py-3 pr-4 text-gray-600 max-w-xs truncate">{report.description || "—"}</td>
                    <td className="py-3 pr-4">
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(report.status)}`}>
                        {t(`review.status.${report.status}`)}
                      </span>
                    </td>
                    <td className="py-3 pr-4 text-gray-500 text-xs">
                      {new Date(report.createdAt).toLocaleDateString()}
                    </td>
                    <td className="py-3">{expandedId !== report.id && <Eye size={14} className="text-gray-400" />}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile cards */}
          <div className="md:hidden space-y-3">
            {reports.map((report) => (
              <div
                key={report.id}
                className="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-gray-300"
                onClick={() => setExpandedId(expandedId === report.id ? null : report.id)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-700">
                    {report.contentType === "story" ? "📖" : "📝"} {t(`review.type.${report.contentType}`)}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(report.status)}`}>
                    {t(`review.status.${report.status}`)}
                  </span>
                </div>
                <p className="text-sm text-gray-700 mb-1">{t(`reports.categories.${report.category}`)}</p>
                <p className="text-xs text-gray-500 truncate">{report.description || "—"}</p>
              </div>
            ))}
          </div>

          {/* Expanded detail / action panel */}
          {expandedId && (() => {
            const report = reports.find((r) => r.id === expandedId);
            if (!report) return null;
            return (
              <div className="mt-4 border border-gray-200 rounded-lg p-5 bg-gray-50">
                <h3 className="font-semibold text-gray-900 mb-3">{t("review.reportDetail")}</h3>
                <dl className="grid grid-cols-2 gap-2 text-sm mb-4">
                  <dt className="text-gray-500">{t("review.columns.type")}</dt>
                  <dd>{t(`review.type.${report.contentType}`)}</dd>
                  <dt className="text-gray-500">{t("review.columns.category")}</dt>
                  <dd>{t(`reports.categories.${report.category}`)}</dd>
                  <dt className="text-gray-500">{t("review.columns.status")}</dt>
                  <dd>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(report.status)}`}>
                      {t(`review.status.${report.status}`)}
                    </span>
                  </dd>
                  <dt className="text-gray-500">{t("review.columns.date")}</dt>
                  <dd>{new Date(report.createdAt).toLocaleString()}</dd>
                </dl>
                {report.description && (
                  <div className="mb-4">
                    <span className="text-xs text-gray-500 uppercase tracking-wide">{t("reports.description")}</span>
                    <p className="text-sm text-gray-800 mt-1">{report.description}</p>
                  </div>
                )}
                {report.resolutionNote && (
                  <div className="mb-4">
                    <span className="text-xs text-gray-500 uppercase tracking-wide">{t("review.resolutionNote")}</span>
                    <p className="text-sm text-gray-800 mt-1">{report.resolutionNote}</p>
                  </div>
                )}

                {/* Actions */}
                {(report.status === "new" || report.status === "reviewed") && (
                  <div className="space-y-3 border-t border-gray-200 pt-4">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">{t("review.resolutionNote")}</label>
                      <textarea
                        value={resolutionNote}
                        onChange={(e) => setResolutionNote(e.target.value)}
                        maxLength={500}
                        rows={2}
                        placeholder={t("review.resolutionNotePlaceholder")}
                        className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-300 resize-none"
                      />
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {report.status === "new" && (
                        <button
                          onClick={() => handleAction(report.id, "reviewed")}
                          disabled={actionLoading}
                          className="inline-flex items-center gap-1.5 px-3 py-2 bg-yellow-500 text-white rounded-lg text-sm font-medium hover:bg-yellow-600 transition-colors disabled:opacity-60"
                        >
                          <Eye size={14} />
                          {t("review.actions.markReviewed")}
                        </button>
                      )}
                      <button
                        onClick={() => handleAction(report.id, "resolved")}
                        disabled={actionLoading}
                        className="inline-flex items-center gap-1.5 px-3 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 transition-colors disabled:opacity-60"
                      >
                        <CheckCircle size={14} />
                        {t("review.actions.resolve")}
                      </button>
                      <button
                        onClick={() => handleAction(report.id, "dismissed")}
                        disabled={actionLoading}
                        className="inline-flex items-center gap-1.5 px-3 py-2 bg-gray-500 text-white rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors disabled:opacity-60"
                      >
                        <XCircle size={14} />
                        {t("review.actions.dismiss")}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })()}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-6">
              <span className="text-sm text-gray-500">
                {t("review.showing", {
                  from: offset + 1,
                  to: Math.min(offset + PAGE_SIZE, total),
                  total,
                })}
              </span>
              <div className="flex gap-2">
                <button
                  onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
                  disabled={offset === 0}
                  className="p-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-40"
                >
                  <ChevronLeft size={16} />
                </button>
                <span className="flex items-center text-sm text-gray-600">
                  {currentPage} / {totalPages}
                </span>
                <button
                  onClick={() => setOffset(offset + PAGE_SIZE)}
                  disabled={offset + PAGE_SIZE >= total}
                  className="p-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-40"
                >
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
