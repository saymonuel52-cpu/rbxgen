# ============================================================
# core/scene.py - Scene management (v2, join fixed)
# Protocol 4.2.0
# ============================================================
import bpy
import math


def clear_scene():
    """Full scene cleanup."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def setup_units():
    """[214] Unit System = None."""
    scene = bpy.context.scene
    scene.unit_settings.system = 'NONE'
    scene.unit_settings.scale_length = 0.01


def select_only(ob):
    """Select only specified object."""
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob


def apply_transform(ob, location=False, rotation=True, scale=True):
    """[1] bake transform before join."""
    select_only(ob)
    bpy.ops.object.transform_apply(
        location=location, rotation=rotation, scale=scale)


def join_objects(objs, name, origin_mode='CENTER'):
    """[160] Join with explicit Origin setup. Fixed for headless mode."""
    if not objs:
        raise ValueError("[E] join_objects: empty list")

    if len(objs) == 1:
        joined = objs[0]
        joined.name = name
    else:
        # Ensure all objects are in current view layer
        view_layer = bpy.context.view_layer
        for o in objs:
            if o.name not in view_layer.objects:
                try:
                    view_layer.active_layer_collection.collection.objects.link(o)
                except Exception:
                    pass

        bpy.ops.object.select_all(action='DESELECT')
        for o in objs:
            o.select_set(True)
        view_layer.objects.active = objs[0]

        # Use temp_override to ensure join context
        try:
            with bpy.context.temp_override(
                active_object=objs[0],
                selected_objects=objs,
                selected_editable_objects=objs
            ):
                bpy.ops.object.join()
        except Exception:
            bpy.ops.object.join()

        joined = bpy.context.view_layer.objects.active
        joined.name = name

    # Set Origin
    if origin_mode == 'CENTER':
        bpy.context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    elif origin_mode == 'GEOMETRY':
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    elif origin_mode == 'MEDIAN':
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    elif origin_mode == 'CURSOR':
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    return joined


def count_tris(ob):
    """[151] count tris."""
    tris = 0
    for poly in ob.data.polygons:
        n = len(poly.vertices)
        if n == 3:
            tris += 1
        elif n == 4:
            tris += 2
        else:
            tris += n - 2
    return tris


def add_uv_smart(ob, angle_deg=66.0, margin=0.02):
    """[222] Smart UV Project."""
    select_only(ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(
        angle_limit=math.radians(angle_deg), island_margin=margin)
    bpy.ops.object.mode_set(mode='OBJECT')