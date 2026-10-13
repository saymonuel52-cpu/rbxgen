# ============================================================
# patterns/al_assembly.py - ASSEMBLY (251-262)
# Protocol 4.2.0
# ============================================================
from core.scene import join_objects
from patterns.aj_atomic import block, column, rod, sphere, ring, cone
from patterns.ak_constructive import (wall, floor, ceiling, roof_gable,
                                       roof_hip, stairs, colonnade)
from patterns.am_placement import place_radial


def room(name, W, D, H, has_door=True, has_window=True, pos=(0, 0, 0)):
    """[251] Room."""
    parts = [floor(name + "_Floor", W, D, 0.15, 4, pos)]
    parts.append(ceiling(name + "_Ceil", W, D, 0.12,
                         (pos[0], pos[1], pos[2] + H)))
    parts.append(wall(name + "_W1", W, H, 0.15,
                      None, (pos[0], pos[1] - D/2, pos[2])))
    parts.append(wall(name + "_W2", W, H, 0.15,
                      None, (pos[0], pos[1] + D/2, pos[2])))
    parts.append(wall(name + "_W3", D, H, 0.15,
                      None, (pos[0] - W/2, pos[1], pos[2])))
    parts.append(wall(name + "_W4", D, H, 0.15,
                      None, (pos[0] + W/2, pos[1], pos[2])))
    return join_objects(parts, name, origin_mode='CENTER')


def story(name, W, D, H, n_rooms=1, pos=(0, 0, 0)):
    """[252] Story."""
    parts = []
    room_w = W / n_rooms
    for i in range(n_rooms):
        x = -W/2 + (i + 0.5) * room_w
        parts.append(room(name + "_Room" + str(i), room_w * 0.95, D, H,
                          True, True, (pos[0] + x, pos[1], pos[2])))
    if n_rooms > 1:
        parts.append(stairs(name + "_Stairs", 8, 0.8, 0.3, 0.4,
                            (pos[0], pos[1] - D/2 - 1.5, pos[2])))
    return join_objects(parts, name, origin_mode='CENTER')


def house_section(name, W, D, H, roof_type='gable', pos=(0, 0, 0)):
    """[253] House section."""
    parts = [block(name + "_Base", (W + 0.6, D + 0.6, 0.3),
                   (pos[0], pos[1], pos[2] + 0.15))]
    parts.append(room(name + "_Room", W, D, H,
                      True, True, (pos[0], pos[1], pos[2] + 0.3)))
    if roof_type == 'gable':
        parts.append(roof_gable(name + "_Roof", W + 0.8, H * 0.5, D + 0.8,
                                35, (pos[0], pos[1], pos[2] + H + 0.3)))
    else:
        parts.append(roof_hip(name + "_Roof", W + 0.8, D + 0.8, H * 0.5,
                              (pos[0], pos[1], pos[2] + H + 0.3)))
    return join_objects(parts, name, origin_mode='CENTER')


def tower(name, h, d, roof_type='hip', pos=(0, 0, 0)):
    """[254] Tower."""
    parts = [column(name + "_Body", h, d, 16, pos)]
    if roof_type == 'hip':
        parts.append(roof_hip(name + "_Roof", d + 0.4, d + 0.4, d * 0.6,
                              (pos[0], pos[1], pos[2] + h)))
    return join_objects(parts, name, origin_mode='CENTER')


def mechanism(name, frame_w, frame_d, n_wheels, pos=(0, 0, 0)):
    """[261] Mechanism."""
    parts = [block(name + "_Frame", (frame_w, frame_d, 0.2), pos)]
    wheel_r = frame_w / 2
    parts.append(ring(name + "_Wheel1", wheel_r, 0.15, 12, 4,
                      (pos[0] - frame_w/2, pos[1], pos[2] + frame_d/2)))
    parts.append(ring(name + "_Wheel2", wheel_r, 0.15, 12, 4,
                      (pos[0] + frame_w/2, pos[1], pos[2] + frame_d/2)))
    spokes, _ = place_radial((pos[0], pos[1], pos[2] + frame_d/2),
                             wheel_r * 0.7, 8)
    for i, sp in enumerate(spokes):
        parts.append(block(name + "_Spoke" + str(i),
                           (0.06, 0.06, wheel_r*0.7), sp))
    return join_objects(parts, name, origin_mode='CENTER')


def nature(name, trunk_h, n_branches=4, n_leaves=3, pos=(0, 0, 0)):
    """[262] Nature - tree."""
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
    return join_objects(parts, name, origin_mode='CENTER')
