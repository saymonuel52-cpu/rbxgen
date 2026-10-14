# ============================================================
# core/preview.py - Improved preview render
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
    """Combined bbox of all MESH objects."""
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    found = False
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        if obj.name.startswith("_Preview"):
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


def _setup_render(width=1600, height=1200):
    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False

    # Use Workbench with good settings
    try:
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'OBJECT'   # Object color
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True
        scene.display.shading.cavity_type = 'BOTH'
        scene.display.shading.curvature_ridge_factor = 1.5
        scene.display.shading.curvature_valley_factor = 1.0

        # Background color
        scene.world = bpy.data.worlds.new("_PreviewWorld")
        scene.world.use_nodes = True
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)  # dark blue
            bg.inputs[1].default_value = 1.0
    except Exception as e:
        print("[WARN] Render setup: {}".format(e))


def _create_camera(location, target, name="PreviewCam"):
    cam_data = bpy.data.cameras.new(name=name)
    cam = bpy.data.objects.new(name=name, object_data=cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = location
    direction = (Vector(target) - Vector(location)).normalized()
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam_data.lens = 50
    return cam


def render_view(name, cam_loc, target, filepath):
    cam = _create_camera(cam_loc, target, name="Cam_" + name)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = filepath
    try:
        bpy.ops.render.render(write_still=True)
        print("[RENDER] {} -> {}".format(name, filepath))
    except Exception as e:
        print("[ERROR] render {}: {}".format(name, e))
    bpy.data.objects.remove(cam, do_unlink=True)


def _create_ground_plane(size, z=0.0):
    """Ground plane with green color (object color mode)."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    plane = bpy.context.object
    plane.name = "_PreviewGround"

    # Set object color (used by Workbench OBJECT mode)
    plane.color = (0.25, 0.45, 0.2, 1.0)  # green

    # Also create material (fallback)
    mat = bpy.data.materials.new("_PreviewGroundMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.25, 0.45, 0.2, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.9
    plane.data.materials.append(mat)
    return plane


def _add_object_colors():
    """Assign distinct colors to objects for better visibility."""
    colors = [
        (0.6, 0.4, 0.2, 1.0),   # brown (trees)
        (0.5, 0.5, 0.5, 1.0),   # gray (rocks)
        (0.3, 0.5, 0.3, 1.0),   # green
        (0.7, 0.5, 0.3, 1.0),   # light brown
        (0.4, 0.4, 0.6, 1.0),   # blue-ish
    ]
    i = 0
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        if obj.name.startswith("_Preview"):
            continue
        obj.color = colors[i % len(colors)]
        i += 1


def render_preview(map_name, views=None):
    """Render 4 views: top, front, side, iso."""
    if views is None:
        views = ['top', 'front', 'side', 'iso']

    out_dir = _ensure_reports()
    _setup_render()

    # Get bbox FIRST (before adding ground)
    min_v, max_v = _get_scene_bbox()
    center = (min_v + max_v) / 2.0
    size = max(max_v.x - min_v.x, max_v.y - min_v.y, max_v.z - min_v.z)
    if size < 5:
        size = 20

    # Ground slightly larger than bbox
    ground_size = size * 1.3

    # Add ground
    ground = _create_ground_plane(size=ground_size, z=-0.05)

    # Assign colors to objects
    _add_object_colors()

    # Camera distance: close enough to see objects
    cam_dist = size * 0.8

    print("[PREVIEW] bbox: min={}, max={}".format(
        tuple(round(v, 1) for v in min_v),
        tuple(round(v, 1) for v in max_v)))
    print("[PREVIEW] size={:.1f}, cam_dist={:.1f}, ground_size={:.1f}".format(
        size, cam_dist, ground_size))

    views_config = {
        'top':   (center + Vector((0, 0, cam_dist)), center),
        'front': (center + Vector((0, -cam_dist, size * 0.4)), center),
        'side':  (center + Vector((cam_dist, 0, size * 0.4)), center),
        'iso':   (center + Vector((cam_dist * 0.6, -cam_dist * 0.6, cam_dist * 0.6)), center),
    }

    for view in views:
        if view not in views_config:
            continue
        cam_loc, target = views_config[view]
        filepath = os.path.join(out_dir, "{}_preview_{}.png".format(map_name, view))
        render_view(view, cam_loc, target, filepath)

    bpy.data.objects.remove(ground, do_unlink=True)
    print("[PREVIEW] Done. Files in: {}".format(out_dir))
    return out_dir