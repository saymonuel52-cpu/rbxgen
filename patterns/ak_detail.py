# ============================================================
# patterns/ak_detail.py - DETAILS
# Protocol 4.2.0 | roof_tiles optimized
# ============================================================
import bpy
import math
from core.scene import apply_transform, join_objects
from patterns.aj_atomic import block, plate, beam, column, rod, sphere, cone
from patterns.ak_constructive import wall, floor, ceiling


# ============================================================
# WINDOWS
# ============================================================

def window_frame(name, W, H, T=0.15, pos=(0, 0, 0)):
    """Window frame."""
    rim = T * 0.8
    parts = [
        beam(name + "_Top", (W + rim*2, rim, rim),
             (pos[0], pos[1], pos[2] + H/2)),
        beam(name + "_Bot", (W + rim*2, rim, rim),
             (pos[0], pos[1], pos[2] - H/2)),
        beam(name + "_L", (rim, rim, H),
             (pos[0] - W/2, pos[1], pos[2])),
        beam(name + "_R", (rim, rim, H),
             (pos[0] + W/2, pos[1], pos[2])),
    ]
    parts.append(beam(name + "_V", (rim*0.7, rim*0.7, H),
                      (pos[0], pos[1], pos[2])))
    parts.append(beam(name + "_H", (W, rim*0.7, rim*0.7),
                      (pos[0], pos[1], pos[2])))
    return join_objects(parts, name, origin_mode='GEOMETRY')


def window_glass(name, W, H, pos=(0, 0, 0)):
    """Window glass - no bevel."""
    return block(name, (W, 0.03, H), pos, bevel_width=0.0)


def window_sill(name, W, D=0.3, pos=(0, 0, 0)):
    """Window sill."""
    return block(name, (W + 0.3, D, 0.1), pos)


def window_lintel(name, W, D=0.3, pos=(0, 0, 0)):
    """Window lintel."""
    parts = [
        block(name + "_Main", (W + 0.4, D, 0.15), pos),
        block(name + "_Drip", (W + 0.5, D + 0.1, 0.08),
              (pos[0], pos[1], pos[2] - 0.1)),
    ]
    return join_objects(parts, name, origin_mode='GEOMETRY')


def window_full(name, W, H, T=0.15, pos=(0, 0, 0)):
    """Full window."""
    parts = []
    parts.append(window_frame(name + "_Frame", W, H, T, pos))
    parts.append(window_glass(name + "_Glass", W * 0.85, H * 0.85, pos))
    parts.append(window_sill(name + "_Sill", W, 0.3,
                             (pos[0], pos[1] - 0.1, pos[2] - H/2 - 0.05)))
    parts.append(window_lintel(name + "_Lintel", W, 0.3,
                               (pos[0], pos[1], pos[2] + H/2 + 0.15)))
    return join_objects(parts, name, origin_mode='GEOMETRY')


# ============================================================
# DOORS
# ============================================================

def door_frame(name, W, H, T=0.2, pos=(0, 0, 0)):
    """Door frame."""
    rim = T * 0.9
    parts = [
        beam(name + "_Top", (W + rim*2, T, rim),
             (pos[0], pos[1], pos[2] + H/2)),
        beam(name + "_L", (rim, T, H),
             (pos[0] - W/2 - rim/2, pos[1], pos[2])),
        beam(name + "_R", (rim, T, H),
             (pos[0] + W/2 + rim/2, pos[1], pos[2])),
    ]
    return join_objects(parts, name, origin_mode='GEOMETRY')


def door_panel(name, W, H, T=0.1, pos=(0, 0, 0)):
    """Door panel with insets."""
    parts = [block(name + "_Main", (W, T, H), pos)]
    for sign in (-1, 1):
        parts.append(block(name + "_Inset" + str(sign),
                           (W * 0.7, T * 0.5, H * 0.35),
                           (pos[0], pos[1] + T * 0.4,
                            pos[2] + sign * H * 0.25)))
    return join_objects(parts, name, origin_mode='GEOMETRY')


def door_handle(name, W, pos=(0, 0, 0)):
    """Door handle."""
    x = W/2 - 0.3
    parts = [
        block(name + "_Plate", (0.15, 0.05, 0.25),
              (pos[0] + x, pos[1], pos[2])),
        sphere(name + "_Knob", 0.07, 8, 6,
               (pos[0] + x, pos[1] + 0.1, pos[2])),
    ]
    return join_objects(parts, name, origin_mode='GEOMETRY')


# ============================================================
# ROOF DETAILS
# ============================================================

def chimney(name, W=1.0, D=1.0, H=3.0, pos=(0, 0, 0)):
    """Chimney with cap."""
    parts = [
        block(name + "_Body", (W, D, H),
              (pos[0], pos[1], pos[2] + H/2)),
        block(name + "_Cap", (W + 0.2, D + 0.2, 0.15),
              (pos[0], pos[1], pos[2] + H + 0.05)),
    ]
    return join_objects(parts, name, origin_mode='GEOMETRY')


def roof_tiles(name, W, D, angle_deg=35, n_rows=3, n_cols=4, pos=(0, 0, 0)):
    """Roof tiles - NO bevel, fewer tiles (3x4 per side = 24 total)."""
    parts = []
    half = W / 2
    slope_len = half / math.cos(math.radians(angle_deg))
    tile_w = slope_len / n_cols
    tile_d = D / n_rows
    tile_t = 0.06
    for sign in (-1, 1):
        angle_rad = math.radians(sign * angle_deg)
        for i in range(n_cols):
            u = (i + 0.5) * tile_w
            x = sign * (half - u * math.cos(math.radians(angle_deg)))
            z = u * math.sin(math.radians(angle_deg))
            for j in range(n_rows):
                y = -D/2 + (j + 0.5) * tile_d
                # NO BEVEL for tiles (bevel_width=0)
                parts.append(block(
                    name + "_T" + str(sign) + "_" + str(i) + "_" + str(j),
                    (tile_w * 0.9, tile_d * 0.9, tile_t),
                    (pos[0] + x, pos[1] + y, pos[2] + z),
                    bevel_width=0.0))
    return join_objects(parts, name, origin_mode='GEOMETRY')