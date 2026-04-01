#!/usr/bin/env node
/**
 * Generate AI portrait images for host personas.
 *
 * Providers (tried in order):
 *   1. Google Gemini     — requires GOOGLE_API_KEY, returns PNG (converted to JPEG via sharp)
 *   2. Pollinations.ai  — fast, returns JPEG directly, free anonymous tier
 *   3. AI Horde          — crowdsourced, returns webp (converted to JPEG via sharp), free anonymous tier
 *
 * Usage:
 *   node scripts/generate-host-images.mjs                  # all hosts, 3 variants each
 *   node scripts/generate-host-images.mjs --host marco     # single host
 *   node scripts/generate-host-images.mjs --provider gemini # force Gemini only
 *   node scripts/generate-host-images.mjs --provider horde # force AI Horde only
 *   node scripts/generate-host-images.mjs --variants 2     # override variant count
 *   node scripts/generate-host-images.mjs --force          # overwrite existing files
 */

import { writeFile, mkdir, access } from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import sharp from "sharp";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(__dirname, "..", "src", "backend", "public", "hosts");

// ── CLI flags ──
function flag(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 ? process.argv[i + 1] : null;
}
const onlyHost = flag("host");
const variantCount = flag("variants") ? parseInt(flag("variants"), 10) : 3;
const forceProvider = flag("provider"); // "gemini" | "pollinations" | "horde" | null (auto)
const forceOverwrite = process.argv.includes("--force");

// ── Style suffix applied to every prompt ──
const STYLE =
  "warm soft studio lighting, 512x512 portrait, realistic, high quality, shallow depth-of-field, photographic";

