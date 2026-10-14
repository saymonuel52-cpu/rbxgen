# ============================================================
# generate_castle.py - Enhanced modular castle
# Protocol 4.2.0 | Uses diverse models from fantasy_town
# ============================================================
import json

SIZE = 8            # grid units per side
SCALE = 4.0         # 1 module = 4 studs
STEP = SCALE
objects = []
half = SIZE // 2


def add(kit, model, pos, scale=SCALE, rot=0.0, mat="stone"):
    objects.append({
        "kit": kit, "model": model,
        "pos": [round(pos[0], 2), round(pos[1], 2)],
        "scale": scale, "rotation": rot, "material": mat
    })


# ============================================================
# PERIMETER WALLS (4 sides)
# ============================================================

# SOUTH WALL (Z = -half) - rot 0
for i in range(-half, half + 1):
    x = i * STEP
    z = -half * STEP
    if i == 0:
        # Main gate - round doorway
        add("fantasy_town", "wall-doorway-round", [x, z], SCALE, 0)
    elif i in (-1, 1):
        # Windows beside gate
        add("fantasy_town", "wall-window-shutters", [x, z], SCALE, 0)
    else:
        add("fantasy_town", "wall", [x, z], SCALE, 0)

# NORTH WALL (Z = +half) - rot 180
for i in range(-half, half + 1):
    x = i * STEP
    z = half * STEP
    if i == 0:
        add("fantasy_town", "wall-window-round", [x, z], SCALE, 180)
    else:
        add("fantasy_town", "wall", [x, z], SCALE, 180)

# WEST WALL (X = -half) - rot 90
for i in range(-half + 1, half):
    x = -half * STEP
    z = i * STEP
    if i == 0:
        add("fantasy_town", "wall-window-shutters", [x, z], SCALE, 90)
    else:
        add("fantasy_town", "wall", [x, z], SCALE, 90)

# EAST WALL (X = +half) - rot -90
for i in range(-half + 1, half):
    x = half * STEP
    z = i * STEP
    if i == 0:
        add("fantasy_town", "wall-window-shutters", [x, z], SCALE, -90)
    else:
        add("fantasy_town", "wall", [x, z], SCALE, -90)


# ============================================================
# CORNERS
# ============================================================
corners = [
    (-half * STEP, -half * STEP, 0),
    ( half * STEP, -half * STEP, -90),
    ( half * STEP,  half * STEP, 180),
    (-half * STEP,  half * STEP, 90),
]
for x, z, rot in corners:
    add("fantasy_town", "wall-corner", [x, z], SCALE, rot)


# ============================================================
# CORNER TOWERS (with varied roofs)
# ============================================================
tower_roofs = ["roof-high-gable", "roof-high-corner",
                "roof-high-flat", "roof-high-point"]

for idx, (cx, cz, _) in enumerate(corners):
    # 4 levels up (alternating wall / wall-window)
    for level in range(4):
        if level % 2 == 0:
            model = "wall"
        else:
            model = "wall-window-small"
        add("fantasy_town", model, [cx, cz], SCALE, 0)
    # Different roof for each tower
    roof = tower_roofs[idx % len(tower_roofs)]
    add("fantasy_town", roof, [cx, cz], SCALE, 0)


# ============================================================
# GATE TOWERS (2 tall towers flanking main gate)
# ============================================================
for sx in [-2, 2]:
    x = sx * STEP
    z = -half * STEP
    for level in range(5):
        if level % 2 == 0:
            model = "wall"
        else:
            model = "wall-window-small"
        add("fantasy_town", model, [x, z], SCALE, 0)
    add("fantasy_town", "roof-high-point", [x, z], SCALE, 0)


# ============================================================
# BANNERS on walls
# ============================================================
banner_positions = [
    (-3 * STEP, -half * STEP, 0, "banner-red"),
    ( 3 * STEP, -half * STEP, 0, "banner-green"),
    (-3 * STEP,  half * STEP, 180, "banner-green"),
    ( 3 * STEP,  half * STEP, 180, "banner-red"),
    (-half * STEP, -3 * STEP, 90, "banner-red"),
    (-half * STEP,  3 * STEP, 90, "banner-green"),
    ( half * STEP, -3 * STEP, -90, "banner-green"),
    ( half * STEP,  3 * STEP, -90, "banner-red"),
]
for x, z, rot, banner in banner_positions:
    add("fantasy_town", banner, [x, z], SCALE, rot, "fabric")


