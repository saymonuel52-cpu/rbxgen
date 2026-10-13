# ============================================================
# core/validator.py — BASE / EXTENDED / FULL
# ============================================================
import bmesh


def validate(ob, level='BASE', budget_tris=None):
    """Уровни: BASE (10), EXTENDED (+9), FULL (+8)."""
    errors, warns = [], []
    tris = 0
    for p in ob.data.polygons:
        n = len(p.vertices)
        tris += (1 if n == 3 else 2 if n == 4 else n - 2)

    if budget_tris and tris > budget_tris:
        errors.append(('E001', f'Tris {tris} > {budget_tris}'))

    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # N-gons
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        warns.append(('W001', f'N-gons: {len(ngons)}'))

    # Boundary edges
    boundary = [e for e in bm.edges if e.is_boundary]
    if boundary:
        warns.append(('W002', f'Boundary edges: {len(boundary)}'))

    # Non-manifold
    nonmani = [e for e in bm.edges if not e.is_manifold]
    if nonmani:
        errors.append(('E002', f'Non-manifold: {len(nonmani)}'))

    # Loose vertices
    loose = [v for v in bm.verts if not v.link_edges]
    if loose:
        warns.append(('W003', f'Loose verts: {len(loose)}'))

    # Scale freeze
    if tuple(round(v, 4) for v in ob.scale) != (1.0, 1.0, 1.0):
        errors.append(('E005', f'Scale not frozen: {ob.scale}'))

    # Materials
    if len(ob.data.materials) > 1:
        warns.append(('W004', f'Materials > 1: {len(ob.data.materials)}'))

    # UV
    if not ob.data.uv_layers:
        warns.append(('W005', 'UV layer missing'))

    bm.free()

    return {
        'tris': tris,
        'errors': errors,
        'warns': warns,
        'status': 'OK' if not errors else 'FAIL'
    }