// ── Per-host prompts — derived from FRD backstory + physical features ──
const hosts = [
  // ── Italian ──
  {
    id: "marco",
    variants: [
      `Warm close-up portrait of Marco Ferretti, a 44-year-old Italian chef. Stocky, broad-shouldered, olive skin, thick dark brown slightly wavy hair with grey at the temples. Deep brown eyes, pronounced laugh lines, strong Roman nose, full dark beard with a touch of grey. Wearing a white chef coat, warm kitchen background with copper pots. Wide infectious smile. ${STYLE}`,
      `Half-body portrait of Marco Ferretti, 44-year-old Italian chef, standing in a rustic Roman trattoria. Stocky build, olive skin, wavy dark brown hair greying at temples, full dark beard. Holding a wooden spoon, wearing a white chef coat dusted with flour. Warm ambient lighting. ${STYLE}`,
      `Candid portrait of Marco Ferretti, 44, Italian chef laughing mid-conversation. Olive skin, thick wavy dark brown hair with grey temples, dark beard. Seated at a restaurant table with a glass of red wine, relaxed posture, infectious smile. ${STYLE}`,
    ],
  },
  {
    id: "giulia",
    variants: [
      `Close-up portrait of Giulia Marchetti, 36-year-old Italian female professor. Tall, slender, fair olive skin. Straight dark brown nearly black hair in a neat low bun. Sharp hazel-green eyes behind rectangular tortoiseshell glasses. High cheekbones, narrow nose, composed thoughtful expression. Wearing a smart navy blazer. University library background with old books. ${STYLE}`,
      `Half-body portrait of Giulia Marchetti, 36, an Italian linguistics professor. Fair olive skin, dark hair falling past her shoulders, tortoiseshell glasses. Standing in a Florentine chapel, gesturing elegantly at a fresco. Smart blazer, silk scarf. ${STYLE}`,
      `Candid portrait of Giulia Marchetti, 36, Italian professor smiling warmly during a lecture. Dark hair in a low bun, tortoiseshell glasses, hazel-green eyes. Standing at a podium with notes, university hall background. ${STYLE}`,
    ],
  },
  {
    id: "luca",
    variants: [
      `Close-up portrait of Luca Bianchi, a 22-year-old Italian male music student. Lean, athletic, light olive skin. Curly dark brown tousled medium-length hair, bright dark brown eyes, thick eyebrows. Clean-shaven, youthful face. Small silver hoop earring in left ear. Wearing a vintage band t-shirt. Modern urban Milan background. ${STYLE}`,
      `Half-body portrait of Luca Bianchi, 22, Italian student busking with an acoustic guitar in a piazza. Curly dark brown hair, silver hoop earring, oversized hoodie. Piazza del Duomo Milan in soft-focus background. Energetic expression. ${STYLE}`,
      `Candid portrait of Luca Bianchi, 22, Italian music student sitting in a recording studio with headphones around his neck. Curly dark hair, silver earring, casual vintage t-shirt. Warm studio lighting, mixing board behind him. ${STYLE}`,
    ],
  },
  {
    id: "sofia",
    variants: [
      `Close-up portrait of Sofia Esposito, a 72-year-old Italian grandmother. Petite, warm deeply tanned Mediterranean skin with fine wrinkles. Silver-white thick wavy hair in a loose bun. Soft brown eyes, small round gold-rimmed spectacles. Rosy cheeks, gentle grandmotherly face. Small gold cross necklace. Traditional Neapolitan home background. ${STYLE}`,
      `Half-body portrait of Sofia Esposito, 72, Italian nonna in her kitchen. Silver-white hair pinned with a decorative comb, gold-rimmed spectacles, patterned apron over a simple dress. Rolling pasta dough at a wooden table. Warm Neapolitan kitchen with tiled walls. ${STYLE}`,
      `Candid portrait of Sofia Esposito, 72, Italian grandmother sitting in a sunlit courtyard. Silver-white wavy hair, gold spectacles, gold cross necklace. Holding a cup of espresso, smiling serenely. Potted lemon trees in background. ${STYLE}`,
    ],
  },

  // ── Danish ──
  {
    id: "anders",
    variants: [
      `Close-up portrait of Anders Kjeldsen, 31-year-old Danish male barista. Medium build, fair Scandinavian skin with light freckles across the nose. Short sandy-blond hair, neatly trimmed sides, slightly longer on top. Blue-grey eyes, short well-kept blond beard. Friendly relaxed half-smile. Wearing a dark apron over a simple crewneck jumper. Coffee shop background. ${STYLE}`,
      `Half-body portrait of Anders Kjeldsen, 31, Danish barista behind a coffee bar. Sandy-blond hair, blond beard, dark apron, sleeves pushed up. Pouring a latte art, Copenhagen café interior with exposed brick. ${STYLE}`,
      `Candid portrait of Anders Kjeldsen, 31, Danish barista sitting at a café window. Sandy-blond hair, blond beard, blue-grey eyes. Holding a ceramic coffee cup, rainy Copenhagen street visible through the window. ${STYLE}`,
    ],
  },
  {
    id: "freja",
    variants: [
      `Close-up portrait of Freja Holm, 38-year-old Danish female librarian. Tall, slender, pale clear Scandinavian skin. Straight auburn-red shoulder-length hair tucked behind one ear. Bright blue eyes behind round thin-framed silver glasses. Light freckles, narrow face, delicate features, calm intelligent expression. Wearing a cosy knit cardigan over a button-up blouse. Library background with bookshelves. ${STYLE}`,
      `Half-body portrait of Freja Holm, 38, Danish librarian reading aloud to a group. Auburn-red hair held with a simple clip, silver glasses, knit cardigan. Seated in a modern Scandinavian library, warm lamp behind her. ${STYLE}`,
      `Candid portrait of Freja Holm, 38, Danish librarian browsing a bookshelf. Auburn-red hair, silver glasses, blue eyes. Fingers touching book spines, soft library lighting. ${STYLE}`,
    ],
  },
  {
    id: "mikkel",
    variants: [
      `Close-up portrait of Mikkel Sørensen, 24-year-old Danish male design student. Tall, lean, fair skin. Thick straight straw-blond hair swept to one side. Light green eyes, clean-shaven, sharp jawline. Wearing a plain white t-shirt. Modern Scandinavian design studio background. ${STYLE}`,
      `Half-body portrait of Mikkel Sørensen, 24, Danish student leaning on a bicycle in an Odense street. Straw-blond hair, light green eyes, structured jacket over slim trousers. Colourful Danish buildings in background. ${STYLE}`,
      `Candid portrait of Mikkel Sørensen, 24, Danish design student sketching at a desk. Straw-blond hair, light green eyes, small bicycle-gear tattoo visible on left forearm. Design models and mood boards on the wall behind. ${STYLE}`,
    ],
  },
  {
    id: "ingrid",
    variants: [
      `Close-up portrait of Ingrid Nielsen, 69-year-old Danish grandmother. Short, sturdy, fair softly wrinkled skin with pink cheeks. Thick silver hair in a short neat bob. Warm pale blue eyes with crow's feet. Round kindly face. Reading glasses on a beaded chain around her neck. Wearing a hand-knitted wool cardigan with a traditional Nordic pattern. Cosy Danish farmhouse kitchen. ${STYLE}`,
      `Half-body portrait of Ingrid Nielsen, 69, Danish farmor in her garden. Silver bob hair, reading glasses hanging on chain, Nordic-pattern cardigan. Tending vegetable beds, Jutland countryside in background. ${STYLE}`,
      `Candid portrait of Ingrid Nielsen, 69, Danish grandmother pouring coffee from a ceramic pot. Silver bob hair, pale blue eyes, pink cheeks. Seated at a farmhouse kitchen table with a plate of Danish pastries. ${STYLE}`,
    ],
  },

  // ── English ──
  {
    id: "james",
    variants: [
      `Close-up portrait of James Whitfield, 47-year-old English male tour guide. Tall, light skin with ruddy complexion. Short neatly combed dark hair greying at the sides, distinguished receding hairline. Warm brown eyes, confident welcoming smile. Clean-shaven, strong chin, slightly crooked nose. Wearing a smart tweed jacket over an open-collared shirt. London landmark soft-focus background. ${STYLE}`,
      `Half-body portrait of James Whitfield, 47, London tour guide gesturing animatedly in front of the Tower of London. Dark-grey hair, tweed jacket, open-collar shirt. Theatrical posture, warm brown eyes. ${STYLE}`,
      `Candid portrait of James Whitfield, 47, English tour guide in a traditional London pub. Dark hair greying at sides, tweed jacket, pint of ale in hand. Warm pub lighting, wood-panelled walls. Charming grin. ${STYLE}`,
    ],
  },
  {
    id: "emma",
    variants: [
      `Close-up portrait of Emma Ashworth, 41-year-old English female professor. Medium height, slim, fair English-rose complexion. Wavy dark blonde hair in a loose braid. Sharp grey-blue eyes behind elegant oval tortoiseshell glasses. Fine features, straight nose, composed expression with an amused grin. Wearing a crisp white shirt and dark cardigan. Oxford university study background. ${STYLE}`,
      `Half-body portrait of Emma Ashworth, 41, Oxford professor lecturing in a panelled hall. Dark blonde hair in a low ponytail, tortoiseshell glasses, silk scarf over a cardigan. Gesturing at a blackboard with phonetic symbols. ${STYLE}`,
      `Candid portrait of Emma Ashworth, 41, English professor reading in an Oxford garden. Wavy dark blonde hair loose, tortoiseshell glasses pushed up on her head. Seated on a stone bench with an open book, autumn leaves. ${STYLE}`,
    ],
  },
  {
    id: "ryan",
    variants: [
      `Close-up portrait of Ryan Mitchell, 26-year-old Australian male surfer. Athletic broad-shouldered build, deeply sun-tanned skin with visible tan lines. Shaggy sun-bleached sandy brown hair falling across forehead. Bright hazel-green eyes with a permanent squint. Relaxed easy grin, straight white teeth. Shark-tooth pendant necklace, faded friendship bracelet. Wearing a faded surf t-shirt. Beach background. ${STYLE}`,
      `Half-body portrait of Ryan Mitchell, 26, Australian surfer carrying a surfboard on a Byron Bay beach at golden hour. Sun-bleached shaggy hair, tanned skin, board shorts, shark-tooth necklace. Ocean and waves behind. ${STYLE}`,
      `Candid portrait of Ryan Mitchell, 26, Australian surfer filming a video with a phone on a tripod. Sandy bleached hair, hazel-green eyes, shark-tooth necklace. Casual wetsuit top, sunny beach setting. ${STYLE}`,
    ],
  },
  {
    id: "margaret",
    variants: [
      `Close-up portrait of Margaret Campbell, 68-year-old Scottish grandmother. Short, stout, soft fair skin with rosy cheeks and fine smile lines. Thick curly silver-white short hair. Kind deep-set blue eyes behind small half-moon reading glasses. Round warm face with dimples. Wearing a Shetland wool shawl and a tartan skirt. Cosy Highland cottage background. ${STYLE}`,
      `Half-body portrait of Margaret Campbell, 68, Scottish grandmother in a village hall. Curly silver-white hair, half-moon glasses, wool shawl. Standing at a lectern, warm smile, Scottish landscape painting on the wall behind. ${STYLE}`,
      `Candid portrait of Margaret Campbell, 68, Scottish grandmother by a fireplace. Curly silver hair, half-moon glasses, dimpled cheeks. Holding a cup of tea, tartan blanket draped over armchair. Warm fire glow. ${STYLE}`,
    ],
  },
];

