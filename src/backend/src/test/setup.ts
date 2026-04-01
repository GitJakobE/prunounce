import { afterAll, afterEach } from "vitest";
import prisma from "../db";

// Use test database from environment
process.env.DATABASE_URL = "file:./test.db";
process.env.JWT_SECRET = "test-secret-key-for-tests";
process.env.PORT = "0";

afterEach(async () => {
  // Clean all tables between tests
  await prisma.userProgress.deleteMany();
  await prisma.wordCategory.deleteMany();
  await prisma.word.deleteMany();
  await prisma.category.deleteMany();
  await prisma.user.deleteMany();
});

afterAll(async () => {
  await prisma.$disconnect();
});
