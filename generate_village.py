# ============================================================
# generate_village.py - Village with 4 modular houses
# Protocol 4.2.0 | Uses fantasy_town + nature_kit
# ============================================================
import json

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
    """Build a small house.
    
    cx, cz = center position (in studs).
    size_modules = house side length in modules.
    """
    half = size_modules / 2.0
    # Grid positions for walls
    positions = [(i - (size_modules - 1) / 2.0) * STEP
                 for i in range(size_modules)]

    # SOUTH wall (rot=0) - Z = cz - half*STEP
    for idx, dx in enumerate(positions):
        x = cx + dx
        z = cz - half * STEP
        if has_door and idx == size_modules // 2:
            add("fantasy_town", "wall-doorway-square-wide",
                [x, z], SCALE, 0, wall_mat)
        else:
            add("fantasy_town", "wall", [x, z], SCALE, 0, wall_mat)

    # NORTH wall (rot=180)
    for idx, dx in enumerate(positions):
        x = cx + dx
        z = cz + half * STEP
        if has_window and idx == size_modules // 2:
            add("fantasy_town", "wall-window-stone",
                [x, z], SCALE, 180, wall_mat)
        else:
            add("fantasy_town", "wall", [x, z], SCALE, 180, wall_mat)

    # WEST wall (rot=90)
    for dx in positions[1:-1] if size_modules > 2 else positions:
        x = cx - half * STEP
        z = cz + dx
        add("fantasy_town", "wall", [x, z], SCALE, 90, wall_mat)

    # EAST wall (rot=-90)
    for dx in positions[1:-1] if size_modules > 2 else positions:
        x = cx + half * STEP
        z = cz + dx
        add("fantasy_town", "wall", [x, z], SCALE, -90, wall_mat)

    # CORNERS
    corners = [
        (cx - half * STEP, cz - half * STEP, 0),
        (cx + half * STEP, cz - half * STEP, -90),
        (cx + half * STEP, cz + half * STEP, 180),
        (cx - half * STEP, cz + half * STEP, 90),
    ]
    for x, z, rot in corners:
        add("fantasy_town", "wall-corner", [x, z], SCALE, rot, wall_mat)

    # ROOF - gable pieces
    for idx, dx in enumerate(positions):
        x = cx + dx
        z = cz
        add("fantasy_town", "roof-gable", [x, z], SCALE, 0, roof_mat)
    # Roof ends
    add("fantasy_town", "roof-gable-end",
        [cx - half * STEP, cz], SCALE, 90, roof_mat)
    add("fantasy_town", "roof-gable-end",
        [cx + half * STEP, cz], SCALE, -90, roof_mat)


# === 4 HOUSES ===
house(cx=-20, cz=-20, size_modules=3, wall_mat="wood_old",
      has_door=True, has_window=True, roof_mat="wood_old")

house(cx=20, cz=-20, size_modules=3, wall_mat="stone",
      has_door=True, has_window=True, roof_mat="stone")

house(cx=-20, cz=20, size_modules=3, wall_mat="wood_old",
      has_door=True, has_window=True, roof_mat="wood_old")

house(cx=20, cz=20, size_modules=4, wall_mat="stone",
      has_door=True, has_window=True, roof_mat="stone")


# === WELL / FOUNTAIN (center) ===
add("fantasy_town", "fountain-square", [0, 0], SCALE * 1.5, 0, "stone")
add("fantasy_town", "fountain-center", [0, 0], SCALE * 1.5, 0, "stone")


# === FENCE around village (perimeter 80x80) ===
half_perim = 40
# South fence
for x in range(-half_perim, half_perim + 1, int(STEP)):
    if abs(x) < 6:  # gate opening
        continue
    add("fantasy_town", "fence", [x, -half_perim], SCALE, 0, "wood_old")
# North fence
for x in range(-half_perim, half_perim + 1, int(STEP)):
    add("fantasy_town", "fence", [x, half_perim], SCALE, 180, "wood_old")
# West fence
for z in range(-half_perim + int(STEP), half_perim, int(STEP)):
    add("fantasy_town", "fence", [-half_perim, z], SCALE, 90, "wood_old")
# East fence
for z in range(-half_perim + int(STEP), half_perim, int(STEP)):
    add("fantasy_town", "fence", [half_perim, z], SCALE, -90, "wood_old")

# Fence corners
for x, z, rot in [(-half_perim, -half_perim, 0),
                  ( half_perim, -half_perim, -90),
                  ( half_perim,  half_perim, 180),
                  (-half_perim,  half_perim, 90)]:
    add("fantasy_town", "fence", [x, z], SCALE, rot, "wood_old")


# === ROADS (paths between houses) ===
# Vertical road
for z in range(-35, 36, int(STEP)):
    add("fantasy_town", "road", [0, z], SCALE, 0, "dirt")
# Horizontal road
for x in range(-35, 36, int(STEP)):
    if abs(x) > 2:
        add("fantasy_town", "road", [x, 0], SCALE, 90, "dirt")


# === LANTERNS at crossroads ===
for x, z in [(4, 4), (-4, 4), (4, -4), (-4, -4),
             (20, 0), (-20, 0), (0, 20), (0, -20)]:
    add("fantasy_town", "lantern", [x, z], SCALE * 1.5, 0, "iron")


# === CARTS near houses ===
add("fantasy_town", "cart", [12, -18], SCALE, 0, "wood_old")
add("fantasy_town", "cart-high", [-12, -18], SCALE, 0, "wood_old")
add("fantasy_town", "cart", [12, 18], SCALE, 0, "wood_old")


# === TREES around village (nature_kit) ===
tree_positions = [
    (-30, -30, "tree_default"),
    (30, -30, "tree_oak"),
    (-30, 30, "tree_pineTallA"),
    (30, 30, "tree_pineRoundA"),
    (-28, 0, "tree_small"),
    (28, 0, "tree_default"),
    (0, -30, "tree_oak"),
    (0, 30, "tree_pineSmallA"),
    (-15, -30, "tree_pineTallB"),
    (15, 30, "tree_default_dark"),
]
for x, z, model in tree_positions:
    add("nature_kit", model, [x, z], 3.0, 0, "wood_old")


# === HEDGES inside village ===
for x, z in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
    add("fantasy_town", "hedge", [x, z], SCALE, 0, "leaf")


# === BANNERS on houses ===
add("fantasy_town", "banner-red",
    [-20, -half_perim if False else -20], SCALE, 0, "fabric")


# === SPEC ===
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
print("Village size: 80 x 80 studs")
