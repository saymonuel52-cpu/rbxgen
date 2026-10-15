#!/usr/bin/env python3
# ============================================================
# build_map.py - Build map from JSON
# ============================================================
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
from core.scene import clear_scene, setup_units
from core.map_builder import build_map, process_map


def main():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    if not argv:
        print("[ERROR] Usage: build_map.py -- <map.json>")
        return

    map_file = argv[0]
    if not os.path.exists(map_file):
        print("[ERROR] Map file not found: {}".format(map_file))
        return

    with open(map_file, encoding="utf-8-sig") as f:
        spec = json.load(f)

    print("=== BUILDING MAP: {} ===".format(spec.get("name", "unknown")))
    clear_scene()
    setup_units()

    root, objects = build_map(spec)
    if root and objects:
        process_map(root, objects, spec)
        print("")
        print("[DONE] {}".format(spec["name"]))
    else:
        print("[FAILED] No objects built")


if __name__ == "__main__":
    main()