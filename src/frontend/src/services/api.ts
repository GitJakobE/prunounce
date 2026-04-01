import type { StoryListItem, StoryDetail, WordLookupResult } from "../types";

const API_BASE = "/api";

function getToken(): string | null {
  return localStorage.getItem("token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.error || "Request failed");
  }

  return res.json();
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// Auth
export function register(
  email: string,
  password: string,
  language: string,
  displayName?: string
) {
  return request<{ token: string; user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null } }>(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify({ email, password, language, displayName }),
    }
  );
}

export function login(email: string, password: string) {
  return request<{ token: string; user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null } }>(
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }
  );
}

export function googleLogin(credential: string) {
  return request<{ token: string; user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null } }>(
    "/auth/google",
    {
      method: "POST",
      body: JSON.stringify({ credential }),
    }
  );
}

export function getMe() {
  return request<{ user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null } }>(
    "/auth/me"
  );
}

// Profile
export function getProfile() {
  return request<{
    user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null };
    progress: { totalWords: number; listenedWords: number };
  }>("/profile");
}

export function updateProfile(data: { displayName?: string; language?: string; hostId?: string }) {
  return request<{ user: { id: string; email: string; displayName: string | null; language: string; hostId: string | null } }>(
    "/profile",
    { method: "PATCH", body: JSON.stringify(data) }
  );
}

export function deleteAccount() {
  return request<{ message: string }>("/profile", { method: "DELETE" });
}

// Hosts
export function getHosts() {
  return request<{
    hosts: {
      id: string;
      name: string;
      language: string;
      emoji: string;
      imageUrl: string;
      descriptionEn: string;
      descriptionDa: string;
      descriptionIt: string;
      greetingEn: string;
      greetingDa: string;
      greetingIt: string;
      color: string;
    }[];
  }>("/hosts");
}

// Dictionary
export function getCategories(lang: string) {
  return request<{
    categories: {
      id: string;
      name: string;
      totalWords: number;
      listenedWords: number;
      progressByDifficulty: { difficulty: string; total: number; listened: number }[];
    }[];
  }>(`/dictionary/categories?lang=${lang}`);
}

export function getCategoryWords(
  categoryId: string,
  lang: string,
  difficulty?: string
) {
  let url = `/dictionary/categories/${encodeURIComponent(categoryId)}/words?lang=${lang}`;
  if (difficulty) url += `&difficulty=${difficulty}`;
  return request<{
    category: { id: string; name: string };
    words: {
      id: string;
      word: string;
      phoneticHint: string;
      translation: string;
      exampleTarget: string;
      example: string;
      difficulty: string;
      listened: boolean;
    }[];
  }>(url);
}

export function markListened(wordId: string) {
  return request<{ listened: boolean }>(
    `/dictionary/words/${encodeURIComponent(wordId)}/listened`,
    { method: "POST" }
  );
}

// Search
export function searchWords(query: string, lang: string) {
  return request<{
    results: {
      id: string;
      word: string;
      phoneticHint: string;
      translation: string;
      exampleTarget: string;
      example: string;
      difficulty: string;
      listened: boolean;
      categories: { id: string; name: string }[];
    }[];
    message?: string;
  }>(`/search?q=${encodeURIComponent(query)}&lang=${lang}`);
}

// Audio URL (not a fetch — returns the URL for an <audio> element)
export function audioUrl(wordId: string): string {
  const token = getToken();
  return `${API_BASE}/audio/${encodeURIComponent(wordId)}?token=${token}`;
}

export function exampleAudioUrl(wordId: string): string {
  const token = getToken();
  return `${API_BASE}/audio/${encodeURIComponent(wordId)}/example?token=${token}`;
}

// Word contribution
export interface ContributeWordPayload {
  word: string;
  translation?: string;
  translationEn?: string;
  translationDa?: string;
  translationIt?: string;
  phoneticHint?: string;
  categoryId?: string;
  difficulty?: string;
  example?: string;
  exampleTranslation?: string;
}

export function contributeWord(data: ContributeWordPayload) {
  return request<{
    word: {
      id: string;
      word: string;
      language: string;
      phoneticHint: string;
      translation: string;
      difficulty: string;
    };
    audioGenerating: boolean;
  }>("/dictionary/words", { method: "POST", body: JSON.stringify(data) });
}

// Stories
export function getStories() {
  return request<{ stories: Record<string, StoryListItem[]> }>("/stories");
}

export function getStory(storyId: string) {
  return request<{ story: StoryDetail }>(`/stories/${encodeURIComponent(storyId)}`);
}

export function lookupWord(word: string, lang?: string) {
  const params = new URLSearchParams({ word });
  if (lang) params.set("lang", lang);
  return request<WordLookupResult>(`/dictionary/lookup?${params.toString()}`);
}

export function storyAudioUrl(storyId: string, speed: string): string {
  const token = getToken();
  return `${API_BASE}/stories/${encodeURIComponent(storyId)}/audio?speed=${encodeURIComponent(speed)}&token=${token}`;
}
