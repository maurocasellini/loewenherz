#!/usr/bin/env python3
"""Erzeugt die KI-Stimme der App: für jeden Satz aus phrases.json eine MP3 in www/voice/.

Motor:
  - OPENAI_API_KEY gesetzt  -> OpenAI-Sprachausgabe (sehr natürlich)
  - sonst                   -> Piper (frei, läuft lokal), Modell in PIPER_MODEL

Schon vorhandene Sätze werden nicht neu erzeugt (spart Zeit und Kosten).
Wechselt der Motor oder die Stimme, wird alles neu erzeugt.
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request

PHRASES = sys.argv[1] if len(sys.argv) > 1 else "phrases.json"
OUT = "www/voice"
KEY = os.environ.get("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_VOICE = os.environ.get("OPENAI_TTS_VOICE", "coral")
STYLE = os.environ.get("TTS_STYLE", (
    "Sprich Hochdeutsch mit leichter Schweizer Färbung, warm, fröhlich und ermutigend, "
    "wie eine liebevolle Erzählerin für ein sechsjähriges Kind. Eher langsam und sehr deutlich. "
    "Einzelne Silben oder Laute klar und kurz aussprechen."))
PIPER_MODEL = os.environ.get("PIPER_MODEL", "")
PRON_VERSION = "p4"  # hochzählen, wenn sich die Aussprache-Regeln ändern

engine = (f"openai:{OPENAI_MODEL}:{OPENAI_VOICE}" if KEY else "piper:" + os.environ.get("PIPER_NAME", os.path.basename(PIPER_MODEL))) + ":" + PRON_VERSION
if not KEY and not PIPER_MODEL:
    sys.exit("Weder OPENAI_API_KEY noch PIPER_MODEL gesetzt.")


# Aussprache-Regeln. Wörter ohne Vokal (SCH, Sss, Psst) buchstabiert Piper sonst ("Es-Ze-Ha").
# Piper bekommt die Laute als Lautschrift [[ ... ]], OpenAI eine natürliche Schreibweise.
PRON = [  # (Muster, Piper, OpenAI)
    (r"\b[Ss][Cc][Hh]+\b", "[[ ʃʃʃʃ ]]", "Schhhh"),
    (r"(?<!['’])\b[Ss]+\b", "[[ ssss ]]", "Ssss"),
    (r"\bPs+t\b", "[[ pst ]]", "Psst"),
    (r"\bHmm+\b", "[[ hmː ]]", "Hmm"),
]


def speakable(t):
    for pat, piper_ph, natural in PRON:
        t = re.sub(pat, natural if KEY else piper_ph, t)
    # GROSSBUCHSTABEN-Wörter normal schreiben, sonst buchstabieren manche Stimmen sie.
    t = re.sub(r"\b([A-ZÄÖÜ])([A-ZÄÖÜß]+)\b", lambda m: m.group(1) + m.group(2).lower(), t)
    return t


def tts_openai(text, mp3):
    body = json.dumps({"model": OPENAI_MODEL, "voice": OPENAI_VOICE, "input": text,
                       "instructions": STYLE, "response_format": "mp3"}).encode()
    for attempt in range(5):
        req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=body, headers={
            "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read()
            break
        except Exception as e:  # Rate-Limit o.ä.: kurz warten, nochmal
            if attempt == 4:
                raise
            time.sleep(2 ** attempt * 2)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(raw)
    to_mp3(f.name, mp3)
    os.unlink(f.name)


_piper = None


def tts_piper(text, mp3):
    global _piper
    import wave
    from piper import PiperVoice, SynthesisConfig
    if _piper is None:
        _piper = PiperVoice.load(PIPER_MODEL)  # Modell nur einmal laden
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav = f.name
    with wave.open(wav, "wb") as wf:
        _piper.synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=1.12))
    to_mp3(wav, mp3, stretch=is_pure_sound(text))
    os.unlink(wav)


def is_pure_sound(t):
    """Nur Laute ohne echte Wörter, z.B. "Schhhh!" -> wird zum Nachmachen länger gezogen."""
    return "[[" in t and not re.search(r"[A-Za-zÄÖÜäöüß]", re.sub(r"\[\[.*?\]\]", "", t))


TRIM = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
        "silenceremove=start_periods=1:start_threshold=-50dB,areverse")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip() or 0)


def to_mp3(src, mp3, stretch=False):
    # Mono, Stille am Anfang/Ende weg, Lautstärke angleichen, klein halten.
    # Reine Laute ("Schhhh!") werden auf ~1,2 s gezogen, damit das Kind mitmachen kann.
    chain = TRIM
    if stretch:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            trimmed = f.name
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", TRIM, trimmed], check=True)
        d, factor = duration(trimmed), 1.0
        os.unlink(trimmed)
        tempos = []
        if d > 0:
            factor = max(d / 1.2, 0.08)
            while factor < 0.5:
                tempos.append("atempo=0.5"); factor /= 0.5
            if factor < 1:
                tempos.append(f"atempo={factor:.3f}")
        if tempos:
            chain += "," + ",".join(tempos)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", chain + ",loudnorm=I=-16:TP=-1.5",
                    "-ac", "1", "-ar", "24000", "-b:a", "48k", mp3], check=True)


phrases = json.load(open(PHRASES))
os.makedirs(OUT, exist_ok=True)
idx_path = os.path.join(OUT, "index.json")
old = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
keep = old.get("texts", {}) if old.get("engine") == engine else {}

texts, made = {}, 0
for i, p in enumerate(phrases):
    h, t = p["h"], p["t"]
    mp3 = os.path.join(OUT, h + ".mp3")
    texts[h] = t
    if keep.get(h) == t and os.path.exists(mp3):
        continue
    (tts_openai if KEY else tts_piper)(speakable(t), mp3)
    made += 1
    if made % 25 == 0:
        print(f"  {made} neu … ({i + 1}/{len(phrases)})", flush=True)

for f in os.listdir(OUT):  # alte Sätze aufräumen
    if f.endswith(".mp3") and f[:-4] not in texts:
        os.unlink(os.path.join(OUT, f))

json.dump({"engine": engine, "files": sorted(texts), "texts": texts}, open(idx_path, "w"), ensure_ascii=False, indent=0)
size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print(f"Fertig: {len(texts)} Sätze, {made} neu erzeugt, {size / 1e6:.1f} MB, Motor {engine}")
