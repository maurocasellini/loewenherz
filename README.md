# Löwenherz 🦁

Kinder-App für Mut, Gefühle und Sprechen, mit dem Jump'n'Run **Dschungel-Expedition** (Matteo & Elara).
Läuft komplett offline (Flugmodus), speichert nur auf dem Gerät und braucht kein Konto.

## Was drin ist

- **Expedition (Jump'n'Run):** 6 Welten mit 18 Leveln (Dschungel, Eiswelt, Vulkaninsel, Wolkenland, Dino-Tal, Pyramiden-Wüste) plus **Endlos-Abenteuer**: jedes Mal ein neu gebautes Level aus erprobten Bausteinen, mit Mut-Toren aus den Übungswörtern (welche Laute, stellt man in der Eltern-Ecke ein). Matteo oder Elara im Entdecker-Outfit, Steuerung im Gameboy-Stil: **A = springen**, **B = Peitsche** (betäubt Gegner, zerschlägt Kisten und ?-Blöcke, schwingt an goldenen Ringen über Abgründe). In den ?-Blöcken stecken Edelsteine und Power-ups wie bei Mario: 🍄 Pilz (gross, ein Treffer ist frei), 🪶 Feder (Doppelsprung), ⭐ Stern (unbesiegbar). Pro Level gibt es 1–3 Sterne je nach gesammelten Edelsteinen.
- **Mut-Welt:** Mut-Missionen, Löwen-Brüller, Gefühle-Wetter, Erzähl-Würfel, Kraft tanken, Stolz-Glas
- **Sprech-Dschungel:** Laut-Training K/T/S/SCH in 6 Stufen, Ohren-Detektiv (Tasse/Tasche), Zungen-Turnen mit animiertem Löwen
- **Eltern-Ecke** (mit Rechenaufgabe gesperrt): Name, Fortschritt, Tipps

## Aufs Gerät bringen

### Variante A: Web-App (iPhone, iPad, Android)
1. Projekt bei Vercel importieren (Output-Ordner `www`, steht schon in `vercel.json`). Alternativ geht jeder statische Hoster.
2. Auf dem Gerät die Adresse **einmal mit Internet** öffnen.
   - **iPhone/iPad:** Safari → Teilen → «Zum Home-Bildschirm»
   - **Android:** Chrome → ⋮ → «App installieren»
3. Ab dann läuft alles im Flugmodus.

### Variante B: Android-App (APK) für Kinder-Tablets
Bei jedem Push auf `main` baut GitHub automatisch eine APK.
GitHub → **Actions** → letzter Lauf «Android-App bauen» → **Artifacts** → `loewenherz-apk` herunterladen, entpacken, `app-debug.apk` aufs Tablet kopieren und öffnen.
(Einmalig erlauben: «Apps aus unbekannten Quellen installieren».)

## KI-Stimme

Alles, was die App sagt, wird **einmal vorab von einer KI-Stimme gesprochen** und als MP3 in `www/voice/` gelegt. Deshalb funktioniert die Stimme auch im Flugmodus. Das erledigt der Workflow «KI-Stimme erzeugen» automatisch, sobald sich ein Text in der App ändert. Was nicht vorab gesprochen werden kann (z.B. selbst getippte Stolz-Sätze), liest die Gerätestimme.

- **Standard (gratis):** Piper-Stimme «Thorsten» (frei, CC0)
- **Natürlicher:** OpenAI-Stimme. Dafür unter GitHub → Settings → Secrets and variables → Actions ein Secret `OPENAI_API_KEY` anlegen. Optional als Variable `OPENAI_TTS_VOICE` eine andere Stimme setzen (z.B. `coral`, `nova`, `shimmer`, `sage`). Danach den Workflow einmal von Hand starten (Actions → «KI-Stimme erzeugen» → Run workflow). Alle Sätze kosten zusammen nur Rappen.

## Kindermodus

| Gerät | So geht's |
|---|---|
| **iPad/iPhone** | Web-App auf den Home-Bildschirm legen. Mit **Bildschirmzeit** Safari und alles andere begrenzen. Mit **Geführter Zugriff** (Einstellungen → Bedienungshilfen) bleibt das Kind in der App: dreimal die Seitentaste drücken. |
| **Samsung (Samsung Kids)** | APK im Eltern-Profil installieren, dann in Samsung Kids → ⋮ → «Apps hinzufügen» → Löwenherz. |
| **Google Family Link** | Auf betreuten Geräten ist das Installieren von APKs meist gesperrt. Einfacher: Web-App über Chrome installieren (Variante A), Chrome in Family Link erlauben. |
| **Amazon Fire (Kids)** | Im Eltern-Profil die APK installieren und im Eltern-Dashboard dem Kinderprofil freigeben. Falls das nicht klappt: Web-App im Silk-Browser. |
| **Android allgemein** | **Bildschirm fixieren** (Einstellungen → Sicherheit → App-Fixierung): Das Kind kann die App nicht verlassen. |

## Später: App Store / Play Store
Mit dem gleichen Code möglich (Capacitor): Google Play kostet einmalig 25 USD, Apple 99 USD pro Jahr. Für Kinder-Apps verlangen beide eine Datenschutzerklärung. Die App sammelt keine Daten, das macht es einfach.

## Entwickeln
- `www/index.html` ist die ganze App (HTML, CSS, JS in einer Datei).
- Neue Versionen erkennt die App selbst und lädt sich neu (die Versionsnummer in `www/sw.js` setzt der Stimmen-Workflow automatisch).
- Lokal testen: `npm run serve`
