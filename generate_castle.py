# ============================================================
# generate_castle.py - Correct modular castle
# Protocol 4.2.0 | Walls rotated by side, corners aligned
# ============================================================
import json
import math

SIZE = 8            # grid units per side
SCALE = 4.0         # 1 module = 4 studs
STEP = SCALE        # step = module size
WALL = "wall"
CORNER = "wall-corner"
DOORWAY = "wall-doorway-square-wide"
TOWER_TOP = "roof-high-point"
TOWER_MID = "wall-window-small"

objects = []
half = SIZE // 2


def add(kit, model, pos, scale, rot=0.0, mat="stone"):
    objects.append({
        "kit": kit, "model": model,
        "pos": [round(pos[0], 2), round(pos[1], 2)],
        "scale": scale, "rotation": rot, "material": mat
    })


# === SOUTH WALL (Z = -half) - rot 0 ===
for i in range(-half, half + 1):
    x = i * STEP
    z = -half * STEP
    if i == 0:
        add("fantasy_town", DOORWAY, [x, z], SCALE, 0)
    else:
        add("fantasy_town", WALL, [x, z], SCALE, 0)

# === NORTH WALL (Z = +half) - rot 180 ===
for i in range(-half, half + 1):
    x = i * STEP
    z = half * STEP
    add("fantasy_town", WALL, [x, z], SCALE, 180)

# === WEST WALL (X = -half) - rot 90 ===
for i in range(-half + 1, half):
    x = -half * STEP
    z = i * STEP
    add("fantasy_town", WALL, [x, z], SCALE, 90)

# === EAST WALL (X = +half) - rot -90 ===
for i in range(-half + 1, half):
    x = half * STEP
    z = i * STEP
    add("fantasy_town", WALL, [x, z], SCALE, -90)

# === CORNERS ===
corners = [
    (-half * STEP, -half * STEP, 0),    # SW
    ( half * STEP, -half * STEP, -90),  # SE
    ( half * STEP,  half * STEP, 180),  # NE
    (-half * STEP,  half * STEP, 90),   # NW
]
for x, z, rot in corners:
    add("fantasy_town", CORNER, [x, z], SCALE, rot)

# === TOWERS (4 corners, 4 levels + roof) ===
for cx, cz, _ in corners:
    for level in range(4):
        model = WALL if level % 2 == 0 else TOWER_MID
        add("fantasy_town", model, [cx, cz], SCALE, 0)
    add("fantasy_town", TOWER_TOP, [cx, cz], SCALE, 0)

# === GATE TOWERS (2 tall towers) ===
for sx in [-2, 2]:
    x = sx * STEP
    z = -half * STEP
    for level in range(4):
        model = WALL if level % 2 == 0 else TOWER_MID
        add("fantasy_town", model, [x, z], SCALE, 0)
    add("fantasy_town", TOWER_TOP, [x, z], SCALE, 0)

# === FOUNTAIN (center) ===
add("fantasy_town", "fountain-square", [0, 0], SCALE * 1.2, 0)
add("fantasy_town", "fountain-center", [0, 0], SCALE * 1.2, 0)

# === LANTERNS ===
for x, z in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
    add("fantasy_town", "lantern", [x * SCALE, z * SCALE],
        SCALE * 1.5, 0, "iron")

# === CARTS near gate ===
add("fantasy_town", "cart", [4, -half + 2], SCALE, 0, "wood_old")
add("fantasy_town", "cart-high", [-4, -half + 2], SCALE, 0, "wood_old")

# === HEDGES ===
for x, z in [(5, 5), (-5, 5), (5, -5), (-5, -5)]:
    add("fantasy_town", "hedge-large", [x, z], SCALE, 0, "leaf")


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
