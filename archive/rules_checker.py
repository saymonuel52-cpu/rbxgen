# ============================================================
# core/rules_checker.py - Validate map BEFORE generation
# Protocol 4.2.0 | Fail-fast validation
# ============================================================
import json
import os

def check_grid(position, grid=4):
    """Rule 1.1: All positions must be multiple of grid."""
    return all(abs(p % grid) < 0.01 or abs(p % grid - grid) < 0.01 for p in position[:2])

def check_on_ground(position):
    """Rule 9.5: All objects on Z=0."""
    return len(position) < 3 or abs(position[2]) < 0.01

def check_rotation(rotation):
    """Rule 8.2: Only 0, 90, 180, -90."""
    return rotation in [0, 90, 180, -90, 270, -180, -270]

def check_collision(obj1, obj2, min_distance=1.0):
    """Rule 12.1: No overlaps."""
    dx = abs(obj1["pos"][0] - obj2["pos"][0])
    dz = abs(obj1["pos"][1] - obj2["pos"][1])
    return dx > min_distance or dz > min_distance

def validate_map(map_data, strict=False):
    """Validate entire map. Returns (errors, warnings)."""
    errors = []
    warnings = []
    
    objects = map_data.get("objects", [])
    
    for i, obj in enumerate(objects):
        pos = obj.get("pos", [0, 0])
        rot = obj.get("rotation", 0)
        model = obj.get("model", "?")
        
        # Rule 1.1 - grid
        if not check_grid(pos):
            msg = f"[{i}] {model}: pos {pos} not on grid (multiple of 4)"
            if strict:
                errors.append(msg)
            else:
                warnings.append(msg)
        
        # Rule 9.5 - on ground
        if not check_on_ground(pos):
            errors.append(f"[{i}] {model}: not on ground (Z={pos[2]})")
        
        # Rule 8.2 - rotation
        if not check_rotation(rot):
            warnings.append(f"[{i}] {model}: rotation {rot} not standard (0/90/180/-90)")
    
    # Rule 12.1 - collisions (pairs)
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if not check_collision(objects[i], objects[j]):
                a = objects[i]
                b = objects[j]
                warnings.append(
                    f"Possible overlap: {a['model']} at {a['pos']} "
                    f"and {b['model']} at {b['pos']}"
                )
    
    return errors, warnings


def check_map_file(map_path, strict=False):
    """Check a map JSON file."""
    with open(map_path, encoding="utf-8-sig") as f:
        data = json.load(f)
    
    name = data.get("name", "unknown")
    print(f"=== Checking: {name} ===")
    print(f"Objects: {len(data.get('objects', []))}")
    print()
    
    errors, warnings = validate_map(data, strict=strict)
    
    if errors:
        print("ERRORS:")
        for e in errors[:20]:
            print(f"  [E] {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
    else:
        print("No errors")
    
    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings[:20]:
            print(f"  [W] {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")
    else:
        print("No warnings")
    
    return errors, warnings


if __name__ == "__main__":
    import sys
    maps = ["maps/castle.json", "maps/village.json"]
    if len(sys.argv) > 1:
        maps = sys.argv[1:]
    
    for mp in maps:
        if os.path.exists(mp):
            check_map_file(mp)
            print()
            print("=" * 60)
            print()
