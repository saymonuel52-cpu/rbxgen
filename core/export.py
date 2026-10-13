# ============================================================
# core/export.py - FBX export (Blender 3.6, scale fixed)
# Protocol 4.2.0
# ============================================================
import bpy
import os

DEFAULT_OUT_DIR = "C:/Users/Public/RobloxExports"
# Blender studs = 1 unit. Studio reads FBX as cm (x100).
# global_scale = 0.01 fixes the scale.
FBX_GLOBAL_SCALE = 0.01


def export_fbx(objs, name, out_dir=DEFAULT_OUT_DIR):
    """FBX export with scale fix."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name + ".fbx")
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        global_scale=FBX_GLOBAL_SCALE,
        apply_scale_options='FBX_SCALE_NONE',
        axis_forward='-Z',
        axis_up='Y',
        path_mode='COPY',
        embed_textures=True,
        mesh_smooth_type='FACE',
    )
    print("[EXPORT] " + path + " (scale=" + str(FBX_GLOBAL_SCALE) + ")")
    return path