# ============================================================
# PILLARS at gate entrance
# ============================================================
for sx in [-3, 3]:
    x = sx * STEP
    z = -half * STEP + STEP
    add("fantasy_town", "pillar-stone", [x, z], SCALE, 0)


# ============================================================
# FOUNTAIN in center
# ============================================================
add("fantasy_town", "fountain-square", [0, 0], SCALE * 1.3, 0)
add("fantasy_town", "fountain-center", [0, 0], SCALE * 1.3, 0)
add("fantasy_town", "fountain-round-detail", [0, 0], SCALE * 1.3, 0)


# ============================================================
# LANTERNS around courtyard
# ============================================================
lantern_positions = [
    (4, 4), (-4, 4), (4, -4), (-4, -4),
    (8, 8), (-8, 8), (8, -8), (-8, -8),
]
for x, z in lantern_positions:
    add("fantasy_town", "lantern", [x, z], SCALE * 1.5, 0, "iron")


# ============================================================
# INNER BUILDINGS (chapel, smithy)
# ============================================================

# Small chapel (NW area)
chapel_cx, chapel_cz = -10, 10
for i in range(-1, 2):
    for j in range(-1, 2):
        x = chapel_cx + i * STEP
        z = chapel_cz + j * STEP
        # Walls on perimeter
        if i == -1 and j == -1:
            add("fantasy_town", "wall-corner", [x, z], SCALE, 0)
        elif i == 1 and j == 1:
            add("fantasy_town", "wall-corner", [x, z], SCALE, 180)
        elif i == 1 and j == -1:
            add("fantasy_town", "wall-corner", [x, z], SCALE, -90)
        elif i == -1 and j == 1:
            add("fantasy_town", "wall-corner", [x, z], SCALE, 90)
        elif i == 0 and j == -1:
            add("fantasy_town", "wall-doorway-square", [x, z], SCALE, 0)
        else:
            add("fantasy_town", "wall", [x, z], SCALE, 0)
# Chapel roof
for i in range(-1, 2):
    x = chapel_cx + i * STEP
    add("fantasy_town", "roof-gable", [x, chapel_cz], SCALE, 0)
add("fantasy_town", "chimney", [chapel_cx, chapel_cz + STEP], SCALE, 0)


# Small smithy (NE area)
smithy_cx, smithy_cz = 10, 10
for i in range(-1, 2):
    for j in range(-1, 2):
        x = smithy_cx + i * STEP
        z = smithy_cz + j * STEP
        if i in (-1, 1) and j in (-1, 1):
            add("fantasy_town", "wall-corner", [x, z], SCALE, 0)
        elif i == -1 and j == 0:
            add("fantasy_town", "wall-doorway-square", [x, z], SCALE, 0)
        else:
            add("fantasy_town", "wall", [x, z], SCALE, 0)
for i in range(-1, 2):
    x = smithy_cx + i * STEP
    add("fantasy_town", "roof-gable", [x, smithy_cz], SCALE, 0)
add("fantasy_town", "chimney", [smithy_cx, smithy_cz - STEP], SCALE, 0)


# ============================================================
# CARTS in courtyard
# ============================================================
add("fantasy_town", "cart", [7, -half + 3], SCALE, 0, "wood_old")
add("fantasy_town", "cart-high", [-7, -half + 3], SCALE, 0, "wood_old")


# ============================================================
# HEDGES around courtyard
# ============================================================
hedge_positions = [
    (6, 6), (-6, 6), (6, -6), (-6, -6),
    (6, 0), (-6, 0), (0, 6), (0, -6),
]
for x, z in hedge_positions:
    add("fantasy_town", "hedge-large", [x, z], SCALE, 0, "leaf")


# ============================================================
# SPEC
# ============================================================
spec = {
    "name": "Castle_Test",
    "level": "FULL",
    "budget_tris": 20000,
    "ground": {
        "size": [SIZE * SCALE * 2.4, SIZE * SCALE * 2.4],
        "pos": [0, 0, 0],
        "thickness": 0.5,
        "material": "dirt"
    },
    "objects": objects
}

with open("maps/castle.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print("Generated castle.json with {} objects".format(len(objects)))
print("Grid: {} x {} studs".format(SIZE * SCALE, SIZE * SCALE))
