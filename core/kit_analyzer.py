# ============================================================
# core/kit_analyzer.py - Analyze Kit models
# Protocol 4.2.0 | Run on PC (Blender needed)
# ============================================================
import bpy
import os
import json
from mathutils import Vector

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "kits")


def _all_object_names():
    return set(bpy.data.objects.keys())


def _import_obj(filepath):
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(filepath=filepath)
    else:
        bpy.ops.import_scene.obj(filepath=filepath)


def analyze_model(filepath):
    """Import single model, return dimensions + bbox."""
    before = _all_object_names()
    try:
        _import_obj(filepath)
    except Exception as e:
        return {"error": str(e)}
    bpy.context.view_layer.update()
    after = _all_object_names()
    new_names = after - before
    new_objs = [bpy.data.objects[n] for n in new_names
                if n in bpy.data.objects and bpy.data.objects[n].type == 'MESH']
    if not new_objs:
        return {"error": "no meshes"}
    
    # Combine all meshes
    bpy.ops.object.select_all(action='DESELECT')
    for o in new_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new_objs[0]
    if len(new_objs) > 1:
        bpy.ops.object.join()
    root = bpy.context.view_layer.objects.active
    
    # Apply transforms
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.context.view_layer.update()
    
    dims = root.dimensions
    bbox_world = [root.matrix_world @ Vector(c) for c in root.bound_box]
    min_v = Vector((min(v.x for v in bbox_world),
                    min(v.y for v in bbox_world),
                    min(v.z for v in bbox_world)))
    max_v = Vector((max(v.x for v in bbox_world),
                    max(v.y for v in bbox_world),
                    max(v.z for v in bbox_world)))
    
    # Tris
    tris = sum(len(p.vertices) - 2 for p in root.data.polygons)
    
    # Cleanup
    for o in new_objs:
        if o.name in bpy.data.objects:
            bpy.data.objects.remove(o, do_unlink=True)
    
    return {
        "dimensions": [round(v, 3) for v in dims],
        "bbox_min": [round(v, 3) for v in min_v],
        "bbox_max": [round(v, 3) for v in max_v],
        "tris": tris,
        "center_offset": [round((min_v[i] + max_v[i]) / 2, 3) for i in range(3)],
    }


def analyze_kit(kit_name, format_filter="OBJ"):
    """Analyze all models in a kit."""
    kit_dir = os.path.join(CACHE_DIR, kit_name)
    if not os.path.exists(kit_dir):
        print("[ERROR] Kit not found: " + kit_name)
        return None
    
    if format_filter == "OBJ":
        fmt_dir = "OBJ format"
        ext = ".obj"
    else:
        fmt_dir = "FBX format"
        ext = ".fbx"
    
    fmt_path = os.path.join(kit_dir, "Models", fmt_dir)
    if not os.path.exists(fmt_path):
        print("[ERROR] Format dir not found: " + fmt_path)
        return None
    
    results = {}
    count = 0
    for root_dir, dirs, files in os.walk(fmt_path):
        for f in sorted(files):
            if not f.lower().endswith(ext):
                continue
            name = os.path.splitext(f)[0]
            filepath = os.path.join(root_dir, f)
            info = analyze_model(filepath)
            results[name] = info
            count += 1
            if count % 20 == 0:
                print("[ANALYZED] {}".format(count))
    
    # Save
    os.makedirs(DOCS_DIR, exist_ok=True)
    out_path = os.path.join(DOCS_DIR, kit_name + "_analysis.json")
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(results, fp, indent=2, ensure_ascii=False)
    
    print("[DONE] Analyzed {} models".format(count))
    print("[SAVED] " + out_path)
    return results


def summarize_kit(kit_name):
    """Print summary table for a kit."""
    out_path = os.path.join(DOCS_DIR, kit_name + "_analysis.json")
    if not os.path.exists(out_path):
        print("[ERROR] No analysis. Run analyze_kit() first.")
        return
    with open(out_path, encoding="utf-8") as fp:
        data = json.load(fp)
    
    print("")
    print("=== KIT: {} ===".format(kit_name))
    print("Total models: {}".format(len(data)))
    print("")
    print("{:30s} {:15s} {:10s}".format("Model", "Dimensions", "Tris"))
    print("-" * 60)
    for name in sorted(data.keys())[:50]:
        info = data[name]
        if "error" in info:
            print("{:30s} ERROR: {}".format(name, info["error"]))
            continue
        d = info["dimensions"]
        print("{:30s} ({:.2f},{:.2f},{:.2f})  {}".format(
            name, d[0], d[1], d[2], info["tris"]))
