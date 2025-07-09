import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re

def convert_ahk_to_py(input_ahk: str) -> str:
    output_lines = [
        "import pyautogui",
        "import time",
        ""
    ]

    for line in input_ahk.splitlines():
        line = line.strip()
        if line.startswith(";") or line == "":
            continue

        if line.lower().startswith("send,"):
            text = line[5:].strip().replace("{ENTER}", "\n")
            output_lines.append(f'pyautogui.write("{text}")')

        elif line.lower().startswith("sleep"):
            ms = re.findall(r"\d+", line)
            if ms:
                seconds = int(ms[0]) / 1000
                output_lines.append(f"time.sleep({seconds})")

        elif line.lower().startswith("click"):
            parts = line.split(",")
            if len(parts) >= 3:
                x, y = parts[1].strip(), parts[2].strip()
                output_lines.append(f"pyautogui.click({x}, {y})")
            else:
                output_lines.append("pyautogui.click()")

        elif line.lower().startswith("mousemove"):
            parts = line.split(",")
            if len(parts) >= 3:
                x, y = parts[1].strip(), parts[2].strip()
                output_lines.append(f"pyautogui.moveTo({x}, {y})")

        elif re.match(r"^[\^\!\+\#]*\w+::", line):
            output_lines.append(f"# TODO: Convertir le raccourci: {line}")

        else:
            output_lines.append(f"# TODO: Ligne non prise en charge: {line}")

    return "\n".join(output_lines)

class AHKConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur AHK → Python (PyAutoGUI)")
        self.root.geometry("800x600")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        btn_load = tk.Button(frame, text="Charger AHK", command=self.load_file)
        btn_load.grid(row=0, column=0, padx=10)

        btn_convert = tk.Button(frame, text="Convertir", command=self.convert_code)
        btn_convert.grid(row=0, column=1, padx=10)

        btn_save = tk.Button(frame, text="Enregistrer .py", command=self.save_file)
        btn_save.grid(row=0, column=2, padx=10)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("AHK files", "*.ahk")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                ahk_code = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, ahk_code)

    def convert_code(self):
        ahk_code = self.text_area.get(1.0, tk.END)
        py_code = convert_ahk_to_py(ahk_code)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, py_code)

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Enregistré", "Fichier Python enregistré avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AHKConverterApp(root)
    root.mainloop()
