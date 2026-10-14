# ============================================================
# core/importer.py - Import with rotation_z support
# Protocol 4.2.0
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
    for root, dirs, files in os.walk(fmt_path):
        for f in files:
            if f.lower() == model_name.lower() + ext:
                return os.path.join(root, f)
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
    for root, dirs, files in os.walk(fmt_path):
        for f in files:
            if f.lower().endswith(ext):
                models.append(os.path.splitext(f)[0])
    return sorted(models)


def import_into_scene(kit_name, model_name, pos_xz=(0, 0), scale=1.0,
                      rotation_z=0.0, prefer_format="OBJ"):
    """Import model with position, scale, rotation.
    
    pos_xz = [X, Z] in Blender horizontal plane.
    rotation_z = degrees around vertical axis (Blender Z, Roblox Y).
    Height (Blender Z) is always 0 (on ground).
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

    # Join into one
    bpy.ops.object.select_all(action='DESELECT')
    for o in new_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new_objs[0]
    if len(new_objs) > 1:
        bpy.ops.object.join()
    root = bpy.context.view_layer.objects.active
    root.name = model_name

    # 1. Apply scale
    if scale != 1.0:
        root.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

    # 2. Apply rotation (around vertical Z)
    if rotation_z != 0.0:
        root.rotation_euler = (0, 0, math.radians(rotation_z))
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=False)

    # 3. Freeze location
    bpy.ops.object.transform_apply(
        location=True, rotation=False, scale=False)

    bpy.context.view_layer.update()

    # 4. Snap to ground (min_z = 0)
    bbox_world = [root.matrix_world @ Vector(c) for c in root.bound_box]
    min_z = min(v.z for v in bbox_world)
    root.location.z -= min_z
    bpy.context.view_layer.update()

    # 5. Freeze
    bpy.ops.object.transform_apply(
        location=True, rotation=False, scale=False)

    # 6. Move to absolute pos
    root.location = (pos_xz[0], pos_xz[1], 0.0)
    bpy.context.view_layer.update()

    return root
