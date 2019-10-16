"""Single class Box, a data structure & tools to store & create tile bounds."""
from vec3 import Vec3


class Box:
    """Implements data structure and tools to store and create tile bounds.

    Implements a data structure to store the bounds of a mesh in 3D Tiles'
    own Tile bounding box format; tools to convert between bounding box
    representations or create a bounding box which encapsulates a list of
    Box objects' bounding boxes.

    Attributes:
        data (:obj:`list` of :obj:`float`): 12 values that describe an axis
            aligned bounding box which conforms to the 3D Tiles' specification.
        mid (Vec3): 3D point describing the center of the bounding box.



    """

    def __init__(self, data=[0] * 12):
        self.data = data
        self.mid = Vec3(data[0], data[1], data[2])
        self.x_dist = Vec3(data[3], data[4], data[5])
        self.y_dist = Vec3(data[6], data[7], data[8])
        self.z_dist = Vec3(data[9], data[10], data[11])
        self.min = self.mid - self.x_dist - self.y_dist - self.z_dist
        self.max = self.mid + self.x_dist + self.y_dist + self.z_dist
        self.width = abs(self.min.x - self.max.x)
        self.depth = abs(self.min.y - self.max.y)
        self.height = abs(self.min.z - self.max.z)
        self.x_bound_point = self.mid + self.x_dist
        self.y_bound_point = self.x_bound_point + self.y_dist
        self.z_bound_point = self.y_bound_point + self.z_dist
        self.side_points = self.calc_side_points(self.min, self.max, self.mid)
        self.corner_points = self.calc_corner_points(self.min, self.max)

    def calc_side_points(self, min, max, mid):
        return [
            Vec3(min.x, mid.y, mid.z),  # Side 1
            Vec3(mid.x, min.y, mid.z),  # Side 2
            Vec3(mid.x, mid.y, min.z),  # Side 3
            Vec3(max.x, mid.y, mid.z),  # Side 4
            Vec3(mid.x, max.y, mid.z),  # Side 5
            Vec3(mid.x, mid.y, max.z),
        ]  # Side 6

    def calc_corner_points(self, min, max):
        return [
            Vec3(min.x, min.y, min.z),  # Corner 1
            Vec3(min.x, max.y, min.z),  # Corner 2
            Vec3(min.x, min.y, max.z),  # Corner 3
            Vec3(min.x, max.y, max.z),  # Corner 4
            Vec3(max.x, min.y, min.z),  # Corner 5
            Vec3(max.x, max.y, min.z),  # Corner 6
            Vec3(max.x, min.y, max.z),  # Corner 7
            Vec3(max.x, max.y, max.z),
        ]

    @classmethod
    def create_from_min_max(cls, min, max):
        center = Vec3(
            (min.x + max.x) / 2.0, (min.y + max.y) / 2.0, (min.z + max.z) / 2.0
        )
        return cls(
            [
                center.x,
                center.y,
                center.z,
                abs(min.x - max.x) / 2,
                0,
                0,
                0,
                abs(min.y - max.y) / 2,
                0,
                0,
                0,
                abs(min.z - max.z) / 2,
            ]
        )

    @classmethod
    def create_parent_box_from_box_list(cls, box_list):
        min = Vec3.zero
        max = Vec3.zero
        for i, box in enumerate(box_list):
            if i == 0:
                min = box.min
                max = box.max
            else:
                if box.max.x > max.x:
                    max.x = box.max.x
                if box.max.y > max.y:
                    max.y = box.max.y
                if box.max.z > max.z:
                    max.z = box.max.z
                if box.min.x < min.x:
                    min.x = box.min.x
                if box.min.y < min.y:
                    min.y = box.min.y
                if box.min.z < min.z:
                    min.z = box.min.z
        return cls.create_from_min_max(min, max)
