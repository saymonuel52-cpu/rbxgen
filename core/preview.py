# ============================================================
# core/preview.py - Auto-render map preview
# Protocol 4.2.0
# ============================================================
import bpy
import os
import math
from mathutils import Vector

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def _ensure_reports():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    return REPORTS_DIR


def _get_scene_bbox():
    """Get combined bounding box of all mesh objects in scene."""
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    found = False
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        found = True
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            min_v.x = min(min_v.x, world.x)
            min_v.y = min(min_v.y, world.y)
            min_v.z = min(min_v.z, world.z)
            max_v.x = max(max_v.x, world.x)
            max_v.y = max(max_v.y, world.y)
            max_v.z = max(max_v.z, world.z)
    if not found:
        return Vector((0, 0, 0)), Vector((1, 1, 1))
    return min_v, max_v


def _setup_render(width=1200, height=900):
    """Setup render settings."""
    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    try:
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'MATERIAL'
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True
    except Exception as e:
        print("[WARN] Workbench setup: {}".format(e))


def _create_camera(location, target, name="PreviewCam"):
    """Create camera looking at target."""
    cam_data = bpy.data.cameras.new(name=name)
    cam = bpy.data.objects.new(name=name, object_data=cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = location
    direction = (Vector(target) - Vector(location)).normalized()
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam_data.lens = 35
    return cam


def render_view(name, cam_loc, target, filepath):
    """Render one view."""
    cam = _create_camera(cam_loc, target, name="Cam_" + name)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = filepath
    try:
        bpy.ops.render.render(write_still=True)
        print("[RENDER] {} -> {}".format(name, filepath))
    except Exception as e:
        print("[ERROR] render {}: {}".format(name, e))
    bpy.data.objects.remove(cam, do_unlink=True)


def _create_ground_plane(size=100, z=0.0):
    """Temp ground plane for preview (removed after)."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    plane = bpy.context.object
    plane.name = "_PreviewGround"
    # Green material
    mat = bpy.data.materials.new("_PreviewGroundMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.35, 0.5, 0.25, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.9
    plane.data.materials.append(mat)
    return plane


def render_preview(map_name, views=None):
    """Render 4 views of current scene.
    
    views = ['top', 'front', 'side', 'iso']
    """
    if views is None:
        views = ['top', 'front', 'side', 'iso']

    out_dir = _ensure_reports()
    _setup_render()

    # Get scene bbox first
    min_v, max_v = _get_scene_bbox()
    size = (max_v - min_v).length
    ground_size = max(size * 1.5, 20)

    # Add ground plane for context
    ground = _create_ground_plane(size=ground_size, z=0.0)
    center = (min_v + max_v) / 2.0
    size = (max_v - min_v).length
    if size < 5:
        size = 20

    cam_dist = size * 0.9

    print("[PREVIEW] bbox: min={}, max={}, size={:.1f}".format(
        tuple(round(v, 1) for v in min_v),
        tuple(round(v, 1) for v in max_v),
        size))

    # Views
    views_config = {
        'top':   (center + Vector((0, 0, cam_dist)), center),
        'front': (center + Vector((0, -cam_dist, size * 0.5)), center),
        'side':  (center + Vector((cam_dist, 0, size * 0.5)), center),
        'iso':   (center + Vector((cam_dist * 0.7, -cam_dist * 0.7, cam_dist * 0.7)), center),
    }

    for view in views:
        if view not in views_config:
            continue
        cam_loc, target = views_config[view]
        filepath = os.path.join(out_dir, "{}_preview_{}.png".format(map_name, view))
        render_view(view, cam_loc, target, filepath)

    # Remove temp ground
    bpy.data.objects.remove(ground, do_unlink=True)

    print("[PREVIEW] Done. Files in: {}".format(out_dir))
    return out_dir