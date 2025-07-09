import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from pynput import mouse, keyboard
import time
import os

# === Config ===
SAVE_DIR = "./dofus_recordings"
os.makedirs(SAVE_DIR, exist_ok=True)

class Recorder:
    def __init__(self):
        self.actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None

    def _now(self):
        return time.time() - self.start_time

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
        action = {
            "type": "click",
            "x": x,
            "y": y,
            "button": str(button),
            "time": self._now()
        }
        self.actions.append(action)

    def on_press(self, key):
        try:
            k = key.char
        except AttributeError:
            k = str(key)
        action = {
            "type": "key",
            "key": k,
            "time": self._now()
        }
        self.actions.append(action)

    def start(self):
        self.actions = []
        self.start_time = time.time()
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def export_pyautogui(self):
        lines = ["import pyautogui", "import time", ""]
        prev_time = 0
        for act in self.actions:
            delay = act["time"] - prev_time
            if delay > 0:
                lines.append(f"time.sleep({delay:.2f})")
            if act["type"] == "click":
                btn = "rightClick" if "right" in act["button"] else "click"
                lines.append(f"pyautogui.moveTo({act['x']}, {act['y']})")
                lines.append(f"pyautogui.{btn}()")
            elif act["type"] == "key":
                lines.append(f"pyautogui.press('{act['key']}')")
            prev_time = act["time"]
        return "\n".join(lines)

class RecorderApp:
    def __init__(self, root):
        self.recorder = Recorder()
        self.root = root
        self.root.title("🎮 Dofus Action Recorder")

        self.label = tk.Label(root, text="Nom de l'action :")
        self.label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(fill=tk.X, padx=10)

        self.start_btn = tk.Button(root, text="● Démarrer l'enregistrement", command=self.start_recording, bg="green", fg="white")
        self.start_btn.pack(fill=tk.X, padx=10, pady=5)

        self.stop_btn = tk.Button(root, text="⏹ Arrêter", command=self.stop_recording, bg="red", fg="white")
        self.stop_btn.pack(fill=tk.X, padx=10, pady=5)

        self.export_btn = tk.Button(root, text="⬇ Exporter script", command=self.export_script)
        self.export_btn.pack(fill=tk.X, padx=10, pady=5)

    def start_recording(self):
        self.recorder.start()
        messagebox.showinfo("Enregistrement", "Enregistrement lancé. Fais tes actions dans Dofus.")

    def stop_recording(self):
        self.recorder.stop()
        messagebox.showinfo("Arrêt", "Enregistrement arrêté.")

    def export_script(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Donne un nom à l'action enregistrée.")
            return
        content = self.recorder.export_pyautogui()
        filepath = os.path.join(SAVE_DIR, f"{name}.py")
        with open(filepath, "w") as f:
            f.write(content)
        messagebox.showinfo("Succès", f"Script sauvegardé : {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()