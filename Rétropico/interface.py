import tkinter as tk
from tkinter import scrolledtext, filedialog
import threading
import sys
import io
from PIL import Image, ImageTk
import time

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dofus Bot Controller")
        self.root.geometry("900x700")

        # Variables d'état
        self.script_running = False
        self.script_paused = False
        self.current_script = None

        # Création de l'interface
        self.create_widgets()

        # Redirection des prints
        self.redirect_prints()

    def create_widgets(self):
        # Frame principale
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Zone de logs
        self.log_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            state='disabled'
        )
        self.log_area.grid(row=0, column=0, columnspan=3, pady=5, sticky="nsew")

        # Boutons de contrôle
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, pady=10, sticky="w")

        self.load_btn = tk.Button(
            btn_frame,
            text="Charger Script",
            command=self.load_script,
            width=15
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.run_btn = tk.Button(
            btn_frame,
            text="Lancer",
            command=self.toggle_script,
            width=15,
            state=tk.DISABLED
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(
            btn_frame,
            text="Pause",
            command=self.toggle_pause,
            width=15,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        # Configuration
        config_frame = tk.LabelFrame(main_frame, text="Paramètres", padx=10, pady=10)
        config_frame.grid(row=2, column=0, sticky="ew", pady=10)

        # Exemple de paramètre (à adapter)
        self.var_speed = tk.StringVar(value="1.0")
        tk.Label(config_frame, text="Vitesse:").grid(row=0, column=0)
        tk.Entry(config_frame, textvariable=self.var_speed, width=10).grid(row=0, column=1)

        # Ajustement des tailles
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def redirect_prints(self):
        """Redirige les prints vers la zone de texte"""
        class PrintRedirector(io.StringIO):
            def __init__(self, widget):
                super().__init__()
                self.widget = widget

            def write(self, text):
                self.widget.config(state=tk.NORMAL)
                self.widget.insert(tk.END, text)
                self.widget.see(tk.END)
                self.widget.config(state=tk.DISABLED)

        sys.stdout = PrintRedirector(self.log_area)
        sys.stderr = PrintRedirector(self.log_area)

    def load_script(self):
        """Charge un script Python"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Fichiers Python", "*.py"), ("Tous fichiers", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.current_script = f.read()
                print(f"✅ Script chargé: {filepath}")
                self.run_btn.config(state=tk.NORMAL)
            except Exception as e:
                print(f"❌ Erreur: {str(e)}")

    def toggle_script(self):
        """Lance/arrête le script"""
        if not self.script_running:
            # Lancement du script
            self.script_thread = threading.Thread(
                target=self.execute_script,
                daemon=True
            )
            self.script_running = True
            self.script_thread.start()
            self.run_btn.config(text="Arrêter")
            self.pause_btn.config(state=tk.NORMAL)
            print("▶ Script lancé")
        else:
            # Arrêt du script
            self.script_running = False
            self.run_btn.config(text="Lancer")
            self.pause_btn.config(state=tk.DISABLED)
            print("⏹ Script arrêté")

    def toggle_pause(self):
        """Met en pause/reprend le script"""
        self.script_paused = not self.script_paused
        if self.script_paused:
            self.pause_btn.config(text="Reprendre")
            print("⏸ Script en pause")
        else:
            self.pause_btn.config(text="Pause")
            print("▶ Script repris")



    def execute_script(self):
    """Exécute le script chargé"""
    try:
        import Kokoperso_corrigé as bot_script
        bot_script.script_running = True
        bot_script.script_paused = False

        # Création d'un thread pour le bot
        self.bot_thread = threading.Thread(
            target=bot_script.main,
            daemon=True
        )
        self.bot_thread.start()

    except Exception as e:
        print(f"⚠ Erreur d'exécution: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()