-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "email" TEXT NOT NULL,
    "passwordHash" TEXT,
    "displayName" TEXT,
    "language" TEXT NOT NULL DEFAULT 'en',
    "hostId" TEXT NOT NULL DEFAULT 'marco',
    "googleId" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Category" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "nameEn" TEXT NOT NULL,
    "nameDa" TEXT NOT NULL,
    "nameIt" TEXT NOT NULL DEFAULT '',
    "order" INTEGER NOT NULL DEFAULT 0
);

-- CreateTable
CREATE TABLE "Word" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "word" TEXT NOT NULL,
    "language" TEXT NOT NULL DEFAULT 'it',
    "phoneticHint" TEXT NOT NULL,
    "translationEn" TEXT NOT NULL,
    "translationDa" TEXT NOT NULL,
    "translationIt" TEXT NOT NULL DEFAULT '',
    "difficulty" TEXT NOT NULL,
    "exampleIt" TEXT NOT NULL DEFAULT '',
    "exampleEn" TEXT NOT NULL DEFAULT '',
    "exampleDa" TEXT NOT NULL DEFAULT '',
    "audioPath" TEXT,
    "source" TEXT NOT NULL DEFAULT 'seed',
    "contributedBy" TEXT,
    CONSTRAINT "Word_contributedBy_fkey" FOREIGN KEY ("contributedBy") REFERENCES "User" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "WordCategory" (
    "wordId" TEXT NOT NULL,
    "categoryId" TEXT NOT NULL,

    PRIMARY KEY ("wordId", "categoryId"),
    CONSTRAINT "WordCategory_wordId_fkey" FOREIGN KEY ("wordId") REFERENCES "Word" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "WordCategory_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "UserProgress" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "wordId" TEXT NOT NULL,
    "listenedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "UserProgress_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "UserProgress_wordId_fkey" FOREIGN KEY ("wordId") REFERENCES "Word" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "User_googleId_key" ON "User"("googleId");

-- CreateIndex
CREATE UNIQUE INDEX "Word_word_language_key" ON "Word"("word", "language");

-- CreateIndex
CREATE UNIQUE INDEX "UserProgress_userId_wordId_key" ON "UserProgress"("userId", "wordId");
