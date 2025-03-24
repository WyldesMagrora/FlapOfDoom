import os
import shutil

# Erstelle CD-Ordner
cd_dir = "cd_content"
if not os.path.exists(cd_dir):
    os.makedirs(cd_dir)

# Kopiere alle Dateien aus dist
dist_dir = "dist"
for item in os.listdir(dist_dir):
    s = os.path.join(dist_dir, item)
    d = os.path.join(cd_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

# Kopiere Icon
shutil.copy2("icons/FlapOfDoom.ico", os.path.join(cd_dir, "FlapOfDoom.ico"))

# Erstelle autorun.inf
autorun_content = """[autorun]
open=FlapOfDoom.exe
icon=FlapOfDoom.ico
label=FlapOfDoom
action=FlapOfDoom starten
"""

with open(os.path.join(cd_dir, "autorun.inf"), "w") as f:
    f.write(autorun_content)

print("CD-Inhalt wurde erstellt in:", cd_dir) 