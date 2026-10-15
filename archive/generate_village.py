# ============================================================
# generate_village.py - Village with CORRECT house assembly
# Protocol 4.2.0 | Uses scale_system.build_house
# ============================================================
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.scale_system import build_house

SCALE = 4.0
STEP = SCALE
objects = []


def add(kit, model, pos, scale=SCALE, rot=0.0, mat="stone"):
    objects.append({
        "kit": kit, "model": model,
        "pos": [round(pos[0], 2), round(pos[1], 2)],
        "scale": scale, "rotation": rot, "material": mat
    })


def house(cx, cz, size_modules=3, wall_mat="wood_old",
          has_door=True, has_window=True, roof_mat="wood_old"):
    """Build house with correct corners/walls (no overlaps)."""
    objects.extend(build_house(None, cx, cz, size_modules, wall_mat))
    
    # Add roof on top
    half = size_modules // 2
    # Roof tiles
    for i in range(-half, half + 1):
        x = cx + i * STEP
        add("fantasy_town", "roof-gable", [x, cz], SCALE, 0, roof_mat)
    # Roof ends
    add("fantasy_town", "roof-gable-end", [cx - half * STEP, cz], SCALE, 90, roof_mat)
    add("fantasy_town", "roof-gable-end", [cx + half * STEP, cz], SCALE, -90, roof_mat)


# ============================================================
# 4 HOUSES (with correct assembly)
# ============================================================
house(cx=-20, cz=-20, size_modules=3, wall_mat="wood_old")
house(cx=20, cz=-20, size_modules=3, wall_mat="stone")
house(cx=-20, cz=20, size_modules=3, wall_mat="wood_old")
house(cx=20, cz=20, size_modules=4, wall_mat="stone")


# ============================================================
# WELL in center
# ============================================================
add("fantasy_town", "fountain-square", [0, 0], SCALE * 1.5, 0, "stone")
add("fantasy_town", "fountain-center", [0, 0], SCALE * 1.5, 0, "stone")


# ============================================================
# FENCE around village
# ============================================================
half_perim = 40
step_p = int(STEP)

# South fence (with gate opening)
for x in range(-half_perim, half_perim + 1, step_p):
    if abs(x) < 6:
        continue
    add("fantasy_town", "fence", [x, -half_perim], SCALE, 0, "wood_old")

# North fence
for x in range(-half_perim, half_perim + 1, step_p):
    add("fantasy_town", "fence", [x, half_perim], SCALE, 180, "wood_old")

# West fence
for z in range(-half_perim + step_p, half_perim, step_p):
    add("fantasy_town", "fence", [-half_perim, z], SCALE, 90, "wood_old")

# East fence
for z in range(-half_perim + step_p, half_perim, step_p):
    add("fantasy_town", "fence", [half_perim, z], SCALE, -90, "wood_old")

# Fence corners (reuse fence with rotation)
for x, z, rot in [(-half_perim, -half_perim, 0),
                  ( half_perim, -half_perim, -90),
                  ( half_perim,  half_perim, 180),
                  (-half_perim,  half_perim, 90)]:
    add("fantasy_town", "fence", [x, z], SCALE, rot, "wood_old")


# ============================================================
# ROADS (correct - just flat plates, no rotation)
# ============================================================
# Vertical road
for z in range(-36, 37, step_p):
    add("fantasy_town", "road", [0, z], SCALE, 0, "dirt")
# Horizontal road
for x in range(-36, 37, step_p):
    if abs(x) > 4:
        add("fantasy_town", "road", [x, 0], SCALE, 0, "dirt")


# ============================================================
# LANTERNS at crossroads
# ============================================================
for x, z in [(4, 4), (-4, 4), (4, -4), (-4, -4),
             (20, 0), (-20, 0), (0, 20), (0, -20)]:
    add("fantasy_town", "lantern", [x, z], SCALE, 0, "iron")


# ============================================================
# CARTS near houses
# ============================================================
add("fantasy_town", "cart", [12, -18], SCALE, 0, "wood_old")
add("fantasy_town", "cart-high", [-12, -18], SCALE, 0, "wood_old")


# ============================================================
# TREES (from nature_kit)
# ============================================================
tree_positions = [
    (-30, -30, "tree_default"),
    (30, -30, "tree_oak"),
    (-30, 30, "tree_pineTallA"),
    (30, 30, "tree_pineRoundA"),
    (-28, 0, "tree_small"),
    (28, 0, "tree_default"),
    (0, -30, "tree_oak"),
    (0, 30, "tree_pineSmallA"),
]
for x, z, model in tree_positions:
    add("nature_kit", model, [x, z], 3.0, 0, "wood_old")


# ============================================================
# HEDGES
# ============================================================
for x, z in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
    add("fantasy_town", "hedge", [x, z], SCALE, 0, "leaf")


# ============================================================
# SPEC
# ============================================================
spec = {
    "name": "Village_Test",
    "level": "FULL",
    "budget_tris": 20000,
    "ground": {
        "size": [90, 90],
        "pos": [0, 0, 0],
        "thickness": 0.5,
        "material": "dirt"
    },
    "objects": objects
}

with open("maps/village.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print("Generated village.json with {} objects".format(len(objects)))