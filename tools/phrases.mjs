// Liest alle sprechbaren Sätze aus der App (www/index.html#phrases) und schreibt sie als JSON.
import { chromium } from "playwright";
import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const out = process.argv[2] || "phrases.json";
const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto(pathToFileURL(resolve("www/index.html")).href + "#phrases");
await page.waitForFunction(() => typeof window.__phrases === "function");
const list = await page.evaluate(() => window.__phrases());
await browser.close();
if (errors.length) { console.error("Fehler in der App:", errors); process.exit(1); }
writeFileSync(out, JSON.stringify(list, null, 1));
console.log(`${list.length} Sätze -> ${out}`);
