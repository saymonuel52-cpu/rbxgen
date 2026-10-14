# ============================================================
# core/map_builder.py - Build map WITHOUT join
# Protocol 4.2.0 | Each object stays separate
# ============================================================
import bpy
import os
import json
from core.scene import (clear_scene, setup_units, select_only,
                        add_uv_smart, count_tris)
from core.importer import import_into_scene
from core.materials import assign as assign_mat
from core.export import export_fbx
from core.validator import validate
from core.report import write_report


def build_map(spec):
    """Build map - keep objects separate."""
    name = spec["name"]
    ground_spec = spec.get("ground")
    objects = spec.get("objects", [])

    all_objects = []

    # Ground
    if ground_spec:
        from patterns.aj_atomic import block
        size = ground_spec.get("size", [100, 100])
        pos = ground_spec.get("pos", [0, 0, 0])
        g = block(name + "_Ground", (size[0], size[1], 0.2), pos,
                  bevel_width=0.0)
        if ground_spec.get("material"):
            assign_mat(g, ground_spec["material"])
        all_objects.append(g)
        print("[GROUND] {} x {}".format(size[0], size[1]))

    # Objects
    for i, obj_spec in enumerate(objects):
        kit = obj_spec.get("kit", "nature_kit")
        model = obj_spec.get("model")
        pos = obj_spec.get("pos", [0, 0, 0])
        scale = obj_spec.get("scale", 1.0)
        mat = obj_spec.get("material")

        if not model:
            continue

        print("[{}] {} / {} at {}".format(i, kit, model, pos))
        ob = import_into_scene(kit, model, pos=pos, scale=scale,
                               prefer_format="OBJ", snap=True)
        if ob:
            if mat:
                assign_mat(ob, mat)
            all_objects.append(ob)
            print("  -> {}: pos={}, dim={}".format(
                ob.name,
                tuple(round(v, 2) for v in ob.location),
                tuple(round(v, 2) for v in ob.dimensions)))

    print("")
    print("[TOTAL OBJECTS] {}".format(len(all_objects)))

    # Create Empty as scene root
    if all_objects:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        root = bpy.context.object
        root.name = name
        # Parent all objects to root
        for ob in all_objects:
            ob.parent = root

        # Count total tris
        total_tris = 0
        for ob in all_objects:
            if ob.type == 'MESH':
                total_tris += count_tris(ob)
        print("[TOTAL TRIS] {}".format(total_tris))

        return root, all_objects
    return None, []


def process_map(ob, objects, spec):
    """Validate + export."""
    level = spec.get("level", "FULL")
    budget = spec.get("budget_tris", 20000)

    # Validate combined stats
    total_tris = 0
    for o in objects:
        if o.type == 'MESH':
            total_tris += count_tris(o)

    print("")
    print("[VALIDATOR] level={}, tris={}/{}".format(level, total_tris, budget))
    if total_tris > budget:
        print("  [E] E001: Tris {} > {}".format(total_tris, budget))
        status = "FAIL"
    else:
        status = "OK"
    print("[VALIDATOR] status: {}".format(status))

    # Export all meshes
    meshes = [o for o in objects if o.type == 'MESH']
    fbx_path = export_fbx(meshes, spec["name"])

    report = {
        "name": spec["name"],
        "level": level,
        "budget_tris": budget,
        "actual_tris": total_tris,
        "objects_count": len(objects),
        "validator": {
            "status": status,
            "errors": [],
            "warns": [],
        },
        "fbx_path": fbx_path,
    }
    write_report(spec["name"], report)
    return report