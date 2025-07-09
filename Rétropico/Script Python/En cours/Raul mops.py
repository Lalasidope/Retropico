import pyautogui
import cv2
import numpy as np
import time
import random
import os

# ============ CONFIG ============
RESOURCES_FOLDER = "D:/macro-dofus-main/macro-dofus-main/ressources"
SCAN_REGION = (562, 22, 1356, 1018)
CONFIDENCE_THRESHOLD = 0.70
BASE_SLEEP_BETWEEN_CHECKS = 0.3
BASE_SLEEP_AFTER_ACTION = 1.7
BASE_COOLDOWN_AFTER_COMBAT = 4
MAX_COMBAT_START_WAIT = 10
script_running = True
script_paused = False

# Compteurs
COMBAT_COUNT = 0  # Compteur de combats
CURRENT_TURN = 1   # Compteur de tours en combat

# Images des groupes de monstres
MONSTER_GROUP_IMAGES = [
    "raulmops.png",
    "raulmops1.png",
    "pichonorange.png",
    "pichonblanc.png",
    "pichonorange1.png",
    "pichonvert.png",
    "pichonkloune.png"
]

# Images pour les phases de combat
PASS_TURN_IMAGE = "pass_turn.png"
COMBAT_READY_IMAGE = "combat_ready.png"
YOUR_TURN_IMAGE = "jouer.png"
COMBAT_END_IMAGE = "fermer_drop.png"

# ============ FONCTIONS UTILITAIRES ============
def get_random_sleep(base_time):
    return base_time * random.uniform(0.8, 1.2)

def get_random_offset(max_offset=5):
    return random.randint(-max_offset, max_offset)

def get_spell_offset():
    return random.randint(-3, 3)  # Offset réduit pour les sorts (±3px)

# ============ DÉTECTION D'IMAGE ============
def detect_and_click(resource_path, region, threshold=0.70, do_click=False, right_click=False, offset=(0, 0), no_offset=False):
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
    PLACEMENT_DONE = 2
    TURN_PLAYED = 3
    COMBAT_ENDED = 4

# ============ ACTIONS ============
def action_deplacement():
    print("🚶 Déplacement du personnage")
    deplacement_coords = [(1096, 347), (1193, 443)]
    for (x, y) in deplacement_coords:
        target_x = x + get_random_offset(2)
        target_y = y + get_random_offset(3)

        pyautogui.moveTo(
            x=target_x,
            y=target_y,
            duration=random.uniform(0.1, 0.3)
        )

        time.sleep(1.5)
        pyautogui.click()
        time.sleep(1.0)
        pyautogui.moveTo(1757, 671)
        time.sleep(1.0)

def pass_turn():
    global CURRENT_TURN
    if detect_and_click(PASS_TURN_IMAGE, SCAN_REGION, threshold=0.70):
        print(f"🔄 Vérification pour passer le tour... (Tour {CURRENT_TURN})")
        pyautogui.moveTo(1529, 984)
        time.sleep(1)
        pyautogui.rightClick()
        time.sleep(get_random_sleep(3))
        pyautogui.rightClick()
        time.sleep(get_random_sleep(3))
        pyautogui.press("f1")
        time.sleep(get_random_sleep(0.5))
        pyautogui.press("f1")
        time.sleep(get_random_sleep(0.5))
    else:
        time.sleep(get_random_sleep(3.0))
    CURRENT_TURN += 1

def action_placement():
    print("🛡️ Placement en combat")
    time.sleep(get_random_sleep(2))

    base_x, base_y = 901, 246
    pyautogui.click(
        x=base_x + get_random_offset(3),
        y=base_y + get_random_offset(3),
        duration=random.uniform(0.1, 0.3)
    )
    time.sleep(get_random_sleep(2))

    base_x, base_y = 1351, 493
    pyautogui.click(
        x=base_x + get_random_offset(2),
        y=base_y + get_random_offset(2),
        duration=random.uniform(0.1, 0.3)
    )
    time.sleep(get_random_sleep(2))
    pyautogui.moveTo(1757, 671)
    pyautogui.press("f1")
    time.sleep(get_random_sleep(BASE_SLEEP_AFTER_ACTION))

def action_combat():
    print("⚔️ Tour de jeu (sorts)")
    time.sleep(get_random_sleep(1))
    pyautogui.moveTo(1529,984)
    time.sleep(1)
    pyautogui.rightClick()
    time.sleep(get_random_sleep(3))
    pyautogui.rightClick()
    time.sleep(get_random_sleep(3))
    pyautogui.press("f1")
    time.sleep(get_random_sleep(0.5))

