# ============================================================
# patterns/aj_atomic.py — АТОМАРНЫЕ ПРИМИТИВЫ (226–235)
# Protocol 4.2.0
# ============================================================
import bpy
from core.scene import apply_transform, join_objects


def block(name, size, pos=(0, 0, 0)):
    """[226] Куб. size=(W, H, D). tris = 12."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=pos)
    ob = bpy.context.object
    ob.scale = size
    apply_transform(ob)
    ob.name = name
    return ob


def plate(name, size, pos=(0, 0, 0)):
    """[227] Плита. thickness <= 0.2. tris = 12."""
    W, D, T = size
    assert T <= 0.2, f"[E] plate: thickness {T} > 0.2"
    return block(name, (W, D, T), pos)


def beam(name, size, pos=(0, 0, 0)):
    """[228] Балка. L/W >= 5. tris = 12."""
    W, D, L = size
    assert L / max(W, D) >= 5, f"[E] beam: L/W < 5"
    return block(name, (W, D, L), pos)


def column(name, h, d, v=8, pos=(0, 0, 0)):
    """[229] Колонна. v=8 -> 32 tris, v=16 -> 64 tris."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=v, radius=d/2, depth=h,
        location=(pos[0], pos[1], pos[2] + h/2))
    ob = bpy.context.object
    ob.name = name
    return ob


def rod(name, h, d, v=8, pos=(0, 0, 0)):
    """[230] Стержень. d <= 0.2."""
    assert d <= 0.2, f"[E] rod: d {d} > 0.2"
    return column(name, h, d, v, pos)


def ring(name, R, r, maj=12, min_=4, pos=(0, 0, 0)):
    """[231] Тор. tris = maj * min * 2."""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=R, minor_radius=r,
        major_segments=maj, minor_segments=min_,
        location=pos)
    ob = bpy.context.object
    ob.name = name
    return ob


def sphere(name, r, seg=8, ring_count=6, pos=(0, 0, 0)):
    """[232] UV-сфера. tris = seg * (2 * ring - 2)."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=ring_count, radius=r, location=pos)
    ob = bpy.context.object
    ob.name = name
    return ob


def cone(name, r, h, v=16, pos=(0, 0, 0)):
    """[233] Конус. tris = v * 3."""
    bpy.ops.mesh.primitive_cone_add(
        vertices=v, radius1=r, radius2=0, depth=h,
        location=(pos[0], pos[1], pos[2] + h/2))
    ob = bpy.context.object
    ob.name = name
    return ob


def wedge(name, size, back, edge, pos=(0, 0, 0)):
    """[234] Клин 8 вершин. back >= 3 * edge. tris = 12."""
    assert back >= 3 * edge, f"[E] wedge: back {back} < 3 * edge {edge}"
    W, H, D = size
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    verts = [
        (-W/2, -D/2, 0), (W/2, -D/2, 0),
        (W/2, -D/2, H), (-W/2, -D/2, H),
        (-W/2,  D/2, 0), (W/2,  D/2, 0),
        (W/2,  D/2, H), (-W/2,  D/2, H),
    ]
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5),
        (0, 4, 5, 1), (3, 2, 6, 7),
        (0, 3, 7, 4), (1, 5, 6, 2),
    ]
    me.from_pydata(verts, [], faces)
    ob.location = pos
    return ob


def grid_bars(name, n, m, spacing, bar_w=0.06, length=1.0, pos=(0, 0, 0)):
    """[235] Решётка: n балок вдоль X + m вдоль Z."""
    parts = []
    for i in range(n):
        y = (i - (n - 1) / 2) * spacing
        parts.append(block(f"{name}_H{i}", (length, bar_w, bar_w),
                           (pos[0], pos[1] + y, pos[2])))
    for j in range(m):
        x = (j - (m - 1) / 2) * spacing
        parts.append(block(f"{name}_V{j}", (bar_w, bar_w, length),
                           (pos[0] + x, pos[1], pos[2])))
    return join_objects(parts, name, origin_mode='GEOMETRY')
