#!/usr/bin/env python3
# ============================================================
# rbxgen.py — CLI генератор Roblox-объектов
# Protocol 4.2.0
# Использование:
#   blender --background --python rbxgen.py -- list
#   blender --background --python rbxgen.py -- <preset_name>
#   blender --background --python rbxgen.py -- custom '<json>'
# ============================================================
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
from core.scene import (clear_scene, setup_units, add_uv_smart,
                        join_objects, count_tris)
from core.export import export_fbx
from core.validator import validate
from core.report import write_report
from core.materials import assign as assign_mat
import patterns
from patterns import REGISTRY


def build_from_preset(preset_name):
    """Загружает presets/<name>.json и собирает объект."""
    path = os.path.join(
        os.path.dirname(__file__), 'presets', f"{preset_name}.json")
    if not os.path.exists(path):
        print(f"[E] Preset not found: {path}")
        sys.exit(1)
    with open(path, encoding='utf-8') as f:
        spec = json.load(f)
    return build_from_spec(spec)


def build_from_spec(spec):
    """spec = {name, level, budget_tris, origin_mode, nodes, joints}."""
    name = spec['name']
    origin_mode = spec.get('origin_mode', 'CENTER')
    nodes = spec['nodes']
    joints_spec = spec.get('joints', [])

    all_parts = []

    for node in nodes:
        fn_name = node['fn']
        if fn_name not in REGISTRY:
            print(f"[E] Unknown pattern: {fn_name}")
            continue
        args = node.get('args', [])
        kwargs = node.get('kwargs', {})
        node_name = node.get('name',
                             f"{name}_{fn_name}_{len(all_parts)}")
        mat_name = node.get('material')

        fn = getattr(patterns, REGISTRY[fn_name]['fn'])
        try:
            ob = fn(node_name, *args, **kwargs)
            all_parts.append(ob)
            if mat_name:
                assign_mat(ob, mat_name)
            print(f"[OK] {node_name} = {fn_name} mat={mat_name}")
        except Exception as e:
            print(f"[E] {node_name}: {e}")

    # Соединения
    joints = []
    for j in joints_spec:
        jfn = getattr(patterns, REGISTRY[j['fn']]['fn'])
        jargs = j.get('args', [])
        jkwargs = j.get('kwargs', {})
        joint = jfn(j['name'], *jargs, **jkwargs)
        joints.append(joint)
        print(f"[OK] Joint: {j['name']} type={joint['joint_type']}")

    # Сборка
    final = join_objects(all_parts, name, origin_mode=origin_mode)
    add_uv_smart(final)

    return final, spec, joints


def process_object(ob, spec, joints=None):
    """Валидация + экспорт + отчёт."""
    level = spec.get('level', 'BASE')
    budget = spec.get('budget_tris', 5000)

    result = validate(ob, level=level, budget_tris=budget)
    tris = result['tris']

    print(f"\n[VALIDATOR] level={level}, tris={tris}/{budget}")
    for code, msg in result['errors']:
        print(f"  [E] {code}: {msg}")
    for code, msg in result['warns']:
        print(f"  [W] {code}: {msg}")
    print(f"[VALIDATOR] status: {result['status']}\n")

    fbx_path = export_fbx([ob], spec['name'])

    report = {
        'name': spec['name'],
        'level': level,
        'budget_tris': budget,
        'actual_tris': tris,
        'origin_mode': spec.get('origin_mode', 'CENTER'),
        'patterns_used': [n['fn'] for n in spec['nodes']],
        'joints': [
            {'name': j.name, 'type': j['joint_type'],
             'part0': j['part0'], 'part1': j['part1']}
            for j in (joints or [])
        ],
        'validator': {
            'status': result['status'],
            'errors': result['errors'],
            'warns': result['warns'],
        },
        'fbx_path': fbx_path,
    }
    write_report(spec['name'], report)
    return report


def main():
    argv = sys.argv
    if '--' in argv:
        argv = argv[argv.index('--') + 1:]
    else:
        argv = []

    if not argv or argv[0] == 'list':
        print(f"[PATTERNS] Всего: {patterns.count_all()}")
        print(f"[CATEGORIES] {patterns.count_by_category()}")
        for name, meta in sorted(REGISTRY.items()):
            print(f"  {name:25s}  {meta['category']}")
        return

    cmd = argv[0]

    clear_scene()
    setup_units()

    if cmd == 'custom':
        if len(argv) < 2:
            print("[E] custom: нужен JSON")
            return
        spec = json.loads(argv[1])
        ob, spec, joints = build_from_spec(spec)
    else:
        ob, spec, joints = build_from_preset(cmd)

    process_object(ob, spec, joints)
    print(f"\n[DONE] {spec['name']}")


if __name__ == '__main__':
    main()
