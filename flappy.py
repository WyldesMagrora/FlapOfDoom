import pygame, random, time, os, sys, json
from pygame.locals import *
import webbrowser  # Importiere die webbrowser-Bibliothek
import math
from random import randint, uniform
import ctypes
try:
    # Für Windows-spezifische Funktionalität
    import ctypes.wintypes
    # Setze die Prozess-AppUserModelID
    myappid = 'magrora.flapofdoom.1.0'  # Beliebige eindeutige ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass  # Auf nicht-Windows Systemen ignorieren

# Nach den Imports, vor den Konstanten
def get_resource_path(relative_path):
    """ Korrigiert den Pfad für PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        print(f"Warnung: Resource nicht gefunden: {full_path}")
    return full_path

# Verbesserte visuelle Effekte
MODERN_BACKGROUND = (50, 50, 70)
MODERN_HIGHLIGHT = (100, 150, 200)

# Gameplay Konstanten
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

# Asset Pfade als Konstanten
ASSET_PATH = 'assets'
SPRITE_PATH = os.path.join(ASSET_PATH, 'sprites')
AUDIO_PATH = os.path.join(ASSET_PATH, 'audio')
VIDEO_PATH = os.path.join(ASSET_PATH, 'video')

GROUND_WIDHT = 2 * SCREEN_WIDTH
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NIGHT_BLUE = (25, 25, 112)
DARK_BLUE = (0, 0, 139)
GRASS_GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
PIPE_GREEN = (67, 205, 128)

# Punktezähler Variable
score = 0

# Nach den Konstanten und vor pygame.init()

# Initialisiere Spielerdaten
COIN_REWARD = 5  # Münzen pro Punkt
player_coins = 0
unlocked_birds = {"default": True}  # Freigeschaltete Vögel
current_bird = "default"

# Bei den BIRD_SKINS Dictionary, fügen wir ein neues Dictionary für Hintergründe hinzu
BACKGROUND_SKINS = {
    "day": {
        "price": 0,
        "files": ["background-day.png"],
        "description": "Sonniger Tag"
    },
    "night": {
        "price": 500,
        "files": ["background-night.png"],
        "description": "Sternenklare Nacht"
    },
    "midnight": {
        "price": 1250,
        "files": ["background-midnight.png"],
        "description": "Mystische Mitternacht"
    }
}

# Nach den globalen Variablen am Anfang der Datei
current_background = "day"

# Nach den anderen Konstanten
PARTICLE_COLORS = {
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "blue": (0, 191, 255),
    "red": (255, 69, 0),
    "purple": (147, 112, 219)
}

# Partikelsystem Definitionen
PARTICLE_EFFECTS = {
    "default": {
        "price": 0,
        "color": "white",
        "description": "Keine Partikel",
        "max_particles": 0
    },
    "stardust": {
        "price": 250,
        "color": "yellow",
        "description": "Funkelnde Sterne",
        "max_particles": 6,
        "requires": ["blue", "red", "yellow"]  # Benötigt alle Vogel-Skins
    },
    "ice": {
        "price": 325,
        "color": "blue",
        "description": "Eisige Aura",
        "max_particles": 8,
        "requires": ["stardust", "night"]  # Benötigt Sternenstaub und Nacht-Hintergrund
    },
    "fire": {
        "price": 650,
        "color": "red",
        "description": "Feurige Spur",
        "max_particles": 10,
        "requires": ["ice", "midnight"]  # Benötigt Eiseffekt und Mitternacht-Hintergrund
    },
    "magic": {
        "price": 850,
        "color": "purple",
        "description": "Magische Essenz",
        "max_particles": 12,
        "requires": ["fire"]  # Benötigt alle anderen Effekte
    }
}

# Nach den anderen globalen Variablen
current_particle_effect = "default"
unlocked_particles = {"default": True}

# Nach den PARTICLE_EFFECTS Definitionen, vor der add_coins Funktion
def can_unlock_particle(effect_name):
    if effect_name == "default":
        return True
        
    effect = PARTICLE_EFFECTS[effect_name]
    if "requires" not in effect:
        return True
        
    # Prüfe alle Voraussetzungen
    for req in effect["requires"]:
        if req in BIRD_SKINS and req not in unlocked_birds:
            return False
        if req in BACKGROUND_SKINS and req not in unlocked_backgrounds:
            return False
        if req in PARTICLE_EFFECTS and req not in unlocked_particles:
            return False
    return True

def add_coins(amount):
    global player_coins
    player_coins += amount
    save_player_data()

def get_save_path():
    """Erstellt und gibt den Pfad zum Speichern der Spielerdaten zurück"""
    # Erstelle einen spezifischen Ordner für das Spiel
    save_dir = os.path.join(os.getenv('APPDATA'), 'FlapOfDoom')
    
    # Erstelle den Ordner, falls er nicht existiert
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    return os.path.join(save_dir, 'player_data.json')

def save_player_data():
    data = {
        "coins": player_coins,
        "unlocked_birds": unlocked_birds,
        "current_bird": current_bird,
        "unlocked_backgrounds": unlocked_backgrounds,
        "current_background": current_background,
        "unlocked_particles": unlocked_particles,
        "current_particle_effect": current_particle_effect
    }
    save_path = get_save_path()
    try:
        with open(save_path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")

def load_player_data():
    global player_coins, unlocked_birds, current_bird, unlocked_backgrounds, current_background, unlocked_particles, current_particle_effect
    save_path = get_save_path()
    try:
        with open(save_path, "r") as f:
            data = json.load(f)
            player_coins = data.get("coins", 0)
            unlocked_birds = data.get("unlocked_birds", {"default": True})
            current_bird = data.get("current_bird", "default")
            unlocked_backgrounds = data.get("unlocked_backgrounds", {"day": True})
            current_background = data.get("current_background", "day")
            unlocked_particles = data.get("unlocked_particles", {"default": True})
            current_particle_effect = data.get("current_particle_effect", "default")
    except:
        player_coins = 0
        unlocked_birds = {"default": True}
        current_bird = "default"
        unlocked_backgrounds = {"day": True}
        current_background = "day"
        unlocked_particles = {"default": True}
        current_particle_effect = "default"

# Lade gespeicherte Spielerdaten
load_player_data()

# Dann erst pygame initialisieren
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Lade und setze das Programm-Icon
try:
    # Lade das Icon-Bild
    program_icon = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'Middle.png')))
    # Setze das Fenster-Icon
    pygame.display.set_icon(program_icon)
except Exception as e:
    print(f"Fehler beim Laden des Programm-Icons: {e}")

# Initialisiere Schriftarten
score_font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 70)
menu_font = pygame.font.Font(None, 48)
input_font = pygame.font.Font(None, 32)

# Erstelle Bildschirm
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('FlapOfDoom')

# Nach pygame.display.set_mode() und vor pygame.display.set_caption()
try:
    # Hole das Fenster-Handle
    hwnd = pygame.display.get_wm_info()['window']
    # Lade das Icon als Windows-Icon
    icon_path = get_resource_path(os.path.join('assets', 'sprites', 'Middle.png'))
    icon_handle = ctypes.windll.user32.LoadImageW(
        None,
        icon_path,
        1,  # IMAGE_ICON
        0,
        0,
        0x00000010 | 0x00000040  # LR_LOADFROMFILE | LR_DEFAULTSIZE
    )
    # Setze das Taskbar-Icon
    ctypes.windll.user32.SendMessageW(
        hwnd,
        0x0080,  # WM_SETICON
        1,  # ICON_BIG
        icon_handle
    )
except:
    print("Taskbar-Icon konnte nicht gesetzt werden")

if sys.version_info < (3, 6):
    print("Dieses Spiel benötigt Python 3.6 oder höher")
    sys.exit(1)

# Konami Code Definitionen
KONAMI_CODE = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a]
konami_index = 0
easter_egg_unlocked = False

def check_konami_code(event):
    global konami_index, easter_egg_unlocked
    if event.type == KEYDOWN:
        if event.key == KONAMI_CODE[konami_index]:
            konami_index += 1
            if konami_index == len(KONAMI_CODE):
                easter_egg_unlocked = True
                konami_index = 0
                # Easter Egg Effekt
                point_sound.play()
                # Gib dem Spieler 1000 Münzen
                add_coins(1000)
        else:
            konami_index = 0

def show_menu():
    global player_coins
    menu_active = True
    
    while menu_active:
        screen.blit(BACKGROUND_NIGHT, (0, 0))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # Ersetze den Text-Titel mit dem Logo
        logo_rect = LOGO_IMAGE.get_rect()
        logo_rect.centerx = SCREEN_WIDTH // 2
        logo_rect.top = SCREEN_HEIGHT // 4
        screen.blit(LOGO_IMAGE, logo_rect)
        
        # Menü-Optionen mit Glaseffekt-Hintergrund
        options = [
            ("Spielen (SPACE)", K_SPACE),
            ("Shop (S)", K_s),
            ("Über uns (A)", K_a),
            ("Beenden (Q)", K_q)
        ]
        
        # Menü-Optionen
        button_rects = []
        for i, (text, key) in enumerate(options):
            button_bg = pygame.Surface((300, 50), pygame.SRCALPHA)
            button_rect = button_bg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60))
            
            # Hover-Effekt
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(button_bg, (255, 255, 255, 80), button_bg.get_rect(), border_radius=25)
            else:
                pygame.draw.rect(button_bg, (255, 255, 255, 50), button_bg.get_rect(), border_radius=25)
            
            screen.blit(button_bg, button_rect)
            
            text_surface = menu_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
            
            button_rects.append((button_rect, key))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                check_konami_code(event)
                if event.key == K_SPACE:
                    return "play"
                elif event.key == K_s:
                    show_shop()
                elif event.key == K_a:
                    show_error_message()
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for rect, key in button_rects:
                    if rect.collidepoint(event.pos):
                        if key == K_SPACE:
                            return "play"
                        elif key == K_s:
                            show_shop()
                        elif key == K_a:
                            show_error_message()
                        elif key == K_q:
                            pygame.quit()
                            sys.exit()

def show_error_message():
    start_time = time.time()
    error_font = pygame.font.Font(None, 36)
    error_text = error_font.render("Error 404 - Class not Found", True, (255, 0, 0))
    error_rect = error_text.get_rect()
    
    # Zentriere horizontal, aber behalte die vertikale Position am unteren Rand
    error_rect.centerx = SCREEN_WIDTH // 2
    error_rect.bottom = SCREEN_HEIGHT - 10
    
    while time.time() - start_time < 2:  # Zeige Nachricht für 2 Sekunden
        screen.blit(error_text, error_rect)
        pygame.display.update()
        clock.tick(60)

def show_about():
    # Video-Pfad
    video_path = get_resource_path(os.path.join('assets', 'video', 'about.mp4'))
    
    # Öffne das Video im Vollbildmodus
    try:
        # Verwende den Parameter "new=0" um im aktuellen Fenster zu öffnen
        # und "autoraise=True" um das Fenster in den Vordergrund zu bringen
        webbrowser.open(video_path, new=0, autoraise=True)
    except Exception as e:
        print(f"Fehler beim Öffnen des Videos: {e}")
    
    # Kehre sofort zum Hauptmenü zurück
    return

def load_number_images():
    numbers = {}
    for i in range(10):
        img = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', f'{i}.png'))).convert_alpha()
        numbers[str(i)] = pygame.transform.scale(img, (24, 36))  # Größe der Zahlen anpassen
    return numbers

# Nach dem Laden der anderen Bilder (vor der Game Loop)
NUMBER_IMAGES = load_number_images()

def show_score():
    if not show_game_over.is_game_over:  # Prüfe ob Game Over aktiv ist
        # Position für den Score festlegen
        score_y = 50
        
        # Score mit Zahlenbildern zeichnen
        score_str = str(score)
        spacing = 2  # Abstand zwischen den Zahlen
        number_width = 24  # Breite jeder Zahl
        total_width = len(score_str) * (number_width + spacing) - spacing
        start_x = SCREEN_WIDTH//2 - total_width//2
        
        for i, digit in enumerate(score_str):
            img = NUMBER_IMAGES[digit]
            screen.blit(img, (start_x + i * (number_width + spacing), score_y))

def draw_number_score(x, y, score_str):
    spacing = 2  # Abstand zwischen den Zahlen
    total_width = len(score_str) * (24 + spacing)  # Gesamtbreite des Scores
    start_x = x - total_width // 2  # Zentriere den Score
    
    for i, digit in enumerate(score_str):
        img = NUMBER_IMAGES[digit]
        screen.blit(img, (start_x + i * (24 + spacing), y))

def show_game_over():
    show_game_over.is_game_over = True  # Markiere Game Over als aktiv
    
    # Game Over Image laden
    game_over_image = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'gameover.png'))).convert_alpha()
    
    # Mittige Positionierung des Game Over Images
    game_over_rect = game_over_image.get_rect()
    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    screen.blit(game_over_image, game_over_rect)
    
    # Score mit Zahlenbildern
    draw_number_score(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, str(score))
    
    pygame.display.update()
    
    # Warte auf Tastendruck
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting = False
                    show_game_over.is_game_over = False  # Reset Game Over Status
                    if score >= 10:
                        get_player_name()
                    return
                else:
                    waiting = False
                    show_game_over.is_game_over = False  # Reset Game Over Status
                    return

# Initialisiere die Game Over Status Variable
show_game_over.is_game_over = False

def get_player_name():
    name = ""
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    input_active = False
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        
        screen.fill(BLACK)
        input_text = input_font.render("Bitte gib deinen Namen ein:", True, WHITE)
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(input_text, input_rect)
        
        input_surface = input_font.render(name, True, WHITE)
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(input_surface, input_rect)
        
        pygame.display.update()
        
    save_score(name)

def save_score(name):
    try:
        # Aktuelles Datum hinzufügen
        current_date = time.strftime("%d.%m.%Y")
        
        # Erstelle ein JSON-Objekt mit den Spielerdaten
        score_data = {
            'name': name,
            'score': score,
            'date': current_date
        }
        
        # Sende die Daten an den Server
        try:
            import requests
            
            # Sende POST-Anfrage an den Server
            response = requests.post('https://api.magrora.de/json', json=score_data)
            
            # Überprüfe, ob die Anfrage erfolgreich war
            if response.status_code == 200:
                print("Score erfolgreich an Server gesendet!")
                
                # Öffne die Highscores-Seite im Browser
                webbrowser.open('https://api.magrora.de/flapofdoom')
            else:
                print(f"Fehler beim Senden des Scores: {response.status_code}")
                
        except Exception as e:
            print(f"Fehler bei der Server-Kommunikation: {e}")
            
            # Fallback: Speichere lokal in JSON-Datei
            try:
                with open('highscores.json', 'r') as f:
                    high_scores = json.load(f)
            except:
                high_scores = []
            
            high_scores.append(score_data)
            high_scores.sort(key=lambda x: x['score'], reverse=True)
            
            with open('highscores.json', 'w') as f:
                json.dump(high_scores, f)
            
            # Erstelle HTML-Datei für die Anzeige
            create_highscore_html()
            
            # Öffne die HTML-Datei
            webbrowser.open('highscores.html')
            
    except Exception as e:
        print(f"Fehler beim Speichern des Scores: {e}")

# Lade Audio - Ändern von pygame.mixer.music zu pygame.mixer.Sound für bessere Performance
wing_sound = pygame.mixer.Sound(get_resource_path(os.path.join('assets', 'audio', 'wing.wav')))
hit_sound = pygame.mixer.Sound(get_resource_path(os.path.join('assets', 'audio', 'hit.wav')))
point_sound = pygame.mixer.Sound(get_resource_path(os.path.join('assets', 'audio', 'point.wav')))  # Separate Sounddatei

# Lade Bilder (nach den Sound-Definitionen)
BACKGROUND_DAY = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'background-day.png')))
BACKGROUND_NIGHT = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'background-night.png')))
BACKGROUND_MIDNIGHT = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'background-midnight.png')))

# Skaliere alle Hintergründe
BACKGROUND_DAY = pygame.transform.scale(BACKGROUND_DAY, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_NIGHT = pygame.transform.scale(BACKGROUND_NIGHT, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_MIDNIGHT = pygame.transform.scale(BACKGROUND_MIDNIGHT, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Nach dem Laden von BACKGROUND_DAY und BACKGROUND_NIGHT, füge hinzu:
BEGIN_IMAGE = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'message.png'))).convert_alpha()
# Skaliere auf 60% der Bildschirmbreite und behalte das Seitenverhältnis bei
original_size = BEGIN_IMAGE.get_size()
scale_factor = (SCREEN_WIDTH * 0.6) / original_size[0]
new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
BEGIN_IMAGE = pygame.transform.scale(BEGIN_IMAGE, new_size)

# Nach den anderen Bild-Ladebefehlen, füge hinzu:
LOGO_IMAGE = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'logo.png'))).convert_alpha()
# Skaliere das Logo auf eine angemessene Größe (passen Sie die Größe nach Bedarf an)
LOGO_IMAGE = pygame.transform.scale(LOGO_IMAGE, (300, 100))  # Anpassen der Größe nach Bedarf

# Definiere BIRD_SKINS
BIRD_SKINS = {
    "default": {
        "price": 0,
        "files": ["down.png", "Middle.png", "up.png"],
        "description": "Standard Vogel"
    },
    "blue": {
        "price": 215,
        "files": ["bluebird-downflap.png", "bluebird-midflap.png", "bluebird-upflap.png"],
        "description": "Eiskalter Flieger"
    },
    "red": {
        "price": 390,
        "files": ["redbird-downflap.png", "redbird-midflap.png", "redbird-upflap.png"],
        "description": "Feuriger Phönix"
    },
    "yellow": {
        "price": 560,
        "files": ["yellowbird-downflap.png", "yellowbird-midflap.png", "yellowbird-upflap.png"],
        "description": "Goldener Blitz"
    }
}

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_skin(current_bird)
        self.speed = SPEED
        self.current_image = 0
        self.animation_timer = 0
        self.animation_speed = 5  # Niedrigere Werte = schnellere Animation
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2
    
    def load_skin(self, skin_name):
        skin = BIRD_SKINS[skin_name]
        self.images = []
        for file in skin["files"]:
            img = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', file))).convert_alpha()
            # Skaliere das Bild auf eine einheitliche Größe
            img = pygame.transform.scale(img, (40, 30))  # Anpassen der Größe nach Bedarf
            self.images.append(img)

    def update(self):
        # Animation basierend auf Timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image]
        
        # Bewegung und Physik
        self.speed += GRAVITY
        self.rect[1] += self.speed
        
        # Verhindere, dass der Vogel über den oberen Bildschirmrand fliegt
        if self.rect[1] < 0:
            self.rect[1] = 0
            self.speed = 0  # Stoppe die Aufwärtsbewegung
        
        # Rotiere den Vogel basierend auf der Geschwindigkeit
        angle = -self.speed * 2  # Negative Geschwindigkeit = nach oben schauen
        angle = max(-30, min(angle, 45))  # Begrenze den Winkel zwischen -30 und 45 Grad
        self.image = pygame.transform.rotate(self.images[self.current_image], angle)
        self.mask = pygame.mask.from_surface(self.image)

    def bump(self):
        self.speed = -SPEED
        self.current_image = 0  # Reset Animation beim Springen

    def begin(self):
        # Sanftere Animation im Startbildschirm
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * 2:  # Langsamere Animation im Menü
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image]

    def emit_particles(self):
        if current_particle_effect in unlocked_particles and self.speed > 0:  # Nur bei Fallbewegung
            effect = PARTICLE_EFFECTS[current_particle_effect]
            if effect["max_particles"] > 0:  # Nur wenn Partikel aktiviert sind
                particle_system.emit(
                    self.rect.centerx,
                    self.rect.centery + 15,  # Etwas nach unten versetzt
                    amount=effect["max_particles"] // 2,  # Halbierte Partikelmenge
                    effect_type=current_particle_effect
                )

# Erstelle Sprite-Gruppen
bird_group = pygame.sprite.Group()
bird = Bird()  # Jetzt wird current_bird korrekt erkannt
bird_group.add(bird)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'pipe-green.png'))).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'base.png'))).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
pipe_pairs = []
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    pipe_pairs.append({"upper": pipes[0], "lower": pipes[1], "scored": False})

# Spiel-Loop
clock = pygame.time.Clock()

def show_shop():
    global player_coins, current_bird, unlocked_birds, current_background, unlocked_backgrounds, current_particle_effect, unlocked_particles
    shopping = True
    selected_item = 0
    current_category = "birds"  # "birds", "backgrounds" oder "particles"
    scroll_offset = 0
    
    bird_items = list(BIRD_SKINS.keys())
    background_items = list(BACKGROUND_SKINS.keys())
    particle_items = list(PARTICLE_EFFECTS.keys())
    
    # Lade Icons
    try:
        lock_icon = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'lock.png'))).convert_alpha()
        unlock_icon = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'unlock.png'))).convert_alpha()
        selected_icon = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'selected.png'))).convert_alpha()
        coin_icon = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', 'coin.png'))).convert_alpha()
        
        # Skaliere Icons
        icon_size = (24, 24)
        lock_icon = pygame.transform.scale(lock_icon, icon_size)
        unlock_icon = pygame.transform.scale(unlock_icon, icon_size)
        selected_icon = pygame.transform.scale(selected_icon, icon_size)
        coin_icon = pygame.transform.scale(coin_icon, icon_size)
        icons_loaded = True
    except:
        icons_loaded = False
    
    # Angepasste Konstanten für besseres Layout
    ITEM_HEIGHT = 80
    PADDING = 10
    TITLE_HEIGHT = 40
    HEADER_HEIGHT = 100
    CATEGORY_HEIGHT = 40
    list_start_y = HEADER_HEIGHT + CATEGORY_HEIGHT + 10
    
    # Erstelle die Texte für die Buttons
    category_font = pygame.font.Font(None, 36)
    vogel_text = category_font.render("Vögel", True, WHITE)
    hintergrund_text = category_font.render("Hintergründe", True, WHITE)
    partikel_text = category_font.render("Partikel", True, WHITE)
    
    # Berechne die Buttonbreiten
    button_padding = 20  # Reduziere den Padding-Wert von 40 auf 20
    vogel_width = vogel_text.get_width() + button_padding
    hintergrund_width = hintergrund_text.get_width() + button_padding
    partikel_width = partikel_text.get_width() + button_padding
    
    # Zentriere die Buttons mit kleinerem Abstand
    total_width = vogel_width + hintergrund_width + partikel_width + 20  # Reduziere den Abstand zwischen Buttons von 40 auf 20
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    # Aktualisiere die Button-Rechtecke mit kleineren Abständen
    category_buttons = [
        pygame.Rect(start_x, HEADER_HEIGHT + 5, vogel_width, 40),
        pygame.Rect(start_x + vogel_width + 10, HEADER_HEIGHT + 5, hintergrund_width, 40),  # Reduziere den Abstand von 20 auf 10
        pygame.Rect(start_x + vogel_width + hintergrund_width + 20, HEADER_HEIGHT + 5, partikel_width, 40)  # Reduziere den Abstand von 40 auf 20
    ]
    
    while shopping:
        clock.tick(30)
        
        screen.blit(BACKGROUND_DAY if current_background == "day" else BACKGROUND_NIGHT, (0, 0))
        
        # Einheitliche Transparenz für den Hauptoverlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        screen.blit(overlay, (0, 0))
        
        # Shop Titel - verschiebe nach unten
        title = game_over_font.render("SHOP", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))  # Von 10 auf 40 geändert
        
        # Münzen-Anzeige - verschiebe in die obere linke Ecke
        coins_pos = (20, 20)  # Neue Position: 20 Pixel von links, 20 Pixel von oben
        if icons_loaded:
            screen.blit(coin_icon, (coins_pos[0], coins_pos[1]))
            coins_text = menu_font.render(str(player_coins), True, WHITE)
            screen.blit(coins_text, (coins_pos[0] + 30, coins_pos[1]))
        else:
            coins_text = menu_font.render(f"💰 {player_coins}", True, WHITE)
            screen.blit(coins_text, coins_pos)
        
        # Zeichne Kategorie-Buttons
        for i, (rect, text) in enumerate([
            (category_buttons[0], "Vögel"),
            (category_buttons[1], "Hintergründe"),
            (category_buttons[2], "Partikel")
        ]):
            text_surf = category_font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
        
        # Zeige Items basierend auf der aktuellen Kategorie
        items = bird_items if current_category == "birds" else (background_items if current_category == "backgrounds" else particle_items)
        skins = BIRD_SKINS if current_category == "birds" else (BACKGROUND_SKINS if current_category == "backgrounds" else PARTICLE_EFFECTS)
        
        # Item-Liste mit einheitlicher Transparenz
        button_rects = []
        
        for i, item_name in enumerate(items):
            y_pos = list_start_y + (i * (ITEM_HEIGHT + 5))
            
            item_bg = pygame.Surface((SCREEN_WIDTH - 20, ITEM_HEIGHT), pygame.SRCALPHA)
            if i == selected_item:
                pygame.draw.rect(item_bg, (255, 255, 255, 120), item_bg.get_rect(), border_radius=10)
            else:
                pygame.draw.rect(item_bg, (255, 255, 255, 80), item_bg.get_rect(), border_radius=10)
            
            item_rect = item_bg.get_rect(topleft=(10, y_pos))
            screen.blit(item_bg, item_rect)
            button_rects.append((item_rect, i))
            
            # Vorschau und Text
            if current_category == "birds":
                preview_img = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', skins[item_name]["files"][1])))
                preview_img = pygame.transform.scale(preview_img, (50, 50))
                screen.blit(preview_img, (20, y_pos + 15))
                text_x = 80
            elif current_category == "backgrounds":
                preview_img = pygame.image.load(get_resource_path(os.path.join('assets', 'sprites', skins[item_name]["files"][0])))
                preview_img = pygame.transform.scale(preview_img, (80, 50))
                screen.blit(preview_img, (20, y_pos + 15))
                text_x = 110
            else:  # Partikel
                # Zeichne einen farbigen Kreis als Vorschau
                color = PARTICLE_COLORS[skins[item_name]["color"]]
                preview_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(preview_surface, (*color, 200), (25, 25), 20)
                screen.blit(preview_surface, (20, y_pos + 15))
                text_x = 80
            
            name_text = menu_font.render(item_name.capitalize(), True, BLACK)
            screen.blit(name_text, (text_x, y_pos + 10))
            
            # Status/Preis
            unlocked = (current_category == "birds" and item_name in unlocked_birds) or \
                      (current_category == "backgrounds" and item_name in unlocked_backgrounds) or \
                      (current_category == "particles" and item_name in unlocked_particles)
            
            is_selected = (current_category == "birds" and item_name == current_bird) or \
                         (current_category == "backgrounds" and item_name == current_background) or \
                         (current_category == "particles" and item_name == current_particle_effect)
            
            if unlocked:
                if is_selected:
                    if icons_loaded:
                        screen.blit(selected_icon, (text_x, y_pos + 45))
                        status_text = menu_font.render("Ausgewählt", True, (0, 100, 0))
                        screen.blit(status_text, (text_x + 30, y_pos + 45))
                    else:
                        status_text = menu_font.render("✓ Ausgewählt", True, (0, 100, 0))
                        screen.blit(status_text, (text_x, y_pos + 45))
                else:
                    if icons_loaded:
                        screen.blit(unlock_icon, (text_x, y_pos + 45))
                        status_text = menu_font.render("Verfügbar", True, (0, 100, 200))
                        screen.blit(status_text, (text_x + 30, y_pos + 45))
                    else:
                        status_text = menu_font.render("⭐ Verfügbar", True, (0, 100, 200))
                        screen.blit(status_text, (text_x, y_pos + 45))
            else:
                if icons_loaded:
                    screen.blit(lock_icon, (text_x, y_pos + 45))
                    screen.blit(coin_icon, (text_x + 30, y_pos + 45))
                    price_text = menu_font.render(str(skins[item_name]["price"]), True, (200, 150, 0))
                    screen.blit(price_text, (text_x + 60, y_pos + 45))
                else:
                    status_text = menu_font.render(f"🔒 {skins[item_name]['price']} 💰", True, (200, 150, 0))
                    screen.blit(status_text, (text_x, y_pos + 45))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    shopping = False
                elif event.key == K_UP:
                    selected_item = (selected_item - 1) % len(items)
                elif event.key == K_DOWN:
                    selected_item = (selected_item + 1) % len(items)
                elif event.key == K_RETURN:
                    selected_item_name = items[selected_item]
                    if current_category == "birds":
                        if selected_item_name in unlocked_birds:
                            current_bird = selected_item_name
                            point_sound.play()
                            save_player_data()
                        elif player_coins >= BIRD_SKINS[selected_item_name]["price"]:
                            player_coins -= BIRD_SKINS[selected_item_name]["price"]
                            unlocked_birds[selected_item_name] = True
                            current_bird = selected_item_name
                            point_sound.play()
                            save_player_data()
                        else:
                            hit_sound.play()
                    elif current_category == "backgrounds":
                        if selected_item_name in unlocked_backgrounds:
                            current_background = selected_item_name
                            point_sound.play()
                            save_player_data()
                        elif player_coins >= BACKGROUND_SKINS[selected_item_name]["price"]:
                            player_coins -= BACKGROUND_SKINS[selected_item_name]["price"]
                            unlocked_backgrounds[selected_item_name] = True
                            current_background = selected_item_name
                            point_sound.play()
                            save_player_data()
                        else:
                            hit_sound.play()
                    else:  # particles
                        if selected_item_name in unlocked_particles:
                            current_particle_effect = selected_item_name
                            point_sound.play()
                            save_player_data()
                        elif (player_coins >= PARTICLE_EFFECTS[selected_item_name]["price"] and 
                              can_unlock_particle(selected_item_name)):
                            player_coins -= PARTICLE_EFFECTS[selected_item_name]["price"]
                            unlocked_particles[selected_item_name] = True
                            current_particle_effect = selected_item_name
                            point_sound.play()
                            save_player_data()
                        else:
                            hit_sound.play()
            if event.type == MOUSEBUTTONDOWN:
                if category_buttons[0].collidepoint(event.pos):
                    current_category = "birds"
                    selected_item = 0
                elif category_buttons[1].collidepoint(event.pos):
                    current_category = "backgrounds"
                    selected_item = 0
                elif category_buttons[2].collidepoint(event.pos):
                    current_category = "particles"
                    selected_item = 0
                
                # Füge die Klick-Erkennung für Items hinzu
                for rect, idx in button_rects:
                    if rect.collidepoint(event.pos):
                        selected_item = idx
                        selected_item_name = items[selected_item]
                        if current_category == "birds":
                            if selected_item_name in unlocked_birds:
                                current_bird = selected_item_name
                                point_sound.play()
                                save_player_data()
                            elif player_coins >= BIRD_SKINS[selected_item_name]["price"]:
                                player_coins -= BIRD_SKINS[selected_item_name]["price"]
                                unlocked_birds[selected_item_name] = True
                                current_bird = selected_item_name
                                point_sound.play()
                                save_player_data()
                            else:
                                hit_sound.play()
                        elif current_category == "backgrounds":
                            if selected_item_name in unlocked_backgrounds:
                                current_background = selected_item_name
                                point_sound.play()
                                save_player_data()
                            elif player_coins >= BACKGROUND_SKINS[selected_item_name]["price"]:
                                player_coins -= BACKGROUND_SKINS[selected_item_name]["price"]
                                unlocked_backgrounds[selected_item_name] = True
                                current_background = selected_item_name
                                point_sound.play()
                                save_player_data()
                            else:
                                hit_sound.play()
                        else:  # particles
                            if selected_item_name in unlocked_particles:
                                current_particle_effect = selected_item_name
                                point_sound.play()
                                save_player_data()
                            elif (player_coins >= PARTICLE_EFFECTS[selected_item_name]["price"] and 
                                  can_unlock_particle(selected_item_name)):
                                player_coins -= PARTICLE_EFFECTS[selected_item_name]["price"]
                                unlocked_particles[selected_item_name] = True
                                current_particle_effect = selected_item_name
                                point_sound.play()
                                save_player_data()
                            else:
                                hit_sound.play()

def create_highscore_html():
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>FlapOfDoom Highscores</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1e90ff, #70a1ff);
                    margin: 0;
                    padding: 20px;
                    color: white;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                    backdrop-filter: blur(10px);
                }
                h1 {
                    text-align: center;
                    color: white;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    overflow: hidden;
                }
                th, td {
                    padding: 15px;
                    text-align: left;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                }
                th {
                    background: rgba(0, 0, 0, 0.2);
                    font-weight: bold;
                }
                tr:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                .rank {
                    font-weight: bold;
                    color: #ffd700;
                }
                .date {
                    color: #a0a0a0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏆 FlapOfDoom Highscores 🏆</h1>
                <table>
                    <tr>
                        <th>Rang</th>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Datum</th>
                    </tr>
        """
        
        for i, score in enumerate(scores[:10], 1):
            html_content += f"""
                    <tr>
                        <td class="rank">#{i}</td>
                        <td>{score['name']}</td>
                        <td>{score['score']}</td>
                        <td class="date">{score['date']}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        with open('highscores.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"Fehler beim Erstellen der HTML-Datei: {e}")

# Füge diese neue Funktion für den Pause-Screen hinzu
def show_pause():
    paused = True
    
    # Kleinere Schriftart für die Buttons
    pause_button_font = pygame.font.Font(None, 36)  # Kleinere Schriftgröße für Buttons
    
    # Erstelle Buttons
    buttons = [
        ("Weiterspielen (ESC)", K_ESCAPE),
        ("Hauptmenü (M)", K_m)
    ]
    
    button_rects = []
    
    while paused:
        screen.blit(BACKGROUND_DAY, (0, 0))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Ersetze den Pause-Text mit dem Logo
        logo_rect = LOGO_IMAGE.get_rect()
        logo_rect.centerx = SCREEN_WIDTH // 2
        logo_rect.top = SCREEN_HEIGHT // 3 - 50  # Etwas höher als der ursprüngliche Text
        screen.blit(LOGO_IMAGE, logo_rect)
        
        # Zeichne Buttons
        button_rects.clear()  # Liste leeren für neue Buttons
        for i, (text, key) in enumerate(buttons):
            # Kleinere Button-Größe
            button_bg = pygame.Surface((250, 40), pygame.SRCALPHA)
            button_rect = button_bg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 50))
            
            # Hover-Effekt
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(button_bg, (255, 255, 255, 80), button_bg.get_rect(), border_radius=20)
            else:
                pygame.draw.rect(button_bg, (255, 255, 255, 50), button_bg.get_rect(), border_radius=20)
            
            screen.blit(button_bg, button_rect)
            
            # Kleinerer Text
            text_surface = pause_button_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
            
            button_rects.append((button_rect, key))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "continue"
                elif event.key == K_m:
                    return "menu"
            if event.type == MOUSEBUTTONDOWN:
                for rect, key in button_rects:
                    if rect.collidepoint(event.pos):
                        if key == K_ESCAPE:
                            return "continue"
                        elif key == K_m:
                            return "menu"

def get_current_background():
    if current_background == "day":
        return BACKGROUND_DAY
    elif current_background == "night":
        return BACKGROUND_NIGHT
    elif current_background == "midnight":
        return BACKGROUND_MIDNIGHT
    return BACKGROUND_DAY  # Fallback zum Tag-Hintergrund

class Particle:
    def __init__(self, x, y, effect_type="default"):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.color = PARTICLE_COLORS[PARTICLE_EFFECTS[effect_type]["color"]]
        self.size = randint(2, 4)
        self.life = 1.0  # Lebensdauer des Partikels (1.0 = voll, 0.0 = tot)
        self.decay_rate = uniform(0.02, 0.05)  # Wie schnell der Partikel verschwindet
        
        # Zufällige Bewegungsrichtung
        angle = uniform(0, 2 * math.pi)
        speed = uniform(1, 3)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= self.decay_rate
        self.size = max(0, self.size - 0.1)
        return self.life > 0

    def draw(self, screen):
        if self.life > 0:
            alpha = int(self.life * 255)
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                (*self.color, alpha),
                (self.size, self.size),
                self.size
            )
            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, amount=10, effect_type="default"):
        for _ in range(amount):
            self.particles.append(Particle(x, y, effect_type))
            
    def update_and_draw(self, screen):
        self.particles = [p for p in self.particles if p.update()]
        for particle in self.particles:
            particle.draw(screen)

# Füge diese Zeilen nach der Bird-Klasse hinzu
particle_system = ParticleSystem()

# Haupt-Spiel-Loop
while True:
    # Zeige Hauptmenü
    menu_choice = show_menu()
    
    # Reset Spiel-Variablen
    score = 0
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)
    
    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDHT * i)
        ground_group.add(ground)
    
    pipe_group = pygame.sprite.Group()
    pipe_pairs = []
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        pipe_pairs.append({"upper": pipes[0], "lower": pipes[1], "scored": False})


    # Start-Bildschirm
    begin = True
    while begin:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    wing_sound.play()
                    begin = False
            # Füge Mausklick-Erkennung hinzu
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    bird.bump()
                    wing_sound.play()
                    begin = False
        
        screen.blit(get_current_background(), (0, 0))
        
        # Mittige Positionierung des BEGIN_IMAGE
        begin_rect = BEGIN_IMAGE.get_rect()
        begin_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(BEGIN_IMAGE, begin_rect)
    
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)
    
        bird.begin()
        ground_group.update()
        bird_group.draw(screen)
        ground_group.draw(screen)
        pygame.display.update()

    # Spiel-Loop
    playing = True
    while playing:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    wing_sound.play()
                elif event.key == K_ESCAPE:
                    # Pause-Screen anzeigen
                    pause_action = show_pause()
                    if pause_action == "menu":
                        playing = False
                        break
                    # Bei "continue" wird einfach weitergespielt
            # Füge Mausklick-Erkennung hinzu
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    bird.bump()
                    wing_sound.play()

        screen.blit(get_current_background(), (0, 0))
    
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            removed_pair = pipe_pairs.pop(0)  # Entferne das erste Paar aus der Liste
            pipe_group.remove(removed_pair["upper"])
            pipe_group.remove(removed_pair["lower"])
            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
            pipe_pairs.append({"upper": pipes[0], "lower": pipes[1], "scored": False})

        bird_center_x = bird.rect.centerx
        for pair in pipe_pairs:
            pipe = pair["upper"]
            if not pair["scored"] and bird_center_x > pipe.rect.centerx:
                pair["scored"] = True
                score += 1
                add_coins(COIN_REWARD)  # Füge Münzen hinzu
                point_sound.play()
        bird_group.update()
        ground_group.update()
        pipe_group.update()
    
        # Partikeleffekte
        particle_system.update_and_draw(screen)
        if playing:  # Nur während des aktiven Spiels Partikel emittieren
            bird.emit_particles()
    
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        
        show_score()
        pygame.display.update()
    
        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            hit_sound.play()
            
            show_game_over()
            break
