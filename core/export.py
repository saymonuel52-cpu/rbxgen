# ============================================================
# core/export.py - FBX export
# Protocol 4.2.0 v2.0
# ============================================================
import bpy
import os

DEFAULT_OUT_DIR = "C:/Users/Public/RobloxExports"


def export_fbx(objs, name, out_dir=None):
    """Export selection to FBX. If out_dir is None, use default."""
    if out_dir is None:
        out_dir = DEFAULT_OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name + ".fbx")
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_UNITS',
        axis_forward='-Z',
        axis_up='Y',
        path_mode='COPY',
        embed_textures=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
    )
    print("[EXPORT] " + path)
    return path