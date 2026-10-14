# Modular rules (Kenney kits)

## 1. Module size
- All walls = 1x1 stud at base scale.
- At scale=4.0 -> 4x4 studs.
- Step = module_size * scale.

## 2. Step formula
STEP = BASE_SIZE * SCALE

## 3. Wall orientation by side
| Side   | Rotation Z | Position Z |
|--------|------------|------------|
| South  | 0          | -half      |
| North  | 180        | +half      |
| West   | 90         | 0          |
| East   | -90        | 0          |

## 4. Corner elements (wall-corner)
- SW (-X, -Z): rot = 0
- SE (+X, -Z): rot = -90
- NE (+X, +Z): rot = 180
- NW (-X, +Z): rot = 90

## 5. Overlap
Walls touch each other, no gaps.
Center of module = block position.
Step = module size.

## 6. Rotation function
importer.py applies rotation_z (degrees):
root.rotation_euler = (0, 0, math.radians(rotation_z))

## 7. Castle layout
       (NW)          (NE)
          +----------+
          |          |
          |  Yard    |
          |          |
          +----------+
       (SW)   Gate   (SE)

## 8. JSON config template
{
  "grid_size": 10,
  "module_size": 1.0,
  "scale": 4.0,
  "step": 4.0,
  "wall_height_levels": 3,
  "tower_levels": 5
}
