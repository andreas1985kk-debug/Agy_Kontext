# Agy_Kontext – Zero‑Token Context‑Watchdog Plugin

Dieses Plugin nutzt die Antigravity‑Hook‑Mechanik, um nach jedem KI‑Antwort‑Turn
eine flüchtige Systemnachricht (Ephemeral Message) anzuzeigen, die den aktuellen
Token‑Verbrauch des Chats visualisiert – **vollständig tokenfrei**.

## Installation

1. Repository klonen oder als Submodule in dein Projekt einbinden
   ```bash
   git clone https://github.com/andreas1985kk-debug/Agy_Kontext.git
   ```
2. Den Hook global in `~/.gemini/config/hooks.json` eintragen:
   ```json
   {
     "hooks": {
       "Stop": [
         {
           "matcher": ".*",
           "hooks": [
             {
               "type": "command",
               "command": "python \"C:/Pfad/zum/Plugin/scripts/context_hook.py\""
             }
           ]
         }
       ]
     }
   }
   ```
3. Antigravity neu starten – der Hook wird automatisch nach jeder Antwort ausgeführt.

## Funktionsweise

- **Hook‑Event**: `Stop` – wird nach jedem KI‑Output ausgelöst (Claude Code / Antigravity).
- **Skript**: `scripts/context_hook.py`
  - Empfängt via `stdin` ein JSON mit dem Feld `transcriptPath`.
  - Liest das aktuelle `transcript.jsonl` des Chats direkt von der Festplatte.
  - Schätzt die Token‑Anzahl (≈ 3,6 Zeichen pro Token).
  - Gibt eine Ephemeral Message aus, z. B.:
    `**Kontext‑Wächter:** 🟢 OK | 28.2k / 1000k Tokens (3%) genutzt.`
  - Falls kein Transkript vorhanden: `⚪ NO TRANSCRIPT | 0k / 1000k Tokens (0%) genutzt.`

## Statusanzeige

| Symbol | Bedeutung | Schwellenwert |
|--------|-----------|---------------|
| 🟢 OK | Kontext unkritisch | < 400 k Tokens |
| 🟡 WARNUNG | Kontext füllt sich | ≥ 400 k Tokens |
| 🔴 KRITISCH | Kontext fast voll | ≥ 750 k Tokens |
| ⚪ NO TRANSCRIPT | Kein Transkript gefunden | – |

## Token‑Kosten

Das Plugin ist **vollständig tokenfrei**:

- Das Skript läuft als externer OS‑Prozess – kein Modell beteiligt.
- Die Ausgabe erfolgt als `ephemeralMessage` – sie wird nur im UI angezeigt,
  **nicht** in den Kontext‑Verlauf geschrieben.

## Debug

Das Skript schreibt ein optionales Debug‑Log nach:
```
C:\AI_Engineering\.agents\plugins\context_watchdog\hook_debug.log
```

## Lizenz

Apache 2.0 – frei nutzbar, Änderungen erlaubt, Attribution erforderlich.

---

*Bei Fragen oder Problemen: Öffne ein Issue im Repository oder kontaktiere den Maintainer.*
