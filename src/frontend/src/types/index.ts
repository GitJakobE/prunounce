export interface User {
  id: string;
  email: string;
  displayName: string | null;
  language: string;
  hostId: string | null;
}

export interface Host {
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
}

export interface WordEntry {
  id: string;
  word: string;
  phoneticHint: string;
  translation: string;
  exampleTarget: string;
  example: string;
  difficulty: string;
  listened: boolean;
  categories?: { id: string; name: string }[];
}

export interface CategorySummary {
  id: string;
  name: string;
  totalWords: number;
  listenedWords: number;
  progressByDifficulty: {
    difficulty: string;
    total: number;
    listened: number;
  }[];
}

export interface ProgressSummary {
  totalWords: number;
  listenedWords: number;
}

export interface StoryListItem {
  id: string;
  slug: string;
  language: string;
  difficulty: string;
  length: string;
  title: string;
  description: string;
  estimatedReadingTime: number;
  format?: string;
  speakers?: string[] | null;
}

export interface NarrationSegment {
  type: "narration";
  text: string;
}

export interface DialogueSegment {
  type: "dialogue";
  speaker: string;
  text: string;
}

export type StorySegment = NarrationSegment | DialogueSegment;

export interface StoryDetail extends StoryListItem {
  body: string;
  segments?: StorySegment[];
}

export interface WordLookupResult {
  word: string;
  translation: string | null;
  phoneticHint: string | null;
  wordId: string | null;
}
