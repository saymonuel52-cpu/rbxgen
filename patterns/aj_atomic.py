# ============================================================
# patterns/aj_atomic.py - ATOMIC PRIMITIVES (226-235)
# Protocol 4.2.0
# ============================================================
import bpy
from core.scene import apply_transform, join_objects


def block(name, size, pos=(0, 0, 0)):
    """[226] Cube. size=(W, H, D). tris = 12."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=pos)
    ob = bpy.context.object
    ob.scale = size
    apply_transform(ob)
    ob.name = name
    return ob


def plate(name, size, pos=(0, 0, 0)):
    """[227] Plate. size=(W, D, T). tris = 12."""
    return block(name, size, pos)


def beam(name, size, pos=(0, 0, 0)):
    """[228] Beam. size=(W, D, L). tris = 12."""
    return block(name, size, pos)


def column(name, h, d, v=8, pos=(0, 0, 0)):
    """[229] Column. v=8 -> 32 tris, v=16 -> 64 tris."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=v, radius=d/2, depth=h,
        location=(pos[0], pos[1], pos[2] + h/2))
    ob = bpy.context.object
    ob.name = name
    return ob


def rod(name, h, d, v=8, pos=(0, 0, 0)):
    """[230] Rod."""
    return column(name, h, d, v, pos)


def ring(name, R, r, maj=12, min_=4, pos=(0, 0, 0)):
    """[231] Torus. tris = maj * min * 2."""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=R, minor_radius=r,
        major_segments=maj, minor_segments=min_,
        location=pos)
    ob = bpy.context.object
    ob.name = name
    return ob


def sphere(name, r, seg=8, ring_count=6, pos=(0, 0, 0)):
    """[232] UV sphere."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=ring_count, radius=r, location=pos)
    ob = bpy.context.object
    ob.name = name
    return ob


def cone(name, r, h, v=16, pos=(0, 0, 0)):
    """[233] Cone. tris = v * 3."""
    bpy.ops.mesh.primitive_cone_add(
        vertices=v, radius1=r, radius2=0, depth=h,
        location=(pos[0], pos[1], pos[2] + h/2))
    ob = bpy.context.object
    ob.name = name
    return ob


def wedge(name, size, back, edge, pos=(0, 0, 0)):
    """[234] Wedge 8 vertices."""
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
    """[235] Grid of bars."""
    parts = []
    for i in range(n):
        y = (i - (n - 1) / 2) * spacing
        parts.append(block(name + "_H" + str(i),
                           (length, bar_w, bar_w),
                           (pos[0], pos[1] + y, pos[2])))
    for j in range(m):
        x = (j - (m - 1) / 2) * spacing
        parts.append(block(name + "_V" + str(j),
                           (bar_w, bar_w, length),
                           (pos[0] + x, pos[1], pos[2])))
    return join_objects(parts, name, origin_mode='GEOMETRY')
