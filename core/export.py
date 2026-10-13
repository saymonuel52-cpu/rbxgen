# ============================================================
# core/export.py - FBX export (Roblox official settings)
# Protocol 4.2.0 | Source: create.roblox.com/docs/art/modeling/export-requirements
# ============================================================
import bpy
import os

DEFAULT_OUT_DIR = "C:/Users/Public/RobloxExports"


def export_fbx(objs, name, out_dir=DEFAULT_OUT_DIR):
    """FBX export - Roblox official settings."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name + ".fbx")
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_scale_options='FBX_UNIT_SCALE',  # Official
        axis_forward='-Z',
        axis_up='Y',
        path_mode='COPY',
        embed_textures=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        bake_animation=False,
    )
    print("[EXPORT] " + path)
    return path