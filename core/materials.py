# ============================================================
# core/materials.py — Материалы (правило 139)
# ============================================================
import bpy

STANDARD = {
    'wood_old':   {'color': (0.35, 0.24, 0.15), 'rough': 0.85, 'metal': 0.0},
    'wood_new':   {'color': (0.55, 0.40, 0.25), 'rough': 0.65, 'metal': 0.0},
    'stone':      {'color': (0.55, 0.52, 0.48), 'rough': 0.90, 'metal': 0.0},
    'iron':       {'color': (0.25, 0.25, 0.28), 'rough': 0.40, 'metal': 0.8},
    'galvanized': {'color': (0.55, 0.58, 0.62), 'rough': 0.50, 'metal': 0.6},
    'glass':      {'color': (0.15, 0.25, 0.30), 'rough': 0.10, 'metal': 0.0, 'alpha': 0.3},
    'fabric':     {'color': (0.60, 0.30, 0.25), 'rough': 0.90, 'metal': 0.0},
    'leather':    {'color': (0.30, 0.18, 0.12), 'rough': 0.70, 'metal': 0.0},
    'vine':       {'color': (0.25, 0.40, 0.20), 'rough': 0.85, 'metal': 0.0},
    'gold':       {'color': (0.85, 0.70, 0.20), 'rough': 0.30, 'metal': 0.9},
    'straw':      {'color': (0.75, 0.60, 0.35), 'rough': 0.90, 'metal': 0.0},
    'leaf':       {'color': (0.25, 0.45, 0.20), 'rough': 0.90, 'metal': 0.0},
    'dirt':       {'color': (0.40, 0.35, 0.22), 'rough': 0.95, 'metal': 0.0},
}


def get_or_create(mat_name):
    mat = bpy.data.materials.get(mat_name)
    if mat:
        return mat
    spec = STANDARD.get(mat_name, {'color': (0.5, 0.5, 0.5), 'rough': 0.8, 'metal': 0.0})
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*spec['color'], 1.0)
    bsdf.inputs["Roughness"].default_value = spec['rough']
    bsdf.inputs["Metallic"].default_value = spec['metal']
    if 'alpha' in spec:
        bsdf.inputs["Alpha"].default_value = spec['alpha']
        mat.blend_method = 'BLEND'
    return mat


def assign(ob, mat_name):
    mat = get_or_create(mat_name)
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
    return mat