// ═══════════════════════════════════════════════════════════
//  Provider 0 — Google Gemini (requires GOOGLE_API_KEY)
// ═══════════════════════════════════════════════════════════

const GEMINI_API_KEY = process.env.GOOGLE_API_KEY || "";
const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash-image";

async function geminiGenerate(prompt, _seed) {
  if (!GEMINI_API_KEY) throw Object.assign(new Error("GOOGLE_API_KEY not set"), { retryable: false });

  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseModalities: ["IMAGE"],
        imageConfig: { aspectRatio: "1:1" },
      },
    }),
    signal: AbortSignal.timeout(120_000),
  });

  if (res.status === 429) throw Object.assign(new Error("Gemini rate-limited"), { retryable: true });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw Object.assign(new Error(`Gemini HTTP ${res.status}: ${body.slice(0, 200)}`), { retryable: res.status >= 500 });
  }

  const data = await res.json();
  const parts = data?.candidates?.[0]?.content?.parts;
  if (!parts?.length) throw new Error("Gemini returned no content parts");

  const imagePart = parts.find((p) => p.inlineData?.mimeType?.startsWith("image/"));
  if (!imagePart) throw new Error("Gemini response contained no image");

  const rawBuf = Buffer.from(imagePart.inlineData.data, "base64");

  // Convert to JPEG via sharp (Gemini returns PNG)
  const jpegBuf = await sharp(rawBuf).jpeg({ quality: 90 }).toBuffer();
  return jpegBuf;
}

