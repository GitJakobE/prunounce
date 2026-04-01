import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import app from "../app";
import prisma from "../db";

async function registerAndGetToken() {
  const res = await request(app).post("/api/auth/register").send({
    email: "dict@example.com",
    password: "Password1",
    language: "en",
  });
  return res.body.token as string;
}

async function seedTestData() {
  const cat = await prisma.category.create({
    data: { id: "cat-food", nameEn: "Food", nameDa: "Mad", order: 1 },
  });

  const w1 = await prisma.word.create({
    data: {
      id: "w-bruschetta",
      word: "bruschetta",
      language: "it",
      phoneticHint: "broo-SKET-tah",
      translationEn: "bruschetta",
      translationDa: "bruschetta",
      difficulty: "beginner",
      source: "seed",
    },
  });

  const w2 = await prisma.word.create({
    data: {
      id: "w-gnocchi",
      word: "gnocchi",
      language: "it",
      phoneticHint: "NYOK-kee",
      translationEn: "gnocchi",
      translationDa: "gnocchi",
      difficulty: "intermediate",
      source: "seed",
    },
  });

  await prisma.wordCategory.createMany({
    data: [
      { wordId: w1.id, categoryId: cat.id },
      { wordId: w2.id, categoryId: cat.id },
    ],
  });

  return { cat, w1, w2 };
}

describe("Dictionary Routes", () => {
  let token: string;

  beforeEach(async () => {
    token = await registerAndGetToken();
  });

  describe("GET /api/dictionary/categories", () => {
    it("returns empty list when no categories", async () => {
      const res = await request(app)
        .get("/api/dictionary/categories")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.categories).toEqual([]);
    });

    it("returns categories with progress", async () => {
      const { w1 } = await seedTestData();
      // Mark one word as listened
      await request(app)
        .post(`/api/dictionary/words/${w1.id}/listened`)
        .set("Authorization", `Bearer ${token}`);

      const res = await request(app)
        .get("/api/dictionary/categories")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.categories).toHaveLength(1);
      expect(res.body.categories[0].name).toBe("Food");
      expect(res.body.categories[0].totalWords).toBe(2);
      expect(res.body.categories[0].listenedWords).toBe(1);
    });

    it("returns Danish names when lang=da", async () => {
      await seedTestData();
      const res = await request(app)
        .get("/api/dictionary/categories?lang=da")
        .set("Authorization", `Bearer ${token}`);
      expect(res.body.categories[0].name).toBe("Mad");
    });

    it("rejects unauthenticated request", async () => {
      const res = await request(app).get("/api/dictionary/categories");
      expect(res.status).toBe(401);
    });
  });

  describe("GET /api/dictionary/categories/:id/words", () => {
    it("returns words for a category", async () => {
      await seedTestData();
      const res = await request(app)
        .get("/api/dictionary/categories/cat-food/words")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.words).toHaveLength(2);
      expect(res.body.category.name).toBe("Food");
    });

    it("filters by difficulty", async () => {
      await seedTestData();
      const res = await request(app)
        .get("/api/dictionary/categories/cat-food/words?difficulty=beginner")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.words).toHaveLength(1);
      expect(res.body.words[0].word).toBe("bruschetta");
    });

    it("returns 404 for non-existent category", async () => {
      const res = await request(app)
        .get("/api/dictionary/categories/non-existent/words")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(404);
    });
  });

  describe("POST /api/dictionary/words/:id/listened", () => {
    it("marks a word as listened", async () => {
      const { w1 } = await seedTestData();
      const res = await request(app)
        .post(`/api/dictionary/words/${w1.id}/listened`)
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.listened).toBe(true);
    });

    it("is idempotent (can be called multiple times)", async () => {
      const { w1 } = await seedTestData();
      await request(app)
        .post(`/api/dictionary/words/${w1.id}/listened`)
        .set("Authorization", `Bearer ${token}`);
      const res = await request(app)
        .post(`/api/dictionary/words/${w1.id}/listened`)
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
    });

    it("returns 404 for non-existent word", async () => {
      const res = await request(app)
        .post("/api/dictionary/words/non-existent/listened")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(404);
    });
  });

  describe("POST /api/dictionary/words", () => {
    it("creates a user-contributed word", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "gelato", translation: "ice cream" });
      expect(res.status).toBe(201);
      expect(res.body.word).toBe("gelato");
      expect(res.body.language).toBe("it");
      expect(res.body.source).toBe("user");
    });

    it("rejects duplicate word+language", async () => {
      await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "pasta", translation: "pasta" });
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "pasta", translation: "noodles" });
      expect(res.status).toBe(409);
      expect(res.body.existingWordId).toBeDefined();
    });

    it("rejects empty word", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "   ", translation: "test" });
      expect(res.status).toBe(400);
    });

    it("rejects word over 100 characters", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "a".repeat(101), translation: "test" });
      expect(res.status).toBe(400);
    });

    it("rejects invalid difficulty", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "pronto", translation: "ready", difficulty: "expert" });
      expect(res.status).toBe(400);
    });

    it("rejects invalid category ID", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "pronto", translation: "ready", categoryId: "nonexistent" });
      expect(res.status).toBe(400);
    });

    it("rejects unauthenticated request", async () => {
      const res = await request(app)
        .post("/api/dictionary/words")
        .send({ word: "pronto", translation: "ready" });
      expect(res.status).toBe(401);
    });

    it("assigns to uncategorised when no category given", async () => {
      await request(app)
        .post("/api/dictionary/words")
        .set("Authorization", `Bearer ${token}`)
        .send({ word: "panino", translation: "sandwich" });
      const cat = await prisma.category.findUnique({ where: { id: "uncategorised" } });
      expect(cat).toBeDefined();
      expect(cat!.nameEn).toBe("Uncategorised");
    });
  });
});
