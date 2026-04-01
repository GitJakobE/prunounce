import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import app from "../app";
import prisma from "../db";
import { _clearStore } from "../middleware/rate-limit";

describe("Auth Routes", () => {
  const validUser = {
    email: "test@example.com",
    password: "Password1",
    language: "en",
    displayName: "Test User",
  };

  beforeEach(() => {
    _clearStore();
  });

  describe("POST /api/auth/register", () => {
    it("creates a new user and returns token", async () => {
      const res = await request(app).post("/api/auth/register").send(validUser);
      expect(res.status).toBe(201);
      expect(res.body.token).toBeDefined();
      expect(res.body.user.email).toBe(validUser.email);
      expect(res.body.user.displayName).toBe(validUser.displayName);
      expect(res.body.user.language).toBe("en");
    });

    it("rejects duplicate email", async () => {
      await request(app).post("/api/auth/register").send(validUser);
      const res = await request(app).post("/api/auth/register").send(validUser);
      expect(res.status).toBe(409);
    });

    it("rejects weak password", async () => {
      const res = await request(app)
        .post("/api/auth/register")
        .send({ ...validUser, password: "weak" });
      expect(res.status).toBe(400);
    });

    it("rejects invalid email", async () => {
      const res = await request(app)
        .post("/api/auth/register")
        .send({ ...validUser, email: "not-an-email" });
      expect(res.status).toBe(400);
    });
  });

  describe("POST /api/auth/login", () => {
    beforeEach(async () => {
      await request(app).post("/api/auth/register").send(validUser);
    });

    it("logs in with correct credentials", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: validUser.password });
      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
      expect(res.body.user.email).toBe(validUser.email);
    });

    it("rejects wrong password", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: "WrongPass1" });
      expect(res.status).toBe(401);
    });

    it("rejects non-existent email", async () => {
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: "nobody@example.com", password: "Password1" });
      expect(res.status).toBe(401);
    });
  });

  describe("GET /api/auth/me", () => {
    it("returns current user from token", async () => {
      const reg = await request(app)
        .post("/api/auth/register")
        .send(validUser);
      const token = reg.body.token;

      const res = await request(app)
        .get("/api/auth/me")
        .set("Authorization", `Bearer ${token}`);
      expect(res.status).toBe(200);
      expect(res.body.user.email).toBe(validUser.email);
    });

    it("rejects request without token", async () => {
      const res = await request(app).get("/api/auth/me");
      expect(res.status).toBe(401);
    });

    it("rejects invalid token", async () => {
      const res = await request(app)
        .get("/api/auth/me")
        .set("Authorization", "Bearer invalid-token");
      expect(res.status).toBe(401);
    });
  });

  describe("Login Rate Limiting", () => {
    beforeEach(async () => {
      await request(app).post("/api/auth/register").send(validUser);
    });

    it("allows login when under the rate limit threshold", async () => {
      // 4 failed attempts should still allow the next attempt
      for (let i = 0; i < 4; i++) {
        await request(app)
          .post("/api/auth/login")
          .send({ email: validUser.email, password: "WrongPass1" });
      }
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: validUser.password });
      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
    });

    it("returns 429 after exceeding the failed attempt threshold", async () => {
      for (let i = 0; i < 5; i++) {
        await request(app)
          .post("/api/auth/login")
          .send({ email: validUser.email, password: "WrongPass1" });
      }
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: validUser.password });
      expect(res.status).toBe(429);
      expect(res.body.error).toBe(
        "Too many login attempts. Please try again in 15 minutes."
      );
    });

    it("error message does not reveal email existence", async () => {
      // Rate-limit a non-existent email
      for (let i = 0; i < 5; i++) {
        await request(app)
          .post("/api/auth/login")
          .send({ email: "nobody@example.com", password: "WrongPass1" });
      }
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: "nobody@example.com", password: "WrongPass1" });
      expect(res.status).toBe(429);
      // Same message regardless of whether the email exists
      expect(res.body.error).toBe(
        "Too many login attempts. Please try again in 15 minutes."
      );
    });

    it("successful login resets the failure counter", async () => {
      // 4 failed attempts
      for (let i = 0; i < 4; i++) {
        await request(app)
          .post("/api/auth/login")
          .send({ email: validUser.email, password: "WrongPass1" });
      }
      // Successful login resets counter
      await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: validUser.password });
      // 5 more failed attempts should be allowed before blocking
      for (let i = 0; i < 5; i++) {
        const res = await request(app)
          .post("/api/auth/login")
          .send({ email: validUser.email, password: "WrongPass1" });
        expect(res.status).toBe(401);
      }
    });

    it("does not affect other email addresses", async () => {
      // Rate-limit one email
      for (let i = 0; i < 5; i++) {
        await request(app)
          .post("/api/auth/login")
          .send({ email: "attacker@example.com", password: "WrongPass1" });
      }
      // Other email should still work
      const res = await request(app)
        .post("/api/auth/login")
        .send({ email: validUser.email, password: validUser.password });
      expect(res.status).toBe(200);
    });
  });
});
