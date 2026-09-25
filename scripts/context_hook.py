import sys
import json
import os
import socket
import threading
from datetime import datetime

LOG_FILE = r"C:\AI_Engineering\.agents\plugins\context_watchdog\hook_debug.log"
STATE_FILE = r"C:\AI_Engineering\.agents\plugins\context_watchdog\state.json"
CONFIG_FILE = r"C:\AI_Engineering\.agents\plugins\context_watchdog\config.json"
GUI_PORT = 49200

def log_debug(msg):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")
    except:
        pass

def run_gui_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", GUI_PORT))
        s.listen(1)
    except OSError:
        return

    import tkinter as tk
    import pystray
    from PIL import Image, ImageDraw

    # Lade Position und Fixierungs-Status
    config = {"x": None, "y": None, "fixed": False}
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config.update(json.load(f))
    except:
        pass

    def save_config():
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
        except:
            pass

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.configure(bg='black')
    root.wm_attributes('-transparentcolor', 'black')

    lbl_msg = tk.Label(root, text="⚪ --k / 1000k", fg='white', bg='black', font=('Segoe UI', 9, 'bold'))
    lbl_msg.pack()

    # --- DRAG & DROP MIT FIXIERUNG ---
    def start_move(event):
        if not config.get("fixed", False):
            root.x = event.x
            root.y = event.y

    def stop_move(event):
        if not config.get("fixed", False):
            config["x"] = root.winfo_x()
            config["y"] = root.winfo_y()
            save_config()
            root.x = None
            root.y = None

    def do_move(event):
        if not config.get("fixed", False) and hasattr(root, 'x') and root.x is not None:
            x = root.winfo_x() + event.x - root.x
            y = root.winfo_y() + event.y - root.y
            root.geometry(f"+{x}+{y}")

    lbl_msg.bind("<ButtonPress-1>", start_move)
    lbl_msg.bind("<ButtonRelease-1>", stop_move)
    lbl_msg.bind("<B1-Motion>", do_move)

    def initial_position():
        root.update_idletasks()
        if config["x"] is not None and config["y"] is not None:
            root.geometry(f"+{config['x']}+{config['y']}")
        else:
            w = root.winfo_reqwidth()
            h = root.winfo_reqheight()
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            x = sw - w - 250 
            y = sh - h - 10  
            root.geometry(f'+{x}+{y}')
            config["x"] = x
            config["y"] = y
            save_config()

    # --- TRAY ICON ---
    def create_tray_image():
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill='white', outline='gray')
        return image

    def on_toggle_fix(icon, item):
        config["fixed"] = not config["fixed"]
        save_config()

    def on_show_log(icon, item):
        try:
            if os.path.exists(LOG_FILE):
                os.startfile(LOG_FILE)
        except Exception as e:
            pass

    def on_quit(icon, item):
        icon.stop()
        root.after(0, root.destroy)

    menu = pystray.Menu(
        pystray.MenuItem(lambda text: "🔒 Position fixiert" if config.get("fixed") else "🔓 Position verschiebbar", on_toggle_fix),
        pystray.MenuItem("📜 Log anzeigen", on_show_log),
        pystray.MenuItem("❌ Beenden", on_quit)
    )
    
    tray_icon = pystray.Icon("AgyKontext", create_tray_image(), "Kontext-Wächter", menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()

    # --- POLLING ---
    def poll_state():
        try:
            # Zwinge das Fenster jede Sekunde in den absoluten Vordergrund (über die Taskleiste!)
            root.lift()
            root.attributes('-topmost', True)

            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    new_text = data.get("message", "⚪ --k / 1000k")
                    if lbl_msg.cget("text") != new_text:
                        lbl_msg.config(text=new_text)
                        root.update_idletasks()
                        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
        except Exception:
            pass
        root.after(1000, poll_state)

    initial_position()
    poll_state()
    root.mainloop()

def get_status_icon(percent):
    if percent < 2: return "⚪"
    elif percent < 20: return "🟢"
    elif percent < 45: return "🔵"
    elif percent < 70: return "🟡"
    elif percent < 85: return "🟠"
    else: return "🔴"

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--gui-server":
        run_gui_server()
        return

    log_debug("Hook gestartet!")
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        input_data = {}

    transcript_path = input_data.get("transcriptPath", "")
    if not transcript_path or not os.path.exists(transcript_path):
        status_icon = "⚪"
        token_k = "0k"
        percent = 0
    else:
        total_chars = 0
        try:
            with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total_chars += len(line)
        except Exception:
            pass
        
        estimated_tokens = int(total_chars / 3.6)
        max_tokens = 1_000_000
        percent = round((estimated_tokens / max_tokens) * 100)
        
        status_icon = get_status_icon(percent)
        token_k = f"{estimated_tokens/1000:.1f}k"

    message_gui = f"{status_icon} {token_k} / 1000k ({percent}%)"
    message_ephemeral = f"**Kontext-Wächter:** {message_gui} genutzt."

    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"message": message_gui}, f)
    except Exception as e:
        log_debug(f"Fehler beim Schreiben der State-Datei: {e}")

    output = {
        "injectSteps": [{"ephemeralMessage": message_ephemeral}],
        "terminationBehavior": ""
    }
    
    print(json.dumps(output))
    log_debug("Fertig.")

if __name__ == "__main__":
    main()