def action_combat_tour_1():
    print("⚔️ Action spécifique tour 1")
    time.sleep(get_random_sleep(1))
    time.sleep(1.55)
    pyautogui.moveTo(1093, 600)
    pyautogui.click()
    time.sleep(5.05)
    pyautogui.moveTo(1891, 905)
    pyautogui.click()
    time.sleep(0.70)
    pyautogui.moveTo(1877, 936)
    pyautogui.click()
    time.sleep(1.20)
    pyautogui.moveTo(1885, 915)
    pyautogui.click()
    time.sleep(1.99)
    pyautogui.moveTo(1851, 929)
    pyautogui.rightClick()
    time.sleep(1.57)
    pyautogui.moveTo(1583, 991)
    pyautogui.rightClick()
    time.sleep(1.73)
    pyautogui.moveTo(1457, 1007)
    pyautogui.click()
    time.sleep(13.32)
    pyautogui.moveTo(1534, 990)
    pyautogui.rightClick()
    time.sleep(0.95)
    pyautogui.moveTo(1534, 990)
    pyautogui.rightClick()
    time.sleep(1.30)
    pyautogui.moveTo(1534, 990)
    pyautogui.rightClick()
    time.sleep(1.27)
    pyautogui.moveTo(1473, 1002)
    pyautogui.click()
    time.sleep(1.20)
    pyautogui.moveTo(1097, 1052)
    pyautogui.click()
    time.sleep(0.66)
    pyautogui.moveTo(327, 360)
    pyautogui.click()
    time.sleep(0.97)
    pyautogui.moveTo(1078, 1042)
    pyautogui.click()
    time.sleep(1.12)
    pyautogui.moveTo(246, 244)
    pyautogui.click()
    pass_turn()
    pyautogui.press("f1")
    time.sleep(get_random_sleep(BASE_SLEEP_AFTER_ACTION))

def action_combat_tour_2():
    print("⚔️ Action spécifique tour 2")
    # Insérer logique spécifique tour 2
    pyautogui.moveTo(1529,984)
    time.sleep(1)
    pyautogui.rightClick()
    time.sleep(get_random_sleep(3))
    pyautogui.rightClick()
    time.sleep(get_random_sleep(3))
    pyautogui.press("f1")
    time.sleep(get_random_sleep(0.5))

def action_fin_combat():
    global COMBAT_COUNT, CURRENT_TURN
    print("🏁 Fin de combat - Fermeture drop")
    CURRENT_TURN = 1  # Réinitialisation du compteur de tours
    time.sleep(get_random_sleep(1))
    if detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, threshold=CONFIDENCE_THRESHOLD):
        COMBAT_COUNT += 1
        print(f"🎉 Combats terminés : {COMBAT_COUNT}")
    pyautogui.press("esc")
    time.sleep(get_random_sleep(BASE_SLEEP_AFTER_ACTION))

# ============ BOUCLE PRINCIPALE ============
def main():
    global COMBAT_COUNT, script_running, script_paused

    print("🚀 Lancement du bot DOFUS - Version précise")
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
                        print(f"⚔ Combat lancé (clic droit précis) - Prochain cooldown: {cooldown:.2f}s")
                        current_state = BotState.COMBAT_STARTED
                        combat_start_time = now
                        time.sleep(get_random_sleep(2))
                        break

        elif current_state == BotState.COMBAT_STARTED:
            if detect_and_click(COMBAT_READY_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🛡️ Début de combat détecté")
                action_placement()
                current_state = BotState.PLACEMENT_DONE
            elif now - combat_start_time > MAX_COMBAT_START_WAIT:
                print("⏳ Timeout - Retour à l'état IDLE")
                current_state = BotState.IDLE

        elif current_state == BotState.PLACEMENT_DONE:
            if detect_and_click(YOUR_TURN_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
                print("🎮 Notre tour détecté")
                time.sleep(1)
                if CURRENT_TURN == 1:
                    action_combat_tour_1()
                elif CURRENT_TURN == 2:
                    action_combat_tour_2()
                else:
                    action_combat()
                current_state = BotState.TURN_PLAYED

        elif current_state == BotState.TURN_PLAYED:
            if detect_and_click(COMBAT_END_IMAGE, SCAN_REGION, CONFIDENCE_THRESHOLD):
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
