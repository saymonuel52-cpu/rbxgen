# ============================================================
# core/export.py — FBX экспорт (правила 179, 216, 225)
# ============================================================
import bpy
import os

DEFAULT_OUT_DIR = "C:/Users/Public/RobloxExports"


def export_fbx(objs, name, out_dir=DEFAULT_OUT_DIR):
    """[2] Абсолютный путь. [216] Полный пресет."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.fbx")
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_NONE',
        global_scale=1.0,
        mesh_smooth_type='FACE',
        use_mesh_edges=False,
        use_mesh_vertices=False,
        path_mode='COPY',
        embed_textures=True,
        add_leaf_bones=False,
        bake_animation=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        axis_forward='-Z',
        axis_up='Y',
    )
    print(f"[EXPORT] {path}")
    return path
