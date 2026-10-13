# ============================================================
# core/export.py - FBX export (Blender 3.6 minimal)
# Protocol 4.2.0
# ============================================================
import bpy
import os

DEFAULT_OUT_DIR = "C:/Users/Public/RobloxExports"


def export_fbx(objs, name, out_dir=DEFAULT_OUT_DIR):
    """FBX export - minimal Blender 3.6 compatible."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name + ".fbx")
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        global_scale=1.0,
        apply_scale_options='FBX_SCALE_NONE',
        axis_forward='-Z',
        axis_up='Y',
        path_mode='COPY',
        embed_textures=True,
        mesh_smooth_type='FACE',
    )
    print("[EXPORT] " + path)
    return path
