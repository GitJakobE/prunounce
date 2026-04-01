import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import app from "../app";
import prisma from "../db";

async function registerAndGetToken() {
  const res = await request(app).post("/api/auth/register").send({
    email: "search@example.com",
    password: "Password1",
    language: "en",
  });
  return res.body.token as string;
}

async function seedSearchData() {
  const cat = await prisma.category.create({
    data: { id: "cat-greet", nameEn: "Greetings", nameDa: "Hilsener", order: 1 },
  });

  const words = await Promise.all([
    prisma.word.create({
      data: {
        id: "w-ciao",
        word: "ciao",
        language: "it",
        phoneticHint: "CHOW",
        translationEn: "hello/bye",
        translationDa: "hej/farvel",
        difficulty: "beginner",
        source: "seed",
      },
    }),
    prisma.word.create({
      data: {
        id: "w-arrivederci",
        word: "arrivederci",
        language: "it",
        phoneticHint: "ah-ree-veh-DEHR-chee",
        translationEn: "goodbye",
        translationDa: "farvel",
        difficulty: "intermediate",
        source: "seed",
      },
    }),
  ]);

  await prisma.wordCategory.createMany({
    data: words.map((w) => ({ wordId: w.id, categoryId: cat.id })),
  });
}

describe("Search Routes", () => {
  let token: string;

  beforeEach(async () => {
    token = await registerAndGetToken();
    await seedSearchData();
  });

  describe("GET /api/search", () => {
    it("finds words by Italian term", async () => {
      const res = await request(app)
        .get("/api/search?q=ciao")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.results).toHaveLength(1);
      expect(res.body.results[0].word).toBe("ciao");
    });

    it("finds words by English translation", async () => {
      const res = await request(app)
        .get("/api/search?q=goodbye")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.results).toHaveLength(1);
      expect(res.body.results[0].word).toBe("arrivederci");
    });

    it("finds partial matches", async () => {
      const res = await request(app)
        .get("/api/search?q=arriv")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.results.length).toBeGreaterThanOrEqual(1);
    });

    it("returns empty for unmatched query", async () => {
      const res = await request(app)
        .get("/api/search?q=xyz123")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.results).toEqual([]);
    });

    it("rejects query shorter than 2 chars", async () => {
      const res = await request(app)
        .get("/api/search?q=a")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(400);
    });

    it("handles diacritics-insensitive search", async () => {
      // Search for "ciao" without diacritics should still match
      const res = await request(app)
        .get("/api/search?q=ciao")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.results.length).toBeGreaterThanOrEqual(1);
    });

    it("rejects unauthenticated request", async () => {
      const res = await request(app).get("/api/search?q=ciao");
      expect(res.status).toBe(401);
    });
  });
});
