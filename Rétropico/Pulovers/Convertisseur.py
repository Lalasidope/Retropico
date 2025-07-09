import pyautogui
import time

def convert_ahk_to_pyautogui(ahk_file, python_file):
    with open(ahk_file, 'r') as f:
        lines = f.readlines()

    with open(python_file, 'w') as out:
        out.write('import pyautogui\n')
        out.write('import time\n\n')

        for line in lines:
            line = line.strip()

            if not line:  # Si la ligne est vide, on l'ignore
                continue

            # Conversion des commandes AHK en pyautogui

            # AHK Click
            if line.lower().startswith('click'):
                parts = line.split()
                if len(parts) == 3:
                    # Click x, y
                    try:
                        x, y = map(int, parts[1:])
                        out.write(f'pyautogui.click({x}, {y})\n')
                    except ValueError:
                        pass  # Ignore si les coordonnées ne sont pas valides
                elif len(parts) == 4 and parts[3].lower() == 'right':
                    # Right Click x, y
                    try:
                        x, y = map(int, parts[1:3])
                        out.write(f'pyautogui.click({x}, {y}, button="right")\n')
                    except ValueError:
                        pass  # Ignore si les coordonnées ne sont pas valides
                out.write('time.sleep(0.1)\n')  # Ajouter un délai pour simuler l'attente

            # AHK Move
            elif line.lower().startswith('move'):
                parts = line.split()
                try:
                    x, y = map(int, parts[1:])
                    out.write(f'pyautogui.moveTo({x}, {y})\n')
                    out.write('time.sleep(0.1)\n')  # Ajouter un délai pour simuler l'attente
                except ValueError:
                    pass  # Ignore si les coordonnées ne sont pas valides

            # AHK Sleep
            elif line.lower().startswith('sleep'):
                parts = line.split()
                try:
                    sleep_time = float(parts[1])
                    out.write(f'time.sleep({sleep_time})\n')
                except (ValueError, IndexError):
                    pass  # Ignore si la durée du sommeil est invalide

            # AHK Send (saisie de texte)
            elif line.lower().startswith('send'):
                text = " ".join(line.split()[1:])
                out.write(f'pyautogui.write("{text}")\n')
                out.write('time.sleep(0.1)\n')  # Ajouter un délai après l'envoi du texte

# Exemple d'utilisation
convert_ahk_to_pyautogui('fourbe.ahk', 'scriptfourbe.py')
