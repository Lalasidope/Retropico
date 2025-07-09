import pyautogui
import cv2
import numpy as np
import time
import random
import os

# ==================== CONFIG ====================

# 📂 Chemin vers ton dossier contenant les ressources (images .png)
RESOURCES_FOLDER = "D:/macro-dofus-main/macro-dofus-main/ressources"

# 🖼️ Liste des images de ressources à détecter
RESOURCE_IMAGES = [
    "kobalte.png",  # Exemple
    "manganese.png",
    "manganesene.png",

]

# 🧭 Région de l'écran à scruter (x, y, largeur, hauteur)
# ⚠️ ICI tu dois calibrer en fonction de ta fenêtre DOFUS
SCAN_REGION = (567, 28, 1340, 772)

# Exemple : toute la fenêtre de jeu sans la barre de titre

# 🎯 Seuil de détection (0.8 recommandé pour Dofus)
CONFIDENCE_THRESHOLD = 0.7

# 💤 Temps d'attente entre deux recherches
SLEEP_BETWEEN_CHECKS = 0.5
# 💤 Temps d'attente après clic (récolte)
SLEEP_AFTER_CLICK = 5

# =================================================


def detect_and_click(resource_path, region, threshold=0.7):
    # Screenshot de la région définie
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Chargement de l'image de la ressource
    resource_img = cv2.imread(resource_path)
    if resource_img is None:
        print(f"❌ Erreur chargement image: {resource_path}")
        return False

    result = cv2.matchTemplate(screenshot, resource_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # Coordonnées dans la fenêtre
        rel_x = max_loc[0] + resource_img.shape[1] // 2
        rel_y = max_loc[1] + resource_img.shape[0] // 2

        # Ajustement par rapport au scan_region
        abs_x = region[0] + rel_x
        abs_y = region[1] + rel_y

        # Randomiser un peu pour paraître humain
        abs_x += random.randint(-5, 5)
        abs_y += random.randint(-5, 5)

        print(f"🎯 Ressource trouvée à ({abs_x}, {abs_y}) confiance: {max_val:.2f}")

        # Premier clic sur la ressource
        pyautogui.moveTo(abs_x, abs_y, duration=(0.1))
        pyautogui.click()

        # Attente très courte pour laisser apparaître le bouton de validation
        time.sleep(0.2)

        # Deuxième clic légèrement en bas à droite
        offset_x = random.randint(40, 50)
        offset_y = random.randint(40, 50)
        new_x = abs_x + offset_x
        new_y = abs_y + offset_y

        print(f"🖱️ Validation par clic secondaire à ({new_x}, {new_y})")
        pyautogui.moveTo(new_x, new_y, duration=(0.1))
        pyautogui.click()

        return True
    else:
        return False


def main():
    print("🚀 Lancement du bot de récolte Dofus Retro...")
    # Test simple pour voir les fichiers
print("🖼️ Images détectées dans le dossier ressources :")
for img in RESOURCE_IMAGES:
    img_path = os.path.join(RESOURCES_FOLDER, img)
    print(f" - {img_path} existe ? {os.path.exists(img_path)}")

    while True:
        found = False

        for img_name in RESOURCE_IMAGES:
            img_path = os.path.join(RESOURCES_FOLDER, img_name)
            if detect_and_click(img_path, SCAN_REGION, threshold=CONFIDENCE_THRESHOLD):
                found = True
                break  # Stop après une récolte trouvée pour ne pas cliquer deux fois

        if found:
            time.sleep(SLEEP_AFTER_CLICK)  # On attend que la récolte soit faite
        else:
            time.sleep(SLEEP_BETWEEN_CHECKS)

if __name__ == "__main__":
    main()
