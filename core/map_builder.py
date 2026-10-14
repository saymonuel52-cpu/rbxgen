# ============================================================
# core/map_builder.py - pos = [X, Z] (horizontal)
# Protocol 4.2.0
# ============================================================
import bpy
import os
import json
from core.scene import (clear_scene, setup_units, count_tris)
from core.importer import import_into_scene
from core.materials import assign as assign_mat
from core.export import export_fbx
from core.report import write_report


def _make_ground(name, size_x, size_y, thickness=0.5, pos=(0, 0, 0)):
    """Ground: top at Z=0, extends down."""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(pos[0], pos[1], pos[2] - thickness/2))
    ob = bpy.context.object
    ob.scale = (size_x, size_y, thickness)
    bpy.ops.object.transform_apply(
        location=False, rotation=False, scale=True)
    ob.name = name
    return ob


def build_map(spec):
    name = spec["name"]
    ground_spec = spec.get("ground")
    objects = spec.get("objects", [])
    all_objects = []

    if ground_spec:
        size = ground_spec.get("size", [100, 100])
        pos = ground_spec.get("pos", [0, 0, 0])
        thickness = ground_spec.get("thickness", 0.5)
        g = _make_ground(name + "_Ground", size[0], size[1], thickness, pos)
        if ground_spec.get("material"):
            assign_mat(g, ground_spec["material"])
        all_objects.append(g)
        print("[GROUND] {} x {}".format(size[0], size[1]))

    for i, obj_spec in enumerate(objects):
        kit = obj_spec.get("kit", "nature_kit")
        model = obj_spec.get("model")
        pos = obj_spec.get("pos", [0, 0])
        scale = obj_spec.get("scale", 1.0)
        mat = obj_spec.get("material")

        if not model:
            continue

        print("[{}] {} / {} at [X={}, Z={}]".format(i, kit, model, pos[0], pos[1]))
        ob = import_into_scene(kit, model, pos_xz=pos, scale=scale,
                               prefer_format="OBJ")
        if ob:
            if mat:
                assign_mat(ob, mat)
            all_objects.append(ob)
            print("  -> {}: pos={}".format(ob.name,
                  tuple(round(v, 2) for v in ob.location)))

    print("")
    print("[TOTAL OBJECTS] {}".format(len(all_objects)))

    if all_objects:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        root = bpy.context.object
        root.name = name
        for ob in all_objects:
            ob.parent = root

        total_tris = 0
        for ob in all_objects:
            if ob.type == 'MESH':
                total_tris += count_tris(ob)
        print("[TOTAL TRIS] {}".format(total_tris))
        return root, all_objects
    return None, []


def process_map(ob, objects, spec):
    level = spec.get("level", "FULL")
    budget = spec.get("budget_tris", 20000)
    total_tris = 0
    for o in objects:
        if o.type == 'MESH':
            total_tris += count_tris(o)
    print("")
    print("[VALIDATOR] level={}, tris={}/{}".format(level, total_tris, budget))
    status = "OK" if total_tris <= budget else "FAIL"
    print("[VALIDATOR] status: {}".format(status))
    meshes = [o for o in objects if o.type == 'MESH']
    fbx_path = export_fbx(meshes, spec["name"])
    report = {
        "name": spec["name"],
        "level": level,
        "budget_tris": budget,
        "actual_tris": total_tris,
        "objects_count": len(objects),
        "validator": {"status": status, "errors": [], "warns": []},
        "fbx_path": fbx_path,
    }
    from core.report import write_report as wr
    wr(spec["name"], report)
    return report