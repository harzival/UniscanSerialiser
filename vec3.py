class Vec3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.list = [x, y, z]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x, y, z)

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    @classmethod
    def one(cls):
        return cls(1, 1, 1)

    def transform_axis_z_up(self):
        old = self
        self.x = old.x
        self.y = -old.z
        self.z = old.y
        return self
