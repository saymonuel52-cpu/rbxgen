# ============================================================
# core/validator.py - EXTENDED validator
# Protocol 4.2.0
# ============================================================
import bmesh
import bpy
from mathutils import Vector


def validate(ob, level='BASE', budget_tris=None, expected_bbox=None):
    """Extended validator. Returns dict with all checks."""
    errors, warns, info = [], [], {}

    tris = 0
    for p in ob.data.polygons:
        n = len(p.vertices)
        tris += (1 if n == 3 else 2 if n == 4 else n - 2)
    info['tris'] = tris

    if budget_tris and tris > budget_tris:
        errors.append(('E001', 'Tris {} > {}'.format(tris, budget_tris)))

    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # N-gons
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        warns.append(('W001', 'N-gons: {}'.format(len(ngons))))

    # Boundary edges
    boundary = [e for e in bm.edges if e.is_boundary]
    if boundary:
        warns.append(('W002', 'Boundary edges: {}'.format(len(boundary))))

    # Non-manifold
    nonmani = [e for e in bm.edges if not e.is_manifold]
    if nonmani:
        errors.append(('E002', 'Non-manifold: {}'.format(len(nonmani))))

    # Loose verts
    loose = [v for v in bm.verts if not v.link_edges]
    if loose:
        warns.append(('W003', 'Loose verts: {}'.format(len(loose))))

    bm.free()

    # Scale frozen
    if tuple(round(v, 4) for v in ob.scale) != (1.0, 1.0, 1.0):
        errors.append(('E005', 'Scale not frozen: {}'.format(ob.scale)))

    # Materials
    mat_count = len(ob.data.materials)
    info['materials'] = mat_count
    if mat_count > 1:
        warns.append(('W004', 'Materials > 1: {}'.format(mat_count)))
    if mat_count == 0:
        errors.append(('E006', 'No material assigned'))

    # UV
    if not ob.data.uv_layers:
        warns.append(('W005', 'UV layer missing'))

    # Bounding box
    bbox = [tuple(round(v, 3) for v in ob.dimensions)]
    info['bbox'] = bbox

    if expected_bbox:
        for i, axis in enumerate(['X', 'Y', 'Z']):
            exp = expected_bbox[i]
            act = ob.dimensions[i]
            if exp > 0 and abs(act - exp) / exp > 0.5:
                errors.append(('E007', 'BBox {} = {:.2f} vs expected {:.2f}'.format(
                    axis, act, exp)))

    # Origin check (should be near 0,0,0 or within bbox)
    loc = ob.location
    info['origin'] = tuple(round(v, 3) for v in loc)
    if abs(loc.x) > 1.0 or abs(loc.y) > 1.0 or abs(loc.z) > 1.0:
        warns.append(('W006', 'Origin far from (0,0,0): {}'.format(
            tuple(round(v, 2) for v in loc))))

    # Bevel check (count sharp edges)
    sharp_edges = [e for e in ob.data.edges if e.use_edge_sharp]
    info['sharp_edges'] = len(sharp_edges)

    return {
        'tris': tris,
        'errors': errors,
        'warns': warns,
        'info': info,
        'status': 'OK' if not errors else 'FAIL'
    }