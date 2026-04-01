import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import app from "../app";
import prisma from "../db";

/**
 * Helper: register a user and return token + userId.
 */
async function registerUser(email: string, password = "Password1") {
  const res = await request(app)
    .post("/api/auth/register")
    .send({ email, password, language: "en" });
  return {
    token: res.body.token as string,
    userId: res.body.user.id as string,
  };
}

/**
 * Helper: select a host for a user via the profile API.
 */
async function selectHost(token: string, hostId: string) {
  return request(app)
    .patch("/api/profile")
    .set("Authorization", `Bearer ${token}`)
    .send({ hostId });
}

/**
 * Seed Italian and Danish words in the same category to test language filtering.
 */
async function seedMultiLangData() {
  const cat = await prisma.category.create({
    data: { id: "cat-greet", nameEn: "Greetings", nameDa: "Hilsener", nameIt: "Saluti", order: 1 },
  });

  const wIt = await prisma.word.create({
    data: {
      id: "w-ciao",
      word: "ciao",
      language: "it",
      phoneticHint: "CHOW",
      translationEn: "hello",
      translationDa: "hej",
      translationIt: "ciao",
      difficulty: "beginner",
      source: "seed",
      exampleIt: "Ciao, come stai?",
      exampleEn: "Hello, how are you?",
      exampleDa: "Hej, hvordan har du det?",
    },
  });

  const wDa = await prisma.word.create({
    data: {
      id: "w-hej",
      word: "hej",
      language: "da",
      phoneticHint: "HI",
      translationEn: "hello",
      translationDa: "hej",
      translationIt: "ciao",
      difficulty: "beginner",
      source: "seed",
      exampleDa: "Hej, hvordan har du det?",
      exampleEn: "Hello, how are you?",
    },
  });

  const wEn = await prisma.word.create({
    data: {
      id: "w-hello",
      word: "hello",
      language: "en",
      phoneticHint: "heh-LOH",
      translationEn: "hello",
      translationDa: "hej",
      translationIt: "ciao",
      difficulty: "beginner",
      source: "seed",
      exampleEn: "Hello there!",
    },
  });

  await prisma.wordCategory.createMany({
    data: [
      { wordId: wIt.id, categoryId: cat.id },
      { wordId: wDa.id, categoryId: cat.id },
      { wordId: wEn.id, categoryId: cat.id },
    ],
  });

  return { cat, wIt, wDa, wEn };
}