// ═══════════════════════════════════════════════════════════
//  Provider 1 — Pollinations.ai
// ═══════════════════════════════════════════════════════════

async function pollinationsGenerate(prompt, seed) {
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=512&nologo=true&nofeed=true&seed=${seed}`;
  const res = await fetch(url, { signal: AbortSignal.timeout(180_000) });
  if (res.status === 429) throw Object.assign(new Error("rate-limited"), { retryable: true });
  if (!res.ok) throw Object.assign(new Error(`HTTP ${res.status}`), { retryable: res.status >= 500 });
  const ct = res.headers.get("content-type") || "";
  if (!ct.startsWith("image/")) throw new Error(`Not image: ${ct}`);
  return Buffer.from(await res.arrayBuffer());
}

// ═══════════════════════════════════════════════════════════
//  Provider 2 — AI Horde  (https://stablehorde.net)
// ═══════════════════════════════════════════════════════════

const HORDE_API = "https://stablehorde.net/api/v2";
const HORDE_KEY = "0000000000"; // anonymous

async function hordeGenerate(prompt, seed) {
  // 1. Submit async job — use photorealistic models with good worker availability
  const submitRes = await fetch(`${HORDE_API}/generate/async`, {
    method: "POST",
    headers: { "Content-Type": "application/json", apikey: HORDE_KEY },
    body: JSON.stringify({
      prompt,
      nsfw: false,
      params: { width: 512, height: 512, steps: 25, seed: String(seed) },
      models: [
        "ICBINP - I Can't Believe It's Not Photography",
        "Deliberate",
        "AbsoluteReality",
        "Realistic Vision",
        "Photon",
      ],
      r2: true,
    }),
    signal: AbortSignal.timeout(30_000),
  });
  if (!submitRes.ok) {
    const body = await submitRes.text();
    throw new Error(`Horde submit ${submitRes.status}: ${body.slice(0, 200)}`);
  }
  const { id: jobId } = await submitRes.json();
  console.log(`    Horde job ${jobId} submitted — polling...`);

  // 2. Poll until done (max ~10 min)
  const maxPolls = 60;
  const pollInterval = 10_000;
  for (let i = 0; i < maxPolls; i++) {
    await new Promise((r) => setTimeout(r, pollInterval));
    const checkRes = await fetch(`${HORDE_API}/generate/check/${jobId}`, {
      signal: AbortSignal.timeout(10_000),
    });
    if (!checkRes.ok) continue;
    const status = await checkRes.json();
    if (status.faulted) throw new Error("Horde job faulted");
    if (status.done) break;
    if (i % 6 === 5) {
      console.log(`    Still waiting... pos=${status.queue_position}, eta=${status.wait_time}s`);
    }
    if (i === maxPolls - 1) throw new Error("Horde poll timeout");
  }

  // 3. Fetch result
  const resultRes = await fetch(`${HORDE_API}/generate/status/${jobId}`, {
    signal: AbortSignal.timeout(15_000),
  });
  if (!resultRes.ok) throw new Error(`Horde status ${resultRes.status}`);
  const result = await resultRes.json();

  if (!result.generations?.length) throw new Error("Horde returned no generations");
  const gen = result.generations[0];
  if (gen.censored) throw new Error("Horde censored this prompt");

  // 4. Download image from R2 URL
  const imgRes = await fetch(gen.img, { signal: AbortSignal.timeout(30_000) });
  if (!imgRes.ok) throw new Error(`Horde image download: ${imgRes.status}`);
  const rawBuf = Buffer.from(await imgRes.arrayBuffer());

  // 5. Convert to JPEG via sharp
  const jpegBuf = await sharp(rawBuf).jpeg({ quality: 90 }).toBuffer();
  return jpegBuf;
}

// ═══════════════════════════════════════════════════════════
//  Orchestration
// ═══════════════════════════════════════════════════════════

async function exists(p) {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

function validateImage(buf) {
  if (buf.length < 5_000) throw new Error(`Image too small: ${buf.length} bytes`);
  const isJpeg = buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff;
  const isPng = buf[0] === 0x89 && buf[1] === 0x50;
  const isWebp = buf[0] === 0x52 && buf[1] === 0x49; // RIFF
  if (!isJpeg && !isPng && !isWebp) throw new Error("Unrecognised image format");
}

async function generateWithFallback(label, prompt, seed) {
  const providers =
    forceProvider === "gemini"
      ? [{ name: "Google Gemini", fn: geminiGenerate }]
      : forceProvider === "horde"
      ? [{ name: "AI Horde", fn: hordeGenerate }]
      : forceProvider === "pollinations"
        ? [{ name: "Pollinations", fn: pollinationsGenerate }]
        : [
            ...(GEMINI_API_KEY ? [{ name: "Google Gemini", fn: geminiGenerate }] : []),
            { name: "Pollinations", fn: pollinationsGenerate },
            { name: "AI Horde", fn: hordeGenerate },
          ];

  for (const { name, fn } of providers) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        console.log(`  [${label}] ${name} (attempt ${attempt}/3)...`);
        const buf = await fn(prompt, seed);
        validateImage(buf);

        // Ensure output is JPEG
        const jpegBuf =
          buf[0] === 0xff && buf[1] === 0xd8
            ? buf
            : await sharp(buf).jpeg({ quality: 90 }).toBuffer();

        return jpegBuf;
      } catch (err) {
        console.log(`  [${label}] ${name} failed: ${err.message}`);
        if (err.retryable === false) {
          break;
        }
        if (attempt < 3 && err.retryable !== false) {
          const wait = attempt * 15;
          console.log(`  Waiting ${wait}s before retry...`);
          await new Promise((r) => setTimeout(r, wait * 1000));
        }
      }
    }
    console.log(`  [${label}] ${name} exhausted — trying next provider...`);
  }
  throw new Error(`All providers failed for ${label}`);
}

async function main() {
  await mkdir(OUTPUT_DIR, { recursive: true });
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Variants per host: ${variantCount}`);
  console.log(
    `Provider: ${
      forceProvider ||
      (GEMINI_API_KEY
        ? `auto (Google Gemini → Pollinations → AI Horde; model ${GEMINI_MODEL})`
        : "auto (Pollinations → AI Horde)")
    }`
  );
  console.log(`Overwrite: ${forceOverwrite}\n`);

  const filtered = onlyHost ? hosts.filter((h) => h.id === onlyHost) : hosts;

  if (filtered.length === 0) {
    console.error(
      `Host "${onlyHost}" not found. Available: ${hosts.map((h) => h.id).join(", ")}`
    );
    process.exit(1);
  }

  let generated = 0;
  let skipped = 0;
  let failed = 0;

  for (const host of filtered) {
    const count = Math.min(variantCount, host.variants.length);
    for (let i = 0; i < count; i++) {
      const label = `${host.id}-${i + 1}`;
      const outPath = path.join(OUTPUT_DIR, `${label}.jpg`);

      if (!forceOverwrite && (await exists(outPath))) {
        console.log(`  [${label}] exists — skipping`);
        skipped++;
        continue;
      }

      try {
        const seed = 42 + i;
        const buf = await generateWithFallback(label, host.variants[i], seed);
        await writeFile(outPath, buf);
        console.log(`  [${label}] Saved (${buf.length} bytes)`);
        generated++;
      } catch (err) {
        console.error(`  [${label}] FAILED: ${err.message}`);
        failed++;
      }

      // Brief pause between jobs to be polite to APIs
      if (!forceProvider || forceProvider === "pollinations" || forceProvider === "gemini") {
        await new Promise((r) => setTimeout(r, 5_000));
      }
    }
  }

  console.log(`\nDone! Generated: ${generated}, Skipped: ${skipped}, Failed: ${failed}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
