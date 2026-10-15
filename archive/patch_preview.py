# Патч preview.py - отключить тени
import sys
path = "core/preview.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "scene.display.shading.show_shadows = True",
    "scene.display.shading.show_shadows = False")
content = content.replace(
    "scene.display.shading.show_cavity = True",
    "scene.display.shading.show_cavity = False")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: shadows disabled in preview")