import { copyFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

try {
  await mkdir(OUTPUT_DIR, { recursive: true });
  await copyFile(join(BOT_DIR, "POST.json"), join(OUTPUT_DIR, "POST.json"));
} catch (err) {
  console.error(`main.ts failed: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
}
