import pyautogui
import cv2
import numpy as np
import time
import random
import os

# ============ CONFIG ============
RESOURCES_FOLDER = "D:/macro-dofus-main/macro-dofus-main/ressources"
SCAN_REGION = (562, 22, 1356, 1018)
CONFIDENCE_THRESHOLD = 0.7
SLEEP_BETWEEN_CHECKS = 0.3
SLEEP_AFTER_ACTION = 0.5

RESOURCE_IMAGES = [
    "manganese.png",
    "manganesene.png",
    "kobalte.png",
    "kokoko1.png",
    "kokoko2.png",
    "kokoko3.png",
    "kokoko4.png"
]

# Images pour les différentes phases
COMBAT_READY_IMAGE = "combat_ready.png"      # Phase 2
YOUR_TURN_IMAGE = "jouer.png"                # Phase 3
COMBAT_END_IMAGE = "fermer_drop.png"         # Phase 4

# ============ DÉTECTION D'IMAGE ============
def detect_and_click(resource_path, region, threshold=0.7, do_click=False, offset=(0, 0)):
    full_path = os.path.join(RESOURCES_FOLDER, resource_path)
    resource_img = cv2.imread(full_path)
    if resource_img is None:
        print(f"❌ Image non trouvée : {full_path}")
        return False

    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot, resource_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Image détectée : {resource_path} (confiance {max_val:.2f})")

        if do_click:
            center_x = max_loc[0] + resource_img.shape[1] // 2 + offset[0]
            center_y = max_loc[1] + resource_img.shape[0] // 2 + offset[1]
            abs_x = region[0] + center_x + random.randint(-5, 5)
            abs_y = region[1] + center_y + random.randint(-5, 5)

            pyautogui.moveTo(abs_x, abs_y, duration=0.1)
            pyautogui.click()

        return True

    return False

# ============ ACTIONS ============
def action_recolte():
    print("🌿 Récolte...")
    time.sleep(SLEEP_AFTER_ACTION)

def action_placement():
    print("🛡️ Placement en combat")
    pyautogui.click(x=1680, y=482)
    time.sleep(0.5)
    pyautogui.click(x=1476, y=674)
    time.sleep(0.5)
    pyautogui.press("f1")
    time.sleep(SLEEP_AFTER_ACTION)

def action_combat():
    print("⚔️ Tour de jeu (sorts)")
    pyautogui.rightClick(x=1589, y=936) # tremblement
    time.sleep(0.7)
    pyautogui.rightClick(x=1534, y=940) # vent empoi
    time.sleep(0.7)
    pyautogui.rightClick(x=1642, y=939) # Arbre
    time.sleep(0.7)
    pyautogui.press("f1")
    time.sleep(SLEEP_AFTER_ACTION)

def action_fin_combat():
    print("🏁 Fin de combat - Fermeture drop")
    # ➤ Ici tu peux ajouter un offset si le bouton "Fermer" est décalé
    detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, threshold=CONFIDENCE_THRESHOLD,)
    pyautogui.press("esc")
    time.sleep(SLEEP_AFTER_ACTION)

# ============ BOUCLE PRINCIPALE ============
def main():
    print("🚀 Lancement du bot DOFUS multi-phases...")

    while True:
        # Phase 2 - Début de combat
        if detect_and_click(COMBAT_READY_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
            action_placement()
            continue

        # Phase 3 - Ton tour
        elif detect_and_click(YOUR_TURN_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
            action_combat()
            continue

        # Phase 4 - Fin de combat
        elif detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
            action_fin_combat()
            continue

        # Phase 1 - Récolte
        else:
            for res_img in RESOURCE_IMAGES:
                if detect_and_click(res_img, SCAN_REGION, CONFIDENCE_THRESHOLD, do_click=True):
                    action_recolte()
                    break

        time.sleep(SLEEP_BETWEEN_CHECKS)

if __name__ == "__main__":
    main()
