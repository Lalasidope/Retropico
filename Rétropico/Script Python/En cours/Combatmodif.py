import pyautogui
import cv2
import numpy as np
import time
import random
import os

# ============ CONFIG ============
RESOURCES_FOLDER = "D:/macro-dofus-main/macro-dofus-main/ressources"
SCAN_REGION = (562, 22, 1356, 1018)
CONFIDENCE_THRESHOLD = 0.75
SLEEP_BETWEEN_CHECKS = 0.3
SLEEP_AFTER_ACTION = 1.7
COOLDOWN_AFTER_COMBAT = 4  # Attendre 5 secondes après un combat avant de relancer

# Images des groupes de monstres (remplacez les noms des images)
MONSTER_GROUP_IMAGES = [
    "kokoko1.png",
    "kokoko2.png",
    "kokoko3.png",
    "kokoko4.png",
    "kokoko5.png",
    "kokoko.png",
    "koko.png",
    "fourbasse.png",
    "tikoko.png"
]

# Images pour les phases de combat
COMBAT_READY_IMAGE = "combat_ready.png"
YOUR_TURN_IMAGE = "jouer.png"
COMBAT_END_IMAGE = "fermer_drop.png"

# ============ DÉTECTION D'IMAGE ============
def detect_and_click(resource_path, region, threshold=0.75, do_click=False, right_click=False, offset=(0, 0)):
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
            if right_click:
                pyautogui.rightClick()
            else:
                pyautogui.click()

        return True
    return False

# ============ ÉTATS DU BOT ============
class BotState:
    IDLE = 0
    COMBAT_STARTED = 1
    PLACEMENT_DONE = 2
    TURN_PLAYED = 3
    COMBAT_ENDED = 4

# ============ CONFIG ============
# Ajouter cette constante
MAX_COMBAT_START_WAIT = 10  # Temps max d'attente pour détecter le début de combat

# ============ BOUCLE PRINCIPALE ============
def main():
    print("🚀 Lancement du bot DOFUS - Version anti-flood")
    current_state = BotState.IDLE
    last_combat_time = 0
    combat_start_time = 0  # Ajouter cette variable pour suivre le temps depuis le lancement du combat

    while True:
        now = time.time()

        # Vérifier l'état actuel
        if current_state == BotState.IDLE:
            # Phase 1 - Lancer un combat seulement si le cooldown est passé
            if now - last_combat_time > COOLDOWN_AFTER_COMBAT:
                for monster_img in MONSTER_GROUP_IMAGES:
                    if detect_and_click(monster_img, SCAN_REGION, CONFIDENCE_THRESHOLD,
                                      do_click=True, right_click=True):
                        print("⚔ Combat lancé (clic droit)")
                        current_state = BotState.COMBAT_STARTED
                        combat_start_time = now  # Enregistrer le moment du lancement
                        time.sleep(2)  # Court délai après lancement
                        break

        elif current_state == BotState.COMBAT_STARTED:
            # Phase 2 - Vérifier si le combat a commencé
            if detect_and_click(COMBAT_READY_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🛡️ Début de combat détecté")
                action_placement()
                current_state = BotState.PLACEMENT_DONE
            elif now - combat_start_time > MAX_COMBAT_START_WAIT:
                # Si on attend trop longtemps sans détecter le début de combat
                print("⏳ Timeout - Retour à l'état IDLE")
                current_state = BotState.IDLE

        elif current_state == BotState.PLACEMENT_DONE:
            # Phase 3 - Attendre notre tour
            if detect_and_click(YOUR_TURN_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🎮 Notre tour détecté")
                action_combat()
                current_state = BotState.TURN_PLAYED

        elif current_state == BotState.TURN_PLAYED:
            # Phase 4 - Attendre la fin du combat
            if detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🏁 Fin de combat détectée")
                action_fin_combat()
                current_state = BotState.COMBAT_ENDED
                last_combat_time = time.time()

        elif current_state == BotState.COMBAT_ENDED:
            # Retour à l'état inactif après un court délai
            print(f"⏳ Attente de {COOLDOWN_AFTER_COMBAT} secondes avant nouveau combat")
            time.sleep(COOLDOWN_AFTER_COMBAT)
            current_state = BotState.IDLE

        time.sleep(SLEEP_BETWEEN_CHECKS)

def action_placement():
    print("🛡️ Placement en combat")
    time.sleep(1)
    pyautogui.click(x=1675, y=588)
    time.sleep(2)
    pyautogui.click(x=1476, y=674)
    time.sleep(2)
    pyautogui.press("f1")
    time.sleep(SLEEP_AFTER_ACTION)

def action_combat():
    print("⚔️ Tour de jeu (sorts)")
    time.sleep(1)
    pyautogui.moveTo(x=1589, y=936)
    pyautogui.rightClick(x=1589, y=936)  # vent
    time.sleep(3)
    pyautogui.moveTo(x=1534, y=940)
    pyautogui.rightClick(x=1534, y=940)  # trembl
    time.sleep(4)
    pyautogui.moveTo(x=1642, y=939)
    time.sleep(2)
    pyautogui.rightClick(x=1642, y=939)  # Arbre
    time.sleep(2)
    pyautogui.press("f1")
    time.sleep(SLEEP_AFTER_ACTION)

def action_fin_combat():
    print("🏁 Fin de combat - Fermeture drop")
    time.sleep(1)
    detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, threshold=CONFIDENCE_THRESHOLD,)
    pyautogui.press("esc")
    time.sleep(SLEEP_AFTER_ACTION)

if __name__ == "__main__":
    main()