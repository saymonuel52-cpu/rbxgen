# ============================================================
# core/importer.py - CLEAN FIX
# Protocol 4.2.0 | Always apply all transforms
# ============================================================
import bpy
import os
import math
from mathutils import Vector

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")


def _all_object_names():
    return set(bpy.data.objects.keys())


def import_model(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".obj":
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=filepath)
        else:
            bpy.ops.import_scene.obj(filepath=filepath)
    elif ext in (".gltf", ".glb"):
        bpy.ops.import_scene.gltf(filepath=filepath)
    return True


def get_model_path(kit_name, model_name, prefer_format="OBJ"):
    kit_dir = os.path.join(CACHE_DIR, kit_name)
    if not os.path.exists(kit_dir):
        return None
    fmt_map = {
        "GLTF": ("GLTF format", ".gltf"),
        "GLB":  ("GLTF format", ".glb"),
        "OBJ":  ("OBJ format", ".obj"),
    }
    if prefer_format not in fmt_map:
        return None
    fmt_dir, ext = fmt_map[prefer_format]
    fmt_path = os.path.join(kit_dir, "Models", fmt_dir)
    if not os.path.exists(fmt_path):
        return None
    for root_dir, dirs, files in os.walk(fmt_path):
        for f in files:
            if f.lower() == model_name.lower() + ext:
                return os.path.join(root_dir, f)
    return None


def list_models(kit_name, format_filter="OBJ"):
    kit_dir = os.path.join(CACHE_DIR, kit_name)
    if not os.path.exists(kit_dir):
        return []
    fmt_map = {
        "GLTF": ("GLTF format", ".gltf"),
        "GLB":  ("GLTF format", ".glb"),
        "OBJ":  ("OBJ format", ".obj"),
    }
    if format_filter not in fmt_map:
        return []
    fmt_dir, ext = fmt_map[format_filter]
    fmt_path = os.path.join(kit_dir, "Models", fmt_dir)
    if not os.path.exists(fmt_path):
        return []
    models = []
    for root_dir, dirs, files in os.walk(fmt_path):
        for f in files:
            if f.lower().endswith(ext):
                models.append(os.path.splitext(f)[0])
    return sorted(models)


def import_into_scene(kit_name, model_name, pos_xz=(0, 0), scale=1.0,
                      rotation_z=0.0, prefer_format="OBJ"):
    """Import model.
       Steps:
       1. Import OBJ, join all meshes into one
       2. Apply ALL transforms (freeze from OBJ import)
       3. Apply scale
       4. Apply rotation Z
       5. Snap bottom to Z=0
       6. Move bbox center to pos_xz
    """
    filepath = get_model_path(kit_name, model_name, prefer_format)
    if not filepath:
        print("[ERROR] Model not found: {}".format(model_name))
        return None

    before = _all_object_names()
    import_model(filepath)
    bpy.context.view_layer.update()

    after = _all_object_names()
    new_names = after - before
    new_objs = [bpy.data.objects[n] for n in new_names
                if n in bpy.data.objects and bpy.data.objects[n].type == 'MESH']

    if not new_objs:
        print("[ERROR] No meshes: {}".format(filepath))
        return None

    # 1. Join all meshes
    bpy.ops.object.select_all(action='DESELECT')
    for o in new_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new_objs[0]
    if len(new_objs) > 1:
        bpy.ops.object.join()
    root = bpy.context.view_layer.objects.active
    root.name = model_name

    # 2. FREEZE all transforms from OBJ import (crucial!)
    bpy.ops.object.transform_apply(
        location=True, rotation=True, scale=True)

    bpy.context.view_layer.update()

    # 3. Apply scale (always)
    if scale != 1.0:
        root.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

    # 4. Apply rotation Z (always)
    if rotation_z != 0.0:
        root.rotation_euler = (0, 0, math.radians(rotation_z))
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=False)

    bpy.context.view_layer.update()

    # 5. Snap bottom to Z=0
    bbox_world = [root.matrix_world @ Vector(c) for c in root.bound_box]
    min_z = min(v.z for v in bbox_world)
    root.location.z -= min_z
    bpy.context.view_layer.update()

    # 6. Move bbox center to pos_xz
    bbox_world = [root.matrix_world @ Vector(c) for c in root.bound_box]
    min_x = min(v.x for v in bbox_world)
    max_x = max(v.x for v in bbox_world)
    min_y = min(v.y for v in bbox_world)
    max_y = max(v.y for v in bbox_world)
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    root.location.x += pos_xz[0] - cx
    root.location.y += pos_xz[1] - cy
    bpy.context.view_layer.update()

    return root