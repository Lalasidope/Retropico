import pyautogui
import cv2
import numpy as np
import time
import random
import os

# ============ CONFIG ============
RESOURCES_FOLDER = "D:/macro-dofus-main/macro-dofus-main/ressources"
SCAN_REGION = (562, 22, 1356, 1018)
CONFIDENCE_THRESHOLD = 0.68
BASE_SLEEP_BETWEEN_CHECKS = 0.3
BASE_SLEEP_AFTER_ACTION = 1.7
BASE_COOLDOWN_AFTER_COMBAT = 4
MAX_COMBAT_START_WAIT = 10
script_running = True
script_paused = False

# Images des groupes de monstres
MONSTER_GROUP_IMAGES = [
    "sanglierp.png",
    "sanglierp1.png",
    "sanglierp2.png",
    "sanglierp3.png",
    "tournesol.png",
    "tournesol1.png",
    "pissenlit.png",
    "pissenlit1.png"
]

# Images pour les phases de combat
PASS_TURN_IMAGE = "pass_turn.png"
COMBAT_READY_IMAGE = "combat_ready.png"
YOUR_TURN_IMAGE = "jouer.png"
COMBAT_END_IMAGE = "fermer_drop.png"
COMBAT_COUNT = 0  # Compteur de combats
TURN_COUNT = 0     # Compteur de tours dans le combat actuel

# ============ FONCTIONS UTILITAIRES ============
def get_random_sleep(base_time):
    return base_time * random.uniform(0.8, 1.2)

def get_random_offset(max_offset=5):
    return random.randint(-max_offset, max_offset)

def get_spell_offset():
    return random.randint(-3, 3)

# ============ DÉTECTION D'IMAGE ============
def detect_and_click(resource_path, region, threshold=0.68, do_click=False, right_click=False, offset=(0, 0), no_offset=False):
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
            if no_offset:
                center_x = max_loc[0] + resource_img.shape[1] // 2 + offset[0]
                center_y = max_loc[1] + resource_img.shape[0] // 2 + offset[1]
            else:
                center_x = max_loc[0] + resource_img.shape[1] // 2 + offset[0] + get_random_offset()
                center_y = max_loc[1] + resource_img.shape[0] // 2 + offset[1] + get_random_offset()

            abs_x = region[0] + center_x
            abs_y = region[1] + center_y

            pyautogui.moveTo(abs_x, abs_y, duration=random.uniform(0.1, 0.3))
            if right_click:
                pyautogui.rightClick()
            else:
                pyautogui.click()

            time.sleep(get_random_sleep(0.2))

        return True
    return False

# ============ ÉTATS DU BOT ============
class BotState:
    IDLE = 0
    COMBAT_STARTED = 1
    TURN_PLAYED = 2
    COMBAT_ENDED = 3

# ============ ACTIONS ============
def pass_turn():
    global TURN_COUNT
    print("🔄 Vérification pour passer le tour...")
    if detect_and_click(YOUR_TURN_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
        print("⏩ Passage du tour (F1)")
        pyautogui.press("f1")
        TURN_COUNT += 1  # Incrémente SEULEMENT quand on passe effectivement le tour
        print(f"🔢 Tours passés dans ce combat : {TURN_COUNT}")
        time.sleep(get_random_sleep(0.5))
    else:
        time.sleep(get_random_sleep(3.0))

def action_combat():
    global TURN_COUNT
    print("⚔️ Tour de jeu (sorts)")

    # Séquence de sorts
    spells = [
        (1589, 936, 3),  # Vent
        (1534, 940, 4),  # Tremblement
        (1642, 939, 2)   # Arbre
    ]

    for x, y, delay in spells:
        pyautogui.moveTo(
            x=x + get_spell_offset(),
            y=y + get_spell_offset(),
            duration=random.uniform(0.1, 0.3)
        )
        pyautogui.rightClick()
        time.sleep(get_random_sleep(delay))

    # Après avoir lancé les sorts, on passe le tour
    pass_turn()

    # Vérification si on doit relancer les sorts (seulement si 5 tours passés)
    if TURN_COUNT >= 5:
        print(f"♻️ {TURN_COUNT} tours passés - Relance des sorts")
        TURN_COUNT = 0  # Réinitialisation du compteur
        action_combat()  # Rappel récursif

def action_fin_combat():
    global COMBAT_COUNT, TURN_COUNT
    print("🏁 Fin de combat - Fermeture drop")
    time.sleep(get_random_sleep(1))
    if detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, threshold=CONFIDENCE_THRESHOLD):
        COMBAT_COUNT += 1
        TURN_COUNT = 0  # Réinitialisation du compteur de tours
        print(f"🎉 Combats terminés : {COMBAT_COUNT}")
    pyautogui.press("esc")
    time.sleep(get_random_sleep(BASE_SLEEP_AFTER_ACTION))

# ============ BOUCLE PRINCIPALE ============
def main():
    global COMBAT_COUNT, script_running, script_paused, TURN_COUNT

    print("🚀 Lancement du bot DOFUS - Version optimisée")
    current_state = BotState.IDLE
    last_combat_time = 0
    combat_start_time = 0

    while script_running:
        now = time.time()

        if script_paused:
            print("⏸ En pause...")
            time.sleep(1)
            continue

        if current_state == BotState.IDLE:
            cooldown = get_random_sleep(BASE_COOLDOWN_AFTER_COMBAT)
            if now - last_combat_time > cooldown:
                for monster_img in MONSTER_GROUP_IMAGES:
                    if detect_and_click(monster_img, SCAN_REGION, CONFIDENCE_THRESHOLD,
                                      do_click=True, right_click=True, no_offset=True):
                        print(f"⚔ Combat lancé - Prochain cooldown: {cooldown:.2f}s")
                        current_state = BotState.COMBAT_STARTED
                        combat_start_time = now
                        TURN_COUNT = 0  # Réinitialisation du compteur
                        time.sleep(get_random_sleep(2))
                        break

        elif current_state == BotState.COMBAT_STARTED:
            if detect_and_click(COMBAT_READY_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🛡️ Début de combat détecté")
                current_state = BotState.TURN_PLAYED
            elif now - combat_start_time > MAX_COMBAT_START_WAIT:
                print("⏳ Timeout - Retour à l'état IDLE")
                current_state = BotState.IDLE

        elif current_state == BotState.TURN_PLAYED:
            if detect_and_click(YOUR_TURN_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🎮 Notre tour détecté")
                time.sleep(1)
                action_combat()
            elif detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🏁 Fin de combat détectée")
                action_fin_combat()
                current_state = BotState.COMBAT_ENDED
                last_combat_time = time.time()
            else:
                pass_turn()

        elif current_state == BotState.COMBAT_ENDED:
            cooldown = get_random_sleep(BASE_COOLDOWN_AFTER_COMBAT)
            print(f"⏳ Attente de {cooldown:.2f} secondes avant nouveau combat")
            time.sleep(cooldown)
            current_state = BotState.IDLE

        time.sleep(get_random_sleep(BASE_SLEEP_BETWEEN_CHECKS))

if __name__ == "__main__":
    main()