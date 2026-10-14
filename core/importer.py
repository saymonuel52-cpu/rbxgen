# ============================================================
# core/importer.py - Import with JOIN into single object
# Protocol 4.2.0
# ============================================================
import bpy
import os
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


def import_into_scene(kit_name, model_name, pos=(0, 0, 0), scale=1.0,
                      prefer_format="OBJ", snap=True):
    """Import model -> join all new meshes -> snap -> move. Returns single obj."""
    filepath = get_model_path(kit_name, model_name, prefer_format)
    if not filepath:
        print("[ERROR] Model not found: {}".format(model_name))
        return None

    # 1. Snapshot scene BEFORE
    before = _all_object_names()

    # 2. Import
    import_model(filepath)
    bpy.context.view_layer.update()

    # 3. Find NEW objects
    after = _all_object_names()
    new_names = after - before
    new_objs = [bpy.data.objects[n] for n in new_names
                if n in bpy.data.objects and bpy.data.objects[n].type == 'MESH']

    if not new_objs:
        print("[ERROR] No new meshes: {}".format(filepath))
        return None

    print("[IMPORT] {} -> {} mesh(es)".format(model_name, len(new_objs)))

    # 4. Select new meshes + join
    bpy.ops.object.select_all(action='DESELECT')
    for o in new_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new_objs[0]
    if len(new_objs) > 1:
        bpy.ops.object.join()

    root = bpy.context.view_layer.objects.active
    root.name = model_name

    # 5. Apply scale
    if scale != 1.0:
        root.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

    # 6. Snap to ground
    if snap:
        bpy.context.view_layer.update()
        bbox_world = [root.matrix_world @ Vector(c) for c in root.bound_box]
        min_z = min(v.z for v in bbox_world)
        if abs(min_z) > 0.001:
            root.location.z -= min_z

    # 7. Apply all transforms (freeze)
    bpy.ops.object.transform_apply(
        location=False, rotation=False, scale=True)

    # 8. Move to pos
    root.location.x = pos[0]
    root.location.y = pos[1]
    root.location.z = pos[2]

    return root