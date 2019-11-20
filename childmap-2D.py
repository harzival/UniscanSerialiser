import matplotlib.pyplot as plt


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)


class Plane:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = Vec2((a.x + b.x) / 2, (a.y + b.y) / 2)

    def corners(self):
        return [
            Vec2(self.a.x, self.a.y),
            Vec2(self.b.x, self.a.y),
            Vec2(self.b.x, self.b.y),
            Vec2(self.a.x, self.b.y),
        ]


ax = plt.axes()


def draw_plane(plane, color="black"):
    def draw_line(a, b):
        ax.plot([a.x, b.x], [a.y, b.y], color)

    pts = plane.corners()
    draw_line(pts[0], pts[1])
    draw_line(pts[1], pts[2])
    draw_line(pts[2], pts[3])
    draw_line(pts[3], pts[0])


plane = Plane(Vec2(3, 3), Vec2(1, 1))
draw_plane(plane)


def slice_line(a, b, n):
    d = (b - a) / n
    return [[a + (i * d), a + (i + 1) * d] for i in range(n)]


def slice_plane(p, nx, ny):
    return [
        Plane(Vec2(dx[0], dy[0]), Vec2(dx[1], dy[1]))
        for dy in slice_line(p.a.y, p.b.y, ny)
        for dx in slice_line(p.a.x, p.b.x, nx)
    ]



def tile_plane(plane, nx, ny):
    plane_list = []
    for dx in split_line(plane.a.x, plane.b.x, ny):
        for dy in split_line(plane.a.y, plane.b.y, ny):
            plane_list.append(Plane(Vec2(dx[0], dy[0]), Vec2(dx[1], dy[1])))
    return plane_list


for p in slice_plane(plane, 2, 2):
    draw_plane(p, "red")


plt.show()

