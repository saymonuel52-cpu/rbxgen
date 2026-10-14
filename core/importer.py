# ============================================================
# core/importer.py - Import with proper group handling
# Protocol 4.2.0
# ============================================================
import bpy
import os
from mathutils import Vector

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")


def _get_all_objects():
    """Snapshot of all objects currently in scene."""
    return set(bpy.data.objects.keys())


def import_obj(filepath):
    if not os.path.exists(filepath):
        return []
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(filepath=filepath)
    else:
        bpy.ops.import_scene.obj(filepath=filepath)
    return list(bpy.context.selected_objects)


def import_gltf(filepath):
    if not os.path.exists(filepath):
        return []
    bpy.ops.import_scene.gltf(filepath=filepath)
    return list(bpy.context.selected_objects)


def import_model(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".gltf", ".glb"):
        return import_gltf(filepath)
    elif ext == ".obj":
        return import_obj(filepath)
    return []


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


def snap_to_ground(obj):
    """Move object so its lowest point is at Z=0 (local)."""
    if not obj or obj.type != 'MESH':
        return
    bpy.context.view_layer.update()
    bbox_world = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_z = min(v.z for v in bbox_world)
    if abs(min_z) > 0.001:
        obj.location.z -= min_z


def import_into_scene(kit_name, model_name, pos=(0, 0, 0), scale=1.0,
                      prefer_format="OBJ", snap=True):
    """Import model, snap to ground, move to pos. Returns the imported object."""
    filepath = get_model_path(kit_name, model_name, prefer_format)
    if not filepath:
        print("[ERROR] Model not found: {}".format(model_name))
        return None

    # Snapshot scene before import
    before = _get_all_objects()

    # Import
    import_model(filepath)

    # Find new objects
    after = _get_all_objects()
    new_names = after - before
    new_objs = [bpy.data.objects[n] for n in new_names if n in bpy.data.objects]

    if not new_objs:
        print("[ERROR] No new objects after import: {}".format(filepath))
        return None

    # Find root mesh (first MESH object)
    root = None
    meshes = [o for o in new_objs if o.type == 'MESH']
    if meshes:
        root = meshes[0]
    else:
        root = new_objs[0]

    # Scale
    if scale != 1.0:
        root.scale = (scale, scale, scale)
        bpy.context.view_layer.update()

    # Snap to ground
    if snap:
        snap_to_ground(root)

    # Move to pos
    root.location.x += pos[0]
    root.location.y += pos[1]
    root.location.z += pos[2]

    # Clean up other objects (join children into root if any)
    for o in new_objs:
        if o != root and o.type == 'MESH':
            try:
                bpy.ops.object.select_all(action='DESELECT')
                o.select_set(True)
                root.select_set(True)
                bpy.context.view_layer.objects.active = root
                bpy.ops.object.join()
            except Exception:
                pass

    return root