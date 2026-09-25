# Agy_Kontext – Zero‑Token Context‑Watchdog Plugin

Dieses Plugin nutzt die Antigravity‑Hook‑Mechanik, um nach jedem KI‑Antwort‑Turn
eine flüchtige Systemnachricht (Ephemeral Message) anzuzeigen, die den aktuellen
Token‑Verbrauch des Chats visualisiert.

## Installation

1. Repository klonen oder als Submodule in dein Projekt einbinden
   ```bash
   git clone https://github.com/andreas1985kk-debug/Agy_Kontext.git
   ```
2. In die Antigravity‑Konfiguration aufnehmen (z. B. `.agents/plugins.json`)
   ```json
   {
     "plugins": [ "./plugins/context_watchdog" ]
   }
   ```
   (Falls du das Plugin bereits im Projektordner `.agents/plugins` hast, reicht ein
   relativer Pfad zu dem Verzeichnis.)
3. Beim Start von Antigravity wird der Hook automatisch aktiviert.

## Funktionsweise

- **Hook‑Event**: `PostInvocation` – wird nach jedem KI‑Output ausgelöst.
- **Skript**: `scripts/context_hook.py`
  - Liest das aktuelle `transcript.jsonl` des Chats.
  - Schätzt die Token‑Anzahl (≈ 3,6 Zeichen pro Token).
  - Gibt eine Ephemeral Message wie
    `**Kontext‑Wächter:** 🟢 OK | 145.0k / 1000k Tokens (15%) genutzt.` aus.
- **Debug‑Log**: `hook_debug.log` im Plugin‑Ordner (optional, zu Fehlersuche).

## Lizenz

Apache 2.0 – frei nutzbar, Änderungen erlaubt, Attribution erforderlich.

---

*Bei Fragen oder Problemen: Öffne ein Issue im Repository oder kontaktiere den
Maintainer.*
