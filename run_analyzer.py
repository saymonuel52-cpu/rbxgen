# ============================================================
# run_analyzer.py - Analyze a kit (run on PC)
# Usage: blender --background --python run_analyzer.py -- fantasy_town
# ============================================================
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
from core.scene import clear_scene, setup_units
from core.kit_analyzer import analyze_kit, summarize_kit


def main():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    
    kit_name = argv[0] if argv else "fantasy_town"
    
    print("=== ANALYZING KIT: {} ===".format(kit_name))
    clear_scene()
    setup_units()
    
    result = analyze_kit(kit_name, "OBJ")
    if result:
        summarize_kit(kit_name)


if __name__ == "__main__":
    main()
