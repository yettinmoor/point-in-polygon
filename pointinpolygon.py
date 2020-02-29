import math


def point_in_polygon(point, polygon):
    oldvec = normdir(point, polygon[0])
    rotation = 0.0
    for lp in polygon[1:]:
        vec = normdir(point, lp)
        rotation += vector_angle(oldvec, vec)
        oldvec = vec
    return abs(rotation) > math.pi


def normdir(p, q):
    x, y = q[0] - p[0], q[1] - p[1]
    mag = math.sqrt(x**2 + y**2)
    return x / mag, y / mag


def vector_angle(p, q):
    x1, y1 = p
    x2, y2 = q
    dot = x1 * x2 + y1 * y2
    orientation = 1 if x1 * y2 - y1 * x2 > 0 else -1
    return math.acos(dot) * orientation


def import_map():
    def neighbors(x, y):
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if (nx != x or ny != y):
                    yield nx, ny

    polygon = []
    points = dict()
    with open('map.txt') as f:
        txtmap = f.readlines()

    startpoint_found = False
    for y, row in enumerate(txtmap):
        for x, tile in enumerate(row.strip()):
            if tile == 'l' and not startpoint_found:
                curpoint = startpoint = x, y
                startpoint_found = True
            elif tile not in '.l':
                points[tile] = (x, y)

    while True:
        polygon.append(curpoint)
        for nx, ny in neighbors(*curpoint):
            if txtmap[ny][nx] == 'l' and (nx, ny) not in polygon[-2:]:
                curpoint = nx, ny
                break
        if (curpoint == startpoint):
            break

    return points, polygon


points, polygon = import_map()
for name, point in sorted(points.items()):
    in_polygon = point_in_polygon(point, polygon)
    print(f"{name}: {in_polygon}")
