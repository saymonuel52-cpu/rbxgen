# ============================================================
# core/scale_system.py - CORRECT orientation
# Protocol 4.2.0
# ============================================================
import json
import os

SIZES_FILE = os.path.join(os.path.dirname(__file__), "..", "docs", "kits", "fantasy_town_sizes.json")

_SIZES = None


def _load_sizes():
    global _SIZES
    if _SIZES is None:
        if os.path.exists(SIZES_FILE):
            with open(SIZES_FILE, encoding="utf-8") as f:
                _SIZES = json.load(f)
        else:
            _SIZES = {}
    return _SIZES


def get_size(model_name):
    sizes = _load_sizes()
    if model_name in sizes:
        return sizes[model_name]["dimensions"]
    return None


# Rotation rules - CORRECT for Kenney (wall along Y)
# South wall (along X): rotate 90
# North wall (along X): rotate -90
# West wall (along Y): rotate 0
# East wall (along Y): rotate 180
ROTATION_WALL = {
    "south": 90,
    "north": -90,
    "west": 0,
    "east": 180,
}

# Corner rotation for each of 4 corners
# Based on which walls meet: (South+West, South+East, North+East, North+West)
ROTATION_CORNER = {
    "SW": 0,     # South (along X) + West (along Y)
    "SE": 90,    # South (along X) + East (along Y)
    "NE": 180,   # North (along X) + East (along Y)
    "NW": -90,   # North (along X) + West (along Y)
}


def build_house(cx, cz, size_modules=3, wall_mat="wood_old"):
    """Build house with CORRECT orientation.
    
    Wall model (scale=4): X=0.4 (thin), Y=4.0 (width), Z=4.0 (height)
    Wall extends along Y. To place it along X, rotate 90°.
    """
    half = size_modules // 2
    STEP = 4.0
    objects = []

    def add(model, pos, rot=0, mat=wall_mat):
        objects.append({
            "kit": "fantasy_town",
            "model": model,
            "pos": [round(pos[0], 2), round(pos[1], 2)],
            "scale": 4.0,
            "rotation": rot,
            "material": mat,
        })

    # === CORNERS FIRST ===
    corners = [
        ("SW", cx - half * STEP, cz - half * STEP),
        ("SE", cx + half * STEP, cz - half * STEP),
        ("NE", cx + half * STEP, cz + half * STEP),
        ("NW", cx - half * STEP, cz + half * STEP),
    ]
    for name, x, z in corners:
        add("wall-corner", [x, z], ROTATION_CORNER[name])

    # === WALLS BETWEEN CORNERS ===
    # positions between corners: from -half+1 to half-1
    for i in range(-half + 1, half):
        # South wall - along X - rotate 90
        add("wall", [cx + i * STEP, cz - half * STEP], ROTATION_WALL["south"])
        # North wall - along X - rotate -90
        add("wall", [cx + i * STEP, cz + half * STEP], ROTATION_WALL["north"])
        # West wall - along Y - rotate 0
        add("wall", [cx - half * STEP, cz + i * STEP], ROTATION_WALL["west"])
        # East wall - along Y - rotate 180
        add("wall", [cx + half * STEP, cz + i * STEP], ROTATION_WALL["east"])

    return objects