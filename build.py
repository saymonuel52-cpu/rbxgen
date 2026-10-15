#!/usr/bin/env python3
# ============================================================
# build.py - CLI for building models from recipes
# Protocol 4.2.0 v2.0
# Usage:
#   blender --background --python build.py -- list
#   blender --background --python build.py -- <recipe_name>
#   blender --background --python build.py -- generator <name> --args
#   blender --background --python build.py -- custom-json '<json>'
#   blender --background --python build.py -- custom-file <path>
# ============================================================
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
from core.recipe import (list_recipes, load_recipe, load_recipe_file,
                          validate_recipe, print_errors)
from core.builder import build_from_recipe, get_all_objects
from core.export import export_fbx
from core.preview import render_preview


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def _get_kit_models():
    """Get {kit_name: [model_names]} for validation."""
    from core.importer import list_models
    from core.downloader import CACHE_DIR
    kits = {}
    if os.path.exists(CACHE_DIR):
        for kit in os.listdir(CACHE_DIR):
            kit_path = os.path.join(CACHE_DIR, kit)
            if os.path.isdir(kit_path):
                models = list_models(kit, "OBJ")
                if models:
                    kits[kit] = models
    return kits


def _write_report(out_dir, name, stats, recipe_path=None,
                   fbx_path=None, previews=None):
    """Write report.json to output dir."""
    os.makedirs(out_dir, exist_ok=True)
    report = {
        "name": name,
        "recipe": recipe_path,
        "objects_count": stats.get("objects_count", 0),
        "kits_used": stats.get("kits_used", []),
        "materials_used": stats.get("materials_used", []),
        "tris": stats.get("tris", 0),
        "fbx": fbx_path,
        "previews": previews or [],
        "warnings": stats.get("warnings", []),
        "errors": stats.get("errors", []),
        "success": len(stats.get("errors", [])) == 0,
    }
    path = os.path.join(out_dir, "report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("[REPORT] " + path)
    return report


def build_and_export(recipe, recipe_path=None):
    """Build, export, preview, report."""
    name = recipe.get("name", "Untitled")

    # Build
    root, objects, stats = build_from_recipe(recipe, verbose=True)

    if not objects:
        print("[ERROR] No objects built")
        return False

    # Output dir
    out_dir = os.path.join(OUTPUT_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    # Export FBX to output/<name>/
    fbx_path = os.path.join(out_dir, name + ".fbx")
    meshes = [o for o in objects if o.type == 'MESH']
    try:
        # Temporarily use local export path
        exported = export_fbx(meshes, name, out_dir=out_dir)
    except Exception as e:
        print("[ERROR] Export: " + str(e))
        exported = None

    # Preview
    previews = []
    try:
        render_preview(name)
        for view in ["top", "front", "side", "iso"]:
            p = os.path.join(os.path.dirname(__file__), "reports",
                             "{}_preview_{}.png".format(name, view))
            if os.path.exists(p):
                previews.append(p)
    except Exception as e:
        print("[WARN] Preview: " + str(e))

    # Report
    report = _write_report(out_dir, name, stats,
                           recipe_path=recipe_path,
                           fbx_path=exported,
                           previews=previews)

    print("")
    print("[DONE] " + name)
    print("  Objects: {}".format(stats["objects_count"]))
    print("  Tris: {}".format(stats["tris"]))
    print("  Output: " + out_dir)
    return True


def cmd_list():
    recipes = list_recipes()
    print("[RECIPES] {} found:".format(len(recipes)))
    for r in recipes:
        print("  " + r)


def cmd_recipe(name):
    recipe, errs = load_recipe(name)
    if errs:
        print("[ERROR] " + errs[0])
        return False
    kit_models = _get_kit_models()
    ok, errors, warns = validate_recipe(recipe, kit_models)
    if not ok:
        print_errors(name, errors)
        return False
    if warns:
        print("[WARN] " + str(warns))
    recipe_path = os.path.join("knowledge", "recipes", name + ".json")
    return build_and_export(recipe, recipe_path)


def cmd_custom_json(json_str):
    try:
        recipe = json.loads(json_str)
    except Exception as e:
        print("[ERROR] JSON parse: " + str(e))
        return False
    kit_models = _get_kit_models()
    ok, errors, warns = validate_recipe(recipe, kit_models)
    if not ok:
        print_errors("custom", errors)
        return False
    return build_and_export(recipe, "custom")


def cmd_custom_file(path):
    recipe, errs = load_recipe_file(path)
    if errs:
        print("[ERROR] " + errs[0])
        return False
    kit_models = _get_kit_models()
    ok, errors, warns = validate_recipe(recipe, kit_models)
    if not ok:
        print_errors(path, errors)
        return False
    return build_and_export(recipe, path)


def main():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    if not argv or argv[0] == "list":
        cmd_list()
        return

    cmd = argv[0]

    if cmd == "custom-json":
        if len(argv) < 2:
            print("[ERROR] custom-json requires JSON string")
            return
        cmd_custom_json(argv[1])
    elif cmd == "custom-file":
        if len(argv) < 2:
            print("[ERROR] custom-file requires path")
            return
        cmd_custom_file(argv[1])
    elif cmd == "generator":
        print("[ERROR] Generators not implemented yet (v2.1)")
    else:
        # Treat as recipe name
        cmd_recipe(cmd)


if __name__ == "__main__":
    main()