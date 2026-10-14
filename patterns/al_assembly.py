# ============================================================
# patterns/al_assembly.py - ASSEMBLY (simplified)
# Protocol 4.2.0 | All parts in global coords
# ============================================================
from core.scene import join_objects
from patterns.aj_atomic import block, column, rod, sphere, ring, cone
from patterns.ak_constructive import (wall, floor, ceiling, roof_gable,
                                       roof_hip, stairs, colonnade)
from patterns.am_placement import place_radial


def _room_parts(prefix, W, D, H, cx, cy, cz):
    """Return list of parts for room, at global coords."""
    T = 0.2  # wall thickness
    parts = []
    # Floor (at bottom)
    parts.append(floor(prefix + "_Floor", W, D, T,
                       0, (cx, cy, cz)))
    # Ceiling (at top)
    parts.append(ceiling(prefix + "_Ceil", W, D, T,
                         (cx, cy, cz + H)))
    # 4 walls (each solid block)
    parts.append(wall(prefix + "_W_S", W, H, T, None,
                      (cx, cy - D/2 + T/2, cz)))
    parts.append(wall(prefix + "_W_N", W, H, T, None,
                      (cx, cy + D/2 - T/2, cz)))
    parts.append(wall(prefix + "_W_W", D - T*2, H, T, None,
                      (cx - W/2 + T/2, cy, cz)))
    parts.append(wall(prefix + "_W_E", D - T*2, H, T, None,
                      (cx + W/2 - T/2, cy, cz)))
    return parts


def room(name, W, D, H, has_door=True, has_window=True, pos=(0, 0, 0)):
    """[251] Room."""
    parts = _room_parts(name, W, D, H, pos[0], pos[1], pos[2])
    return join_objects(parts, name, origin_mode='GEOMETRY')


def story(name, W, D, H, n_rooms=1, pos=(0, 0, 0)):
    """[252] Story."""
    parts = []
    room_w = W / n_rooms
    for i in range(n_rooms):
        x = -W/2 + (i + 0.5) * room_w
        parts += _room_parts(
            name + "_R" + str(i),
            room_w * 0.95, D, H,
            pos[0] + x, pos[1], pos[2]
        )
    return join_objects(parts, name, origin_mode='GEOMETRY')


def house_section(name, W, D, H, roof_type='gable', pos=(0, 0, 0)):
    """[253] House - base + room + roof."""
    parts = []
    # Base plate
    parts.append(block(name + "_Base", (W + 0.6, D + 0.6, 0.3),
                       (pos[0], pos[1], pos[2] + 0.15)))
    # Room
    parts += _room_parts(name, W, D, H, pos[0], pos[1], pos[2] + 0.3)
    # Roof
    roof_z = pos[2] + 0.3 + H
    if roof_type == 'gable':
        parts.append(roof_gable(name + "_Roof", W + 0.8, H * 0.5, D + 0.8,
                                35, (pos[0], pos[1], roof_z)))
    else:
        parts.append(roof_hip(name + "_Roof", W + 0.8, D + 0.8, H * 0.5,
                              (pos[0], pos[1], roof_z)))
    return join_objects(parts, name, origin_mode='GEOMETRY')


def tower(name, h, d, roof_type='hip', pos=(0, 0, 0)):
    """[254] Tower."""
    parts = [column(name + "_Body", h, d, 16, pos)]
    if roof_type == 'hip':
        parts.append(roof_hip(name + "_Roof", d + 0.4, d + 0.4, d * 0.6,
                              (pos[0], pos[1], pos[2] + h)))
    return join_objects(parts, name, origin_mode='GEOMETRY')


def mechanism(name, frame_w, frame_d, n_wheels, pos=(0, 0, 0)):
    """[261] Mechanism."""
    parts = [block(name + "_Frame", (frame_w, frame_d, 0.2), pos)]
    return join_objects(parts, name, origin_mode='GEOMETRY')


def nature(name, trunk_h, n_branches=4, n_leaves=3, pos=(0, 0, 0)):
    """[262] Tree."""
    parts = [column(name + "_Trunk", trunk_h, 0.4, 8, pos)]
    branch_pos, _ = place_radial(
        (pos[0], pos[1], pos[2] + trunk_h * 0.7), 0.4, n_branches)
    for i, bp in enumerate(branch_pos):
        parts.append(block(name + "_Branch" + str(i),
                           (0.15, 0.15, 1.5), bp))
    leaf_pos, _ = place_radial(
        (pos[0], pos[1], pos[2] + trunk_h + 0.6), 0.8, n_leaves)
    for i, lp in enumerate(leaf_pos):
        parts.append(sphere(name + "_Leaf" + str(i), 0.9, 8, 6, lp))
    return join_objects(parts, name, origin_mode='GEOMETRY')