# ============================================================
# core/builder.py - Build scene from recipe
# Protocol 4.2.0 v2.0
# ============================================================
import bpy
import os
import json
from core.importer import import_into_scene
from core.materials import assign as assign_mat
from core.scene import clear_scene, setup_units
from core.recipe import normalize_rotation


def _make_ground(name, size_x, size_y, thickness=0.5, pos=(0, 0, 0),
                 material=None):
    """Create ground plate: top at Z=0."""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(pos[0], pos[1], pos[2] - thickness/2))
    ob = bpy.context.object
    ob.scale = (size_x, size_y, thickness)
    bpy.ops.object.transform_apply(
        location=False, rotation=False, scale=True)
    ob.name = name
    if material:
        assign_mat(ob, material)
    return ob


def _make_empty(name, pos=(0, 0, 0)):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=pos)
    ob = bpy.context.object
    ob.name = name
    return ob


def build_from_recipe(recipe, verbose=True):
    """Build scene from a recipe dict.
    
    Returns: (root, objects, stats) or (None, [], error_dict)
    """
    clear_scene()
    setup_units()

    name = recipe.get("name", "Untitled")
    stats = {
        "name": name,
        "objects_count": 0,
        "kits_used": [],
        "materials_used": [],
        "tris": 0,
        "warnings": [],
        "errors": [],
    }

    all_objects = []
    kits_set = set()
    mats_set = set()

    # === GROUND ===
    ground_spec = recipe.get("ground")
    if ground_spec:
        size = ground_spec.get("size", [100, 100])
        material = ground_spec.get("material", "dirt")
        thickness = ground_spec.get("thickness", 0.5)
        g = _make_ground(name + "_Ground", size[0], size[1],
                         thickness, material=material)
        all_objects.append(g)
        mats_set.add(material)
        if verbose:
            print("[GROUND] {}x{} mat={}".format(size[0], size[1], material))

    # === OBJECTS ===
    objects_list = recipe.get("objects", [])
    for i, obj_spec in enumerate(objects_list):
        kit = obj_spec.get("kit")
        model = obj_spec.get("model")
        pos = obj_spec.get("pos", [0, 0])
        rot = normalize_rotation(obj_spec.get("rot", 0))
        scale = obj_spec.get("scale", 4.0)
        mat = obj_spec.get("mat")

        if not kit or not model:
            stats["warnings"].append("objects[{}]: skipped (no kit/model)".format(i))
            continue

        kits_set.add(kit)

        try:
            ob = import_into_scene(kit, model, pos_xz=pos, scale=scale,
                                   rotation_z=rot)
            if ob:
                if mat:
                    assign_mat(ob, mat)
                    mats_set.add(mat)
                all_objects.append(ob)
                if verbose:
                    print("  [{}] {} / {} at ({}, {}) rot={}".format(
                        i, kit, model, pos[0], pos[1], rot))
            else:
                stats["errors"].append("objects[{}]: failed to import".format(i))
        except Exception as e:
            stats["errors"].append("objects[{}]: {}".format(i, str(e)))

    # === ROOT EMPTY ===
    if all_objects:
        root = _make_empty(name, pos=(0, 0, 0))
        for ob in all_objects:
            if ob != root:
                ob.parent = root
    else:
        root = None

    # === STATS ===
    stats["objects_count"] = len(all_objects)
    stats["kits_used"] = sorted(kits_set)
    stats["materials_used"] = sorted(mats_set)
    stats["tris"] = sum(
        len(p.vertices) - 2
        for o in all_objects if o.type == 'MESH'
        for p in o.data.polygons)

    if verbose:
        print("")
        print("[TOTAL] {} objects, {} tris".format(
            stats["objects_count"], stats["tris"]))

    return root, all_objects, stats


def get_all_objects():
    """Return all mesh objects in scene (for export)."""
    return [o for o in bpy.data.objects if o.type == 'MESH']