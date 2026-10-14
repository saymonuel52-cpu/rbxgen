# ============================================================
# patterns/ak_constructive.py - CONSTRUCTIVE (236-250)
# Protocol 4.2.0 | roof_gable fixed (thickness)
# ============================================================
import bpy
import math
from core.scene import apply_transform, join_objects
from patterns.aj_atomic import block, plate, beam, column, rod


def wall(name, W, H, T, openings=None, pos=(0, 0, 0)):
    """[236] Wall: plate + rim."""
    parts = [plate(name + "_Plate", (W, T, H),
                   (pos[0], pos[1], pos[2] + H/2))]
    rim = T * 1.5
    parts += [
        block(name + "_Bot", (W + rim, rim, rim),
              (pos[0], pos[1], pos[2] + rim/2)),
        block(name + "_Top", (W + rim, rim, rim),
              (pos[0], pos[1], pos[2] + H - rim/2)),
        block(name + "_L", (rim, rim, H),
              (pos[0] - W/2 - rim/2, pos[1], pos[2] + H/2)),
        block(name + "_R", (rim, rim, H),
              (pos[0] + W/2 + rim/2, pos[1], pos[2] + H/2)),
    ]
    return join_objects(parts, name, origin_mode='CENTER')


def floor(name, W, D, T=0.15, n_beams=4, pos=(0, 0, 0)):
    """[237] Floor."""
    parts = [plate(name + "_Plate", (W, D, T), pos)]
    for i in range(n_beams):
        x = (i - (n_beams - 1) / 2) * (W / n_beams)
        parts.append(beam(name + "_Beam" + str(i),
                          (0.15, 0.2, D - 0.4),
                          (pos[0] + x, pos[1], pos[2] - T/2 - 0.1)))
    return join_objects(parts, name, origin_mode='CENTER')


def ceiling(name, W, D, T=0.12, pos=(0, 0, 0)):
    """[238] Ceiling."""
    return plate(name, (W, D, T), pos)


def roof_gable(name, W, H, D=1.0, angle_deg=35, pos=(0, 0, 0)):
    """[239] Gable roof - FIXED with thickness (solid plates)."""
    parts = []
    half = W / 2
    slope_len = math.sqrt(half**2 + H**2)
    thickness = 0.15
    for sign in (-1, 1):
        # Use block (solid) instead of plane (zero thickness)
        # Position: mid-point of slope
        angle_rad = math.radians(sign * angle_deg)
        # Center of the slope
        cx = pos[0] + sign * half/2
        cy = pos[1]
        cz = pos[2] + H/2
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
        r = bpy.context.object
        r.scale = (slope_len, D, thickness)
        r.rotation_euler = (0, angle_rad, 0)
        apply_transform(r)
        parts.append(r)
    # Ridge (top block)
    parts.append(block(name + "_Ridge", (0.25, D, 0.25),
                       (pos[0], pos[1], pos[2] + H)))
    return join_objects(parts, name, origin_mode='GEOMETRY')


def roof_hip(name, W, D, H, pos=(0, 0, 0)):
    """[240] Hip roof."""
    bpy.ops.mesh.primitive_cone_add(
        vertices=4, radius1=max(W, D)/2, radius2=0, depth=H,
        location=(pos[0], pos[1], pos[2] + H/2),
        rotation=(0, 0, math.radians(45)))
    ob = bpy.context.object
    if W > 0:
        ob.scale = (1.0, D/W, 1.0)
    apply_transform(ob)
    ob.name = name
    return ob


def arch(name, span, height, n_segments=8, thick=0.2, pos=(0, 0, 0)):
    """[241] Arch."""
    R = span / (2 * math.sin(math.pi / n_segments))
    parts = []
    for i in range(n_segments):
        angle = i * math.pi / n_segments
        cx = R * math.cos(angle)
        cz = R * math.sin(angle) - R + height
        parts.append(block(name + "_S" + str(i),
                           (thick*1.5, thick*1.5, thick),
                           (pos[0] + cx, pos[1], pos[2] + cz)))
    parts.append(block(name + "_Key",
                       (thick*1.8, thick*1.8, thick*1.2),
                       (pos[0], pos[1], pos[2] + height)))
    return join_objects(parts, name, origin_mode='CENTER')


