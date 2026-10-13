# ============================================================
# patterns/am_placement.py — РАЗМЕЩЕНИЯ (263–269)
# Protocol 4.2.0
# ============================================================
import math
import random


def place_linear(start, step, n):
    """[263] pos_i = start + i * step."""
    return [(start[0] + i*step[0],
             start[1] + i*step[1],
             start[2] + i*step[2]) for i in range(n)]


def place_radial(center, R, n, axis='xz'):
    """[264] R*cos/sin. Возвращает (positions, angles)."""
    positions, angles = [], []
    for i in range(n):
        a = i * 2 * math.pi / n
        if axis == 'xz':
            positions.append((center[0] + R*math.cos(a), center[1],
                              center[2] + R*math.sin(a)))
        else:
            positions.append((center[0] + R*math.cos(a),
                              center[1] + R*math.sin(a), center[2]))
        angles.append(math.degrees(a))
    return positions, angles


def place_grid(start, sx, sz, nx, nz):
    """[265] 2D сетка."""
    return [(start[0] + i*sx, start[1], start[2] + j*sz)
            for j in range(nz) for i in range(nx)]


def place_spiral(center, R, n, step_h):
    """[266] Спираль."""
    return [(center[0] + R*math.cos(i*2*math.pi/n),
             center[1] + R*math.sin(i*2*math.pi/n),
             center[2] + i*step_h) for i in range(n)]


def place_mirror(pos, axis='x'):
    """[267] Зеркало по X/Y/Z."""
    x, y, z = pos
    if axis == 'x':
        return (-x, y, z)
    if axis == 'y':
        return (x, -y, z)
    if axis == 'z':
        return (x, y, -z)
    return pos


def place_bezier(p0, p1, p2, n):
    """[268] Кривая Безье (квадратичная)."""
    pts = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        z = (1-t)**2 * p0[2] + 2*(1-t)*t * p1[2] + t**2 * p2[2]
        pts.append((x, y, z))
    return pts


def place_jitter(base, delta, n, seed=None):
    """[269] Случайное смещение."""
    if seed is not None:
        random.seed(seed)
    return [(base[0] + random.uniform(-delta, delta),
             base[1] + random.uniform(-delta, delta),
             base[2] + random.uniform(-delta, delta)) for _ in range(n)]
