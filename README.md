# Löwenherz 🦁

Kinder-App für Mut, Gefühle und Sprechen, mit dem Jump'n'Run **Dschungel-Expedition** (Matteo & Elara).
Läuft komplett offline (Flugmodus), speichert nur auf dem Gerät und braucht kein Konto.

## Was drin ist

- **Dschungel-Expedition:** 6 Level im Mario-Stil mit Matteo oder Elara im Entdecker-Outfit. Laufen, springen, ?-Blöcke, Gegner plattspringen, wackelige Brücke, dunkle Höhle, Schlangen-Tempel, rollende Steinkugel, goldener Löwe. An den **Mut-Toren** muss das Kind etwas laut sagen (übt K, T, S, SCH) oder den Mut-Knopf halten.
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
- Nach Änderungen `VERSION` in `www/sw.js` hochzählen, damit installierte Web-Apps das Update holen.
- Lokal testen: `npm run serve`
