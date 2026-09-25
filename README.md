# Agy_Kontext – Zero‑Token Context‑Watchdog Plugin

Dieses Plugin kombiniert einen Antigravity-Hook mit einem permanenten Desktop-Widget (System Tray), um nach jedem KI-Antwort-Turn den aktuellen Token-Verbrauch des Chats live, minimalistisch und **vollständig tokenfrei** auf Ihrem Bildschirm anzuzeigen.

## Installation & Einrichtung

### 1. Abhängigkeiten installieren
Das Overlay benötigt `pystray` für das System-Tray-Icon und `pillow` für die Bildgenerierung:
```bash
pip install pystray pillow
```

### 2. Repository klonen
```bash
git clone https://github.com/andreas1985kk-debug/Agy_Kontext.git
```

### 3. Den Hook in Antigravity registrieren
Trage den Hook global in `~/.gemini/config/hooks.json` ein:
```json
{
  "context-watchdog": {
    "PostInvocation": [
      {
        "type": "command",
        "command": "python \"C:/Pfad/zum/Plugin/scripts/context_hook.py\""
      }
    ]
  }
}
```

### 4. Das Desktop-Widget starten
Da Antigravity alle Hooks in einer versteckten Hintergrundsitzung ("headless") ausführt, kann das Hook-Skript keine sichtbaren Desktop-Fenster zeichnen. Deshalb starten Sie das kleine Widget **einmalig manuell** im Hintergrund. 

Führen Sie diesen Befehl in der Windows PowerShell aus:
```powershell
Start-Process pythonw -ArgumentList "C:\Pfad\zum\Plugin\scripts\context_hook.py --gui-server" -WindowStyle Hidden
```
*Es taucht sofort ein kleines Tray-Icon (weißer Punkt) neben Ihrer Windows-Uhr auf.*

## Funktionsweise & Features

- **Drag & Drop**: Klicken Sie das Widget an und ziehen Sie es per Maus an eine beliebige Stelle (z. B. direkt über die Taskleiste).
- **Position speichern & Fixieren**: Rechtsklick auf das Tray-Icon unten rechts erlaubt es, die Position zu **fixieren**. Die Koordinaten werden in der `config.json` dauerhaft gespeichert.
- **Topmost & Transparent**: Das Fenster zwingt sich jede Sekunde über die Windows-Taskleiste (`root.lift()`) und hat einen vollständig transparenten Hintergrund.
- **Auto-Update**: Nach jedem KI-Turn sendet der Antigravity-Hook die neu berechnete Token-Zahl an die `state.json`. Das Widget liest diese im Sekundentakt aus und aktualisiert sich sofort, ohne zu flackern.

## Farb-Abstufungen (Max: 1 Million Tokens)

| Symbol | Bedeutung | Schwellenwert |
|--------|-----------|---------------|
| ⚪ | Weiß | 0 - 2 % |
| 🟢 | Grün | 2 - 20 % |
| 🔵 | Blau | 20 - 45 % |
| 🟡 | Gelb | 45 - 70 % |
| 🟠 | Orange | 70 - 85 % |
| 🔴 | Rot (Kritisch) | 85 - 100 % |

## Architektur

1. **Client (Hook)**: `PostInvocation`-Event löst `context_hook.py` aus. Dieses schätzt die Tokens und schreibt sie in `state.json`.
2. **Server (Widget)**: `pythonw context_hook.py --gui-server` läuft als persistenter Task im System-Tray, liest `state.json` und zeichnet das Tkinter-Overlay.

## Lizenz

Apache 2.0 – frei nutzbar, Änderungen erlaubt, Attribution erforderlich.