def truss(name, length, height, n_panels=6, pos=(0, 0, 0)):
    """[242] Truss."""
    parts = []
    panel_len = length / n_panels
    parts.append(beam(name + "_Top", (0.15, 0.15, length),
                      (pos[0], pos[1], pos[2] + height/2)))
    parts.append(beam(name + "_Bot", (0.15, 0.15, length),
                      (pos[0], pos[1], pos[2] - height/2)))
    for i in range(n_panels + 1):
        x = (i - n_panels/2) * panel_len
        parts.append(block(name + "_Post" + str(i),
                           (0.1, 0.1, height),
                           (pos[0] + x, pos[1], pos[2])))
    for i in range(n_panels):
        x1 = (i - n_panels/2) * panel_len
        x2 = (i + 1 - n_panels/2) * panel_len
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=((x1 + x2)/2 + pos[0], pos[1], pos[2]))
        d = bpy.context.object
        diag_len = math.sqrt(panel_len**2 + height**2)
        d.scale = (0.08, 0.08, diag_len)
        d.rotation_euler = (math.atan2(panel_len, height), 0, 0)
        apply_transform(d)
        parts.append(d)
    return join_objects(parts, name, origin_mode='CENTER')


def stairs(name, n_steps, step_w, step_d, step_h, pos=(0, 0, 0)):
    """[244] Stairs."""
    parts = []
    for i in range(n_steps):
        parts.append(block(name + "_S" + str(i),
                           (step_w, step_d, step_h),
                           (pos[0], pos[1] + step_d * (i + 0.5),
                            pos[2] + step_h * (i + 0.5))))
    return join_objects(parts, name, origin_mode='CENTER')


def colonnade(name, n_cols, spacing, h, d=0.5, pos=(0, 0, 0)):
    """[243] Colonnade + architrave."""
    parts = []
    for i in range(n_cols):
        x = (i - (n_cols - 1) / 2) * spacing
        parts.append(column(name + "_C" + str(i), h, d, 8,
                            (pos[0] + x, pos[1], pos[2])))
    total_w = (n_cols - 1) * spacing + d
    parts.append(beam(name + "_Arch", (0.3, 0.3, total_w),
                      (pos[0], pos[1], pos[2] + h + 0.15)))
    return join_objects(parts, name, origin_mode='CENTER')


def opening(name, W, H, T, pos=(0, 0, 0)):
    """[245] Opening - frame."""
    rim = 0.15
    parts = [
        block(name + "_T", (W + rim*2, T, rim),
              (pos[0], pos[1], pos[2] + H/2)),
        block(name + "_B", (W + rim*2, T, rim),
              (pos[0], pos[1], pos[2] - H/2)),
        block(name + "_L", (rim, T, H),
              (pos[0] - W/2, pos[1], pos[2])),
        block(name + "_R", (rim, T, H),
              (pos[0] + W/2, pos[1], pos[2])),
    ]
    return join_objects(parts, name, origin_mode='CENTER')


def frame(name, W, H, T, pos=(0, 0, 0)):
    """[246] Frame."""
    return opening(name, W, H, T, pos)


def base(name, W, D, H=0.3, pos=(0, 0, 0)):
    """[248] Base."""
    parts = [
        plate(name + "_Plate", (W, D, H),
              (pos[0], pos[1], pos[2] + H/2)),
        block(name + "_Rim", (W + 0.2, D + 0.2, H * 0.3),
              (pos[0], pos[1], pos[2] + H * 0.85)),
    ]
    return join_objects(parts, name, origin_mode='CENTER')


def cornice(name, W, T=0.3, D=0.4, pos=(0, 0, 0)):
    """[249] Cornice."""
    parts = [
        block(name + "_Main", (W, D, T), pos),
        block(name + "_Drip", (W, 0.1, T * 0.6),
              (pos[0], pos[1] + D/2, pos[2] - T * 0.5)),
    ]
    return join_objects(parts, name, origin_mode='CENTER')


def parapet(name, W, H, T, n_blocks, pos=(0, 0, 0)):
    """[250] Parapet."""
    parts = []
    spacing = W / n_blocks
    for i in range(n_blocks):
        x = -W/2 + (i + 0.5) * spacing
        parts.append(block(name + "_B" + str(i),
                           (spacing * 0.85, T, H),
                           (pos[0] + x, pos[1], pos[2] + H/2)))
    return join_objects(parts, name, origin_mode='CENTER')