import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";

const prisma = new PrismaClient();

interface SeedCategory {
  id: string;
  nameEn: string;
  nameDa: string;
  nameIt?: string;
  order: number;
}

interface SeedWordIt {
  italian: string;
  phoneticHint: string;
  translationEn: string;
  translationDa: string;
  difficulty: string;
  categories: string[];
}

interface SeedWordMulti {
  word: string;
  phoneticHint: string;
  translationEn: string;
  translationDa: string;
  translationIt: string;
  difficulty: string;
  categories: string[];
}

interface SeedDataIt {
  categories: SeedCategory[];
  words: SeedWordIt[];
}

interface SeedDataMulti {
  language: string;
  words: SeedWordMulti[];
}

type ExampleMap = Record<string, { it: string; en: string; da: string }>;

function loadJson<T>(filePath: string): T {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

async function seedWords(
  words: { word: string; language: string; phoneticHint: string; translationEn: string; translationDa: string; translationIt: string; difficulty: string; categories: string[] }[],
  examples: ExampleMap,
  label: string,
) {
  console.log(`Seeding ${words.length} ${label} words...`);
  for (const w of words) {
    const ex = examples[w.word] || { it: "", en: "", da: "" };
    const word = await prisma.word.upsert({
      where: { word_language: { word: w.word, language: w.language } },
      update: {
        phoneticHint: w.phoneticHint,
        translationEn: w.translationEn,
        translationDa: w.translationDa,
        translationIt: w.translationIt,
        difficulty: w.difficulty,
        exampleIt: ex.it,
        exampleEn: ex.en,
        exampleDa: ex.da,
      },
      create: {
        word: w.word,
        language: w.language,
        source: "seed",
        phoneticHint: w.phoneticHint,
        translationEn: w.translationEn,
        translationDa: w.translationDa,
        translationIt: w.translationIt,
        difficulty: w.difficulty,
        exampleIt: ex.it,
        exampleEn: ex.en,
        exampleDa: ex.da,
      },
    });

    for (const catId of w.categories) {
      await prisma.wordCategory.upsert({
        where: { wordId_categoryId: { wordId: word.id, categoryId: catId } },
        update: {},
        create: { wordId: word.id, categoryId: catId },
      });
    }
  }
}

async function main() {
  const dataDir = path.join(__dirname, "..", "data");

  // --- Categories (from Italian seed file which has all categories) ---
  const itData: SeedDataIt = loadJson(path.join(dataDir, "seed-words.json"));
  console.log(`Seeding ${itData.categories.length} categories...`);
  for (const cat of itData.categories) {
    await prisma.category.upsert({
      where: { id: cat.id },
      update: { nameEn: cat.nameEn, nameDa: cat.nameDa, nameIt: cat.nameIt || "", order: cat.order },
      create: {
        id: cat.id,
        nameEn: cat.nameEn,
        nameDa: cat.nameDa,
        nameIt: cat.nameIt || "",
        order: cat.order,
      },
    });
  }

  // --- Italian words ---
  const itExamples: ExampleMap = loadJson(path.join(dataDir, "examples.json"));
  const itWords = itData.words.map((w) => ({
    word: w.italian,
    language: "it",
    phoneticHint: w.phoneticHint,
    translationEn: w.translationEn,
    translationDa: w.translationDa,
    translationIt: w.italian, // Italian word is its own "translation"
    difficulty: w.difficulty,
    categories: w.categories,
  }));
  await seedWords(itWords, itExamples, "Italian");

  // --- Danish words ---
  const daData: SeedDataMulti = loadJson(path.join(dataDir, "seed-words-da.json"));
  const daExamples: ExampleMap = loadJson(path.join(dataDir, "examples-da.json"));
  const daWords = daData.words.map((w) => ({ ...w, language: "da" }));
  await seedWords(daWords, daExamples, "Danish");

  // --- English words ---
  const enData: SeedDataMulti = loadJson(path.join(dataDir, "seed-words-en.json"));
  const enExamples: ExampleMap = loadJson(path.join(dataDir, "examples-en.json"));
  const enWords = enData.words.map((w) => ({ ...w, language: "en" }));
  await seedWords(enWords, enExamples, "English");

  console.log("Seed complete!");
}

main()
  .catch((e) => {
    console.error("Seed failed:", e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
