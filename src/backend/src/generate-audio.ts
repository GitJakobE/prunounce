import { PrismaClient } from "@prisma/client";
import { getAudioPath } from "./services/tts.js";

const prisma = new PrismaClient();

async function generateAllAudio() {
  const words = await prisma.word.findMany({
    orderBy: { word: "asc" },
  });

  console.log(`Found ${words.length} words. Generating word audio...\n`);

  let success = 0;
  let failed = 0;

  for (const word of words) {
    process.stdout.write(`  ${word.word}... `);
    try {
      const audioPath = await getAudioPath(word.word);
      if (audioPath) {
        console.log("OK");
        success++;
      } else {
        console.log("FAILED");
        failed++;
      }
    } catch {
      console.log("ERROR");
      failed++;
    }
    await new Promise((r) => setTimeout(r, 300));
  }

  console.log(`\nWords: ${success} generated, ${failed} failed.\n`);

  // Generate example sentence audio
  const wordsWithExamples = words.filter((w) => w.exampleIt);
  console.log(
    `Generating ${wordsWithExamples.length} example sentence audio files...\n`
  );

  let exSuccess = 0;
  let exFailed = 0;

  for (const word of wordsWithExamples) {
    process.stdout.write(`  ex: ${word.word}... `);
    try {
      const audioPath = await getAudioPath(
        `ex_${word.word}`,
        word.exampleIt
      );
      if (audioPath) {
        console.log("OK");
        exSuccess++;
      } else {
        console.log("FAILED");
        exFailed++;
      }
    } catch {
      console.log("ERROR");
      exFailed++;
    }
    await new Promise((r) => setTimeout(r, 300));
  }

  console.log(`\nExamples: ${exSuccess} generated, ${exFailed} failed.`);
  console.log(`\nTotal: ${success + exSuccess} audio files.`);
  await prisma.$disconnect();
}

generateAllAudio().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
