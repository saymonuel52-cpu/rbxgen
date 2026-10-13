# ============================================================
# patterns/__init__.py — РЕЕСТР ПАТТЕРНОВ
# Protocol 4.2.0
# ============================================================
from .aj_atomic import *
from .ak_constructive import *
from .am_placement import *
from .an_joints import *
from .al_assembly import *


REGISTRY = {
    # AJ — атомарные (10)
    'block':  {'fn': 'block',  'category': 'atomic'},
    'plate':  {'fn': 'plate',  'category': 'atomic'},
    'beam':   {'fn': 'beam',   'category': 'atomic'},
    'column': {'fn': 'column', 'category': 'atomic'},
    'rod':    {'fn': 'rod',    'category': 'atomic'},
    'ring':   {'fn': 'ring',   'category': 'atomic'},
    'sphere': {'fn': 'sphere', 'category': 'atomic'},
    'cone':   {'fn': 'cone',   'category': 'atomic'},
    'wedge':  {'fn': 'wedge',  'category': 'atomic'},
    'grid_bars': {'fn': 'grid_bars', 'category': 'atomic'},

    # AK — конструктивные (14)
    'wall':      {'fn': 'wall',      'category': 'constructive'},
    'floor':     {'fn': 'floor',     'category': 'constructive'},
    'ceiling':   {'fn': 'ceiling',   'category': 'constructive'},
    'roof_gable':{'fn': 'roof_gable','category': 'constructive'},
    'roof_hip':  {'fn': 'roof_hip',  'category': 'constructive'},
    'arch':      {'fn': 'arch',      'category': 'constructive'},
    'truss':     {'fn': 'truss',     'category': 'constructive'},
    'colonnade': {'fn': 'colonnade', 'category': 'constructive'},
    'stairs':    {'fn': 'stairs',    'category': 'constructive'},
    'opening':   {'fn': 'opening',   'category': 'constructive'},
    'frame':     {'fn': 'frame',     'category': 'constructive'},
    'base':      {'fn': 'base',      'category': 'constructive'},
    'cornice':   {'fn': 'cornice',   'category': 'constructive'},
    'parapet':   {'fn': 'parapet',   'category': 'constructive'},

    # AM — размещения (7)
    'place_linear': {'fn': 'place_linear', 'category': 'placement'},
    'place_radial': {'fn': 'place_radial', 'category': 'placement'},
    'place_grid':   {'fn': 'place_grid',   'category': 'placement'},
    'place_spiral': {'fn': 'place_spiral', 'category': 'placement'},
    'place_mirror': {'fn': 'place_mirror', 'category': 'placement'},
    'place_bezier': {'fn': 'place_bezier', 'category': 'placement'},
    'place_jitter': {'fn': 'place_jitter', 'category': 'placement'},

    # AN — соединения (8)
    'connect_weld':           {'fn': 'connect_weld',           'category': 'joint'},
    'connect_hinge':          {'fn': 'connect_hinge',          'category': 'joint'},
    'connect_ball':           {'fn': 'connect_ball',           'category': 'joint'},
    'connect_prismatic':      {'fn': 'connect_prismatic',      'category': 'joint'},
    'connect_cylindrical':    {'fn': 'connect_cylindrical',    'category': 'joint'},
    'connect_rope':           {'fn': 'connect_rope',           'category': 'joint'},
    'connect_spring':         {'fn': 'connect_spring',         'category': 'joint'},
    'connect_weldconstraint': {'fn': 'connect_weldconstraint', 'category': 'joint'},

    # AL — сборки (6)
    'room':          {'fn': 'room',          'category': 'assembly'},
    'story':         {'fn': 'story',         'category': 'assembly'},
    'house_section': {'fn': 'house_section', 'category': 'assembly'},
    'tower':         {'fn': 'tower',         'category': 'assembly'},
    'mechanism':     {'fn': 'mechanism',     'category': 'assembly'},
    'nature':        {'fn': 'nature',        'category': 'assembly'},
}


def list_patterns():
    return REGISTRY


def count_by_category():
    counts = {}
    for meta in REGISTRY.values():
        cat = meta['category']
        counts[cat] = counts.get(cat, 0) + 1
    return counts


def count_all():
    return len(REGISTRY)
