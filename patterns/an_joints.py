# ============================================================
# patterns/an_joints.py — СОЕДИНЕНИЯ (270–277)
# Protocol 4.2.0
# Соединения создаются как Empty-объекты с метаданными.
# При экспорте в Studio — преобразуются в Constraints.
# ============================================================
import bpy


def _make_joint(name, joint_type, part0, part1, **props):
    """Создаёт Empty-маркер соединения с метаданными."""
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'SPHERE'
    empty.empty_display_size = 0.2
    bpy.context.collection.objects.link(empty)
    empty['joint_type'] = joint_type
    empty['part0'] = part0
    empty['part1'] = part1
    for k, v in props.items():
        if v is not None:
            empty[k] = v
    return empty


def connect_weld(name, part0, part1):
    """[270] Weld — жёсткое соединение."""
    return _make_joint(name, 'Weld', part0, part1)


def connect_hinge(name, part0, part1, actuator='Motor',
                  torque=10000, velocity=0, limits=None):
    """[271] Hinge. actuator='Motor'|'Servo'."""
    props = {'actuator': actuator, 'torque': torque, 'velocity': velocity}
    if limits:
        props['limits'] = list(limits)
    return _make_joint(name, 'Hinge', part0, part1, **props)


def connect_ball(name, part0, part1):
    """[272] BallSocket."""
    return _make_joint(name, 'BallSocket', part0, part1)


def connect_prismatic(name, part0, part1, limits=None):
    """[273] Prismatic — линейное движение."""
    return _make_joint(name, 'Prismatic', part0, part1,
                       limits=list(limits) if limits else None)


def connect_cylindrical(name, part0, part1):
    """[274] Cylindrical — вращение + скольжение."""
    return _make_joint(name, 'Cylindrical', part0, part1)


def connect_rope(name, part0, part1, length, thickness=0.05,
                 color=(0.6, 0.5, 0.3)):
    """[275] Rope. Правило 173: только существующие свойства."""
    return _make_joint(name, 'Rope', part0, part1,
                       length=length, thickness=thickness,
                       visible=True, color=list(color),
                       restitution=0.0, friction=0.0,
                       current_length=length)


def connect_spring(name, part0, part1, stiffness=1000, damping=100):
    """[276] Spring."""
    return _make_joint(name, 'Spring', part0, part1,
                       stiffness=stiffness, damping=damping)


def connect_weldconstraint(name, part0, part1):
    """[277] WeldConstraint — для Tool."""
    return _make_joint(name, 'WeldConstraint', part0, part1)


def collect_joints():
    """Возвращает все Empty-соединения в сцене."""
    return [o for o in bpy.data.objects
            if o.type == 'EMPTY' and 'joint_type' in o]
