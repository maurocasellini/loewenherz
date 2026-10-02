// Löwenherz – Offline-Speicher. VERSION wird bei neuer KI-Stimme automatisch angepasst.
const VERSION = "loewenherz-774709fa";
const FILES = [
  "./index.html", "./manifest.webmanifest",
  "./icon.svg", "./icon-180.png", "./icon-192.png", "./icon-512.png",
  "./fonts/grandstander.woff2", "./fonts/nunito.woff2"
];

// Alle Sprach-Dateien vorab laden, damit die Stimme auch im Flugmodus da ist.
async function cacheVoice(cache) {
  try {
    const idx = await (await fetch("./voice/index.json", { cache: "no-cache" })).json();
    const files = (idx.files || []).map((h) => `./voice/${h}.mp3`);
    for (let i = 0; i < files.length; i += 40) await cache.addAll(files.slice(i, i + 40));
  } catch (e) { /* ohne Stimm-Dateien spricht die Gerätestimme */ }
}

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then(async (c) => { await c.addAll(FILES); await cacheVoice(c); }).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("loewenherz-") && k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Seite und Satzliste: erst Netz (damit Updates ankommen), sonst Cache. Rest: erst Cache, dann Netz (und merken).
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  const fresh = e.request.mode === "navigate" || url.pathname.endsWith("/voice/index.json");
  if (fresh) {
    const key = e.request.mode === "navigate" ? "./index.html" : e.request;
    e.respondWith(
      fetch(e.request)
        .then((r) => { const copy = r.clone(); if (r.ok) caches.open(VERSION).then((c) => c.put(key, copy)); return r; })
        .catch(() => caches.match(key))
    );
    return;
  }
  e.respondWith(caches.match(e.request).then((hit) => hit || fetch(e.request).then((r) => {
    if (r.ok) { const copy = r.clone(); caches.open(VERSION).then((c) => c.put(e.request, copy)); }
    return r;
  })));
});
