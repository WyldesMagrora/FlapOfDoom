from PIL import Image
import os

# Erstelle icons Ordner, falls er nicht existiert
if not os.path.exists('icons'):
    os.makedirs('icons')

# Öffne das PNG-Bild
img = Image.open('assets/sprites/Middle.png')

# Konvertiere zu ICO
img.save('icons/FlapOfDoom.ico', format='ICO') 