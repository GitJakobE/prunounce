import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import app from "../app";

async function registerAndGetToken() {
  const res = await request(app).post("/api/auth/register").send({
    email: "profile@example.com",
    password: "Password1",
    language: "en",
    displayName: "Profile User",
  });
  return res.body.token as string;
}

describe("Profile Routes", () => {
  let token: string;

  beforeEach(async () => {
    token = await registerAndGetToken();
  });

  describe("GET /api/profile", () => {
    it("returns user profile with progress", async () => {
      const res = await request(app)
        .get("/api/profile")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.user.email).toBe("profile@example.com");
      expect(res.body.user.displayName).toBe("Profile User");
      expect(res.body.progress).toBeDefined();
      expect(res.body.progress.totalWords).toBeGreaterThanOrEqual(0);
      expect(res.body.progress.listenedWords).toBe(0);
    });

    it("rejects unauthenticated request", async () => {
      const res = await request(app).get("/api/profile");
      expect(res.status).toBe(401);
    });
  });

  describe("PATCH /api/profile", () => {
    it("updates display name", async () => {
      const res = await request(app)
        .patch("/api/profile")
        .set("Authorization", `Bearer ${token}`)
        .send({ displayName: "New Name" });
      expect(res.status).toBe(200);
      expect(res.body.user.displayName).toBe("New Name");
    });

    it("updates language", async () => {
      const res = await request(app)
        .patch("/api/profile")
        .set("Authorization", `Bearer ${token}`)
        .send({ language: "da" });
      expect(res.status).toBe(200);
      expect(res.body.user.language).toBe("da");
    });

    it("rejects invalid language", async () => {
      const res = await request(app)
        .patch("/api/profile")
        .set("Authorization", `Bearer ${token}`)
        .send({ language: "xx" });
      expect(res.status).toBe(400);
    });

    it("rejects empty update", async () => {
      const res = await request(app)
        .patch("/api/profile")
        .set("Authorization", `Bearer ${token}`)
        .send({});
      expect(res.status).toBe(400);
    });
  });

  describe("DELETE /api/profile", () => {
    it("deletes user account (GDPR)", async () => {
      const res = await request(app)
        .delete("/api/profile")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.message).toContain("deleted");

      // Verify user is actually gone
      const check = await request(app)
        .get("/api/profile")
        .set("Authorization", `Bearer ${token}`);
      expect(check.status).toBe(404);
    });
  });
});