describe("Integration — Multi-Language & UGC", () => {
  let token: string;
  let userId: string;

  beforeEach(async () => {
    const reg = await registerUser("integrate@test.com");
    token = reg.token;
    userId = reg.userId;
  });

  // ─── Host Switching & Dictionary Scoping ────────────────────────

  describe("Host switching changes dictionary content", () => {
    it("returns Italian words when an Italian host is selected", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco"); // Italian host

      const res = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(res.status).toBe(200);
      const cat = res.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(cat).toBeDefined();
      expect(cat.totalWords).toBe(1); // only "ciao"
    });

    it("returns Danish words when a Danish host is selected", async () => {
      await seedMultiLangData();
      await selectHost(token, "anders"); // Danish host

      const res = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);

      const cat = res.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(cat.totalWords).toBe(1); // only "hej"
    });

    it("returns English words when an English host is selected", async () => {
      await seedMultiLangData();
      await selectHost(token, "james"); // English host

      const res = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);

      const cat = res.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(cat.totalWords).toBe(1); // only "hello"
    });
  });

  // ─── Reference Language Translations ────────────────────────────

  describe("Reference language switches translations", () => {
    it("returns English translations with lang=en", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      const res = await request(app)
        .get("/api/dictionary/categories/cat-greet/words?lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(res.body.words[0].translation).toBe("hello");
    });

    it("returns Danish translations with lang=da", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      const res = await request(app)
        .get("/api/dictionary/categories/cat-greet/words?lang=da")
        .set("Authorization", `Bearer ${token}`);

      expect(res.body.words[0].translation).toBe("hej");
    });

    it("returns category names in the reference language", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      const resEn = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);
      const catEn = resEn.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(catEn.name).toBe("Greetings");

      const resDa = await request(app)
        .get("/api/dictionary/categories?lang=da")
        .set("Authorization", `Bearer ${token}`);
      const catDa = resDa.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(catDa.name).toBe("Hilsener");
    });
  });

  // ─── Search Scoping ─────────────────────────────────────────────

  describe("Search scopes to target language", () => {
    it("Italian host searches only Italian words", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      const res = await request(app)
        .get("/api/search?q=ciao&lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(res.body.results.length).toBe(1);
      expect(res.body.results[0].word).toBe("ciao");
    });

    it("does not leak words from other languages", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco"); // Italian host

      const res = await request(app)
        .get("/api/search?q=hej&lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(res.body.results.length).toBe(0);
    });
  });

  // ─── User Word Contribution ─────────────────────────────────────

  describe("Word contribution flow", () => {
    it("contributes a word and it appears in dictionary", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      // Contribute new Italian word
      const postRes = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "arrivederci", translation: "goodbye" });

      expect(postRes.status).toBe(201);
      expect(postRes.body.word).toBe("arrivederci");
      expect(postRes.body.language).toBe("it");
      expect(postRes.body.audioGenerating).toBe(true);

      // Verify it appears in search
      const searchRes = await request(app)
        .get("/api/search?q=arrivederci&lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(searchRes.body.results.length).toBe(1);
      expect(searchRes.body.results[0].word).toBe("arrivederci");
    });

    it("returns 409 for duplicate words", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "ciao", translation: "hello" });

      expect(res.status).toBe(409);
      expect(res.body.existingWordId).toBe("w-ciao");
    });

    it("contributed word appears in the correct language only", async () => {
      await seedMultiLangData();
      await selectHost(token, "anders"); // Danish host

      await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "farvel", translation: "goodbye" });

      // Switch to Italian host — word should NOT appear
      await selectHost(token, "marco");
      const searchRes = await request(app)
        .get("/api/search?q=farvel&lang=en")
        .set("Authorization", `Bearer ${token}`);

      expect(searchRes.body.results.length).toBe(0);
    });
  });

  // ─── Progress Isolation ─────────────────────────────────────────

  describe("Progress isolation across languages", () => {
    it("progress in Italian does not appear for Danish host", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      // Listen to Italian word
      await request(app)
        .post("/api/dictionary/words/w-ciao/listened")
        .set("Authorization", `Bearer ${token}`);

      // Check progress on Italian
      const itRes = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);
      const itCat = itRes.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(itCat.listenedWords).toBe(1);

      // Switch to Danish host
      await selectHost(token, "anders");

      const daRes = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);
      const daCat = daRes.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(daCat.listenedWords).toBe(0);
    });

    it("progress is preserved when switching back", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      await request(app)
        .post("/api/dictionary/words/w-ciao/listened")
        .set("Authorization", `Bearer ${token}`);

      // Switch away and back
      await selectHost(token, "anders");
      await selectHost(token, "marco");

      const res = await request(app)
        .get("/api/dictionary/categories?lang=en")
        .set("Authorization", `Bearer ${token}`);
      const cat = res.body.categories.find((c: { id: string }) => c.id === "cat-greet");
      expect(cat.listenedWords).toBe(1);
    });

    it("profile progress is scoped to target language", async () => {
      await seedMultiLangData();
      await selectHost(token, "marco");

      await request(app)
        .post("/api/dictionary/words/w-ciao/listened")
        .set("Authorization", `Bearer ${token}`);

      // Italian host: 1 listened out of 1
      const itProfile = await request(app)
        .get("/api/profile")
        .set("Authorization", `Bearer ${token}`);
      expect(itProfile.body.progress.totalWords).toBe(1);
      expect(itProfile.body.progress.listenedWords).toBe(1);

      // Switch to Danish: 0 listened out of 1
      await selectHost(token, "anders");
      const daProfile = await request(app)
        .get("/api/profile")
        .set("Authorization", `Bearer ${token}`);
      expect(daProfile.body.progress.totalWords).toBe(1);
      expect(daProfile.body.progress.listenedWords).toBe(0);
    });
  });

  // ─── New Registration Has No Default Host ───────────────────────

  describe("Registration defaults", () => {
    it("new user has no default hostId", async () => {
      const res = await request(app)
        .post("/api/auth/register")
        .send({ email: "fresh@test.com", password: "Password1" });

      expect(res.status).toBe(201);
      expect(res.body.user.hostId).toBeNull();
    });
  });

  // ─── Hosts Endpoint ─────────────────────────────────────────────

  describe("Hosts endpoint", () => {
    it("returns all 12 hosts grouped by language", async () => {
      const res = await request(app)
        .get("/api/hosts")
        .set("Authorization", `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.hosts.length).toBe(12);

      const langs = new Set(res.body.hosts.map((h: { language: string }) => h.language));
      expect(langs).toEqual(new Set(["it", "da", "en"]));

      const itHosts = res.body.hosts.filter((h: { language: string }) => h.language === "it");
      expect(itHosts.length).toBe(4);
    });
  });
});
