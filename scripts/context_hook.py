import sys
import json
import os
from datetime import datetime

def log_debug(msg):
    try:
        with open(r"C:\AI_Engineering\.agents\plugins\context_watchdog\hook_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")
    except:
        pass

def main():
    log_debug("Hook gestartet!")
    try:
        input_data = json.load(sys.stdin)
        log_debug(f"Input received: {json.dumps(input_data)[:200]}")
    except Exception as e:
        log_debug(f"Fehler beim Lesen von stdin: {e}")
        input_data = {}

    transcript_path = input_data.get("transcriptPath", "")
    if not transcript_path or not os.path.exists(transcript_path):
        # No transcript available – still provide a status message
        log_debug(f"Transcript path not found or missing: {transcript_path}")
        status = "⚪ NO TRANSCRIPT"
        token_k = "0k"
        max_k = "1000k"
        percent = 0
        message = f"**Kontext-Wächter:** {status} | {token_k} / {max_k} Tokens ({percent}%) genutzt."
        output = {"injectSteps": [{"ephemeralMessage": message}]}
        print(json.dumps(output))
        log_debug("Fertig ohne Transcript.")
        return

    log_debug(f"Transcript path gefunden: {transcript_path}")
    total_chars = 0
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_chars += len(line)
    except Exception as e:
        log_debug(f"Fehler beim Lesen der Datei: {e}")
    
    estimated_tokens = int(total_chars / 3.6)
    max_tokens = 1_000_000

    if estimated_tokens >= 750_000:
        status = "🔴 KRITISCH"
    elif estimated_tokens >= 400_000:
        status = "🟡 WARNUNG"
    else:
        status = "🟢 OK"
    
    token_k = f"{estimated_tokens/1000:.1f}k"
    max_k = f"{max_tokens/1000:.0f}k"
    percent = round((estimated_tokens / max_tokens) * 100)
    
    message = f"**Kontext-Wächter:** {status} | {token_k} / {max_k} Tokens ({percent}%) genutzt."
    log_debug(f"Sende Ephemeral Message: {message}")

    output = {
        "injectSteps": [
            {
                "ephemeralMessage": message
            }
        ],
        "terminationBehavior": ""
    }
    
    print(json.dumps(output))
    log_debug("Fertig.")

if __name__ == "__main__":
    main()
