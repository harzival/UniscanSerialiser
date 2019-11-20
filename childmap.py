import json
from pathlib import Path
from collections import namedtuple


class Vec3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return super().__init__(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return super().__init__(x, y, z)

    def transform_axis_z_up(self):
        x = self.x
        y = -self.z
        z = self.y
        return super().__init__(x, y, z)


class Tile:
    def __init__(self, box, pos):
        self.box = box
        self.pos = pos

    def get_obj_path(self, lod):
        return lod.dir / (
            str(self.pos.x)
            + "_"
            + str(self.pos.y)
            + "_"
            + str(self.pos.z)
            + ".obj"
        )

    def calc_geometry_bounding_box(self, lod):
        Point = namedtuple("Point", ["x", "y", "z"])
        min = Vec3(0, 0, 0)
        max = Vec3(0, 0, 0)
        vertex_count = 0
        for line in open(self.get_obj_path(lod), "r"):
            if line[:2] == "v ":
                vertex_values = line[2:].rstrip("\n").split(" ")
                vertex = Point(
                    float(vertex_values[0]),
                    float(vertex_values[1]),
                    float(vertex_values[2]),
                )
                vertex_count += 1
                if vertex_count == 1:
                    min = Vec3(vertex.x, vertex.y, vertex.z)
                    max = Vec3(vertex.x, vertex.y, vertex.z)
                else:
                    if vertex.x > max.x:
                        max.x = vertex.x
                    if vertex.y > max.y:
                        max.y = vertex.y
                    if vertex.z > max.z:
                        max.z = vertex.z
                    if vertex.x < min.x:
                        min.x = vertex.x
                    if vertex.y < min.y:
                        min.y = vertex.y
                    if vertex.z < min.z:
                        min.z = vertex.z
        return Box(min, max)


class Box:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    @classmethod
    def from_joining_box_list(cls, box_list):
        min = Vec3(0, 0, 0)
        max = Vec3(0, 0, 0)
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
        return cls(min, max)


class Lod:
    def __init__(self, dir):
        self.dir = dir
        self.box = None
        self.slices = None
        self.tile_list = []


def slice_line(min, max, slices):
    slice_length = (max - min) / slices
    return [
        [min + (slice * slice_length), min + (slice + 1) * slice_length]
        for slice in range(slices)
    ]


def slice_box_into_tiles(box, slices):
    return [
        Tile(
            Box(Vec3(x[0], y[0], z[0]), Vec3(x[1], y[1], z[1])),
            Vec3(ix, iy, iz),
        )
        for ix, x in enumerate(slice_line(box.min.x, box.max.x, slices.x))
        for iy, y in enumerate(slice_line(box.min.y, box.max.y, slices.y))
        for iz, z in enumerate(slice_line(box.min.z, box.max.z, slices.z))
    ]


def print_lod_details(lod_list, num_cols):
    lod_list_of_detail_lists = []
    col_length = 0
    tile_name_length = 0
    for lod in lod_list:
        for j, tile in enumerate(lod.tile_list):
            tile_name = (
                str(format(j+1, "05d"))
                + ". "
                + str(tile.pos.x)
                + "_"
                + str(tile.pos.y)
                + "_"
                + str(tile.pos.z)
            )
            if len(tile_name) > tile_name_length:
                tile_name_length = len(tile_name)

    for lod in lod_list:
        tile_detail_list = []
        for j, tile in enumerate(lod.tile_list):
            tile_name = (
                str(format(j+1, "05d"))
                + ". "
                + str(tile.pos.x)
                + "_"
                + str(tile.pos.y)
                + "_"
                + str(tile.pos.z)
            )
            geom_box = tile.calc_geometry_bounding_box(lod)
            for i in range(tile_name_length - len(tile_name)):
                tile_name += " "
            w = str(round(abs(geom_box.min.x - geom_box.max.x), 1))
            d = str(round(abs(geom_box.min.y - geom_box.max.y), 1))
            h = str(round(abs(geom_box.min.z - geom_box.max.z), 1))
            tile_detail_list.append(
                "|| " + tile_name + "  " + w + " × " + d + " × " + h + " "
            )
        for detail in tile_detail_list:
            if len(detail) > col_length:
                col_length = len(detail)
        lod_list_of_detail_lists.append(tile_detail_list)

    for id, lod in enumerate(lod_list):
        w = str(
            round(
                abs(lod.tile_list[0].box.min.x - lod.tile_list[0].box.max.x), 1
            )
        )
        d = str(
            round(
                abs(lod.tile_list[0].box.min.y - lod.tile_list[0].box.max.y), 1
            )
        )
        h = str(
            round(
                abs(lod.tile_list[0].box.min.z - lod.tile_list[0].box.max.z), 1
            )
        )
        spacer1 = (
            "[ "
            + lod.dir.name
            + " | sliced into a "
            + str(lod.slices.x)
            + " × "
            + str(lod.slices.y)
            + " × "
            + str(lod.slices.z)
            + " 3D grid of tiles, each "
            + w
            + " × "
            + d
            + " × "
            + h
            + " in size | number of tiles containing data: "
            + str(len(lod.tile_list))
            + " ] "
        )
        spacer = spacer1
        spacer2 = ""
        for i in range(col_length * num_cols - (len(spacer) + 7)):
            spacer1 += "-"
            spacer2 += "_"
        for i in range((len(spacer) + 5)):
            spacer2 += "_"
        print(" ")
        print(spacer1)
        print(spacer2)
        print_count = 0
        print_buffer = ""
        for detail in lod_list_of_detail_lists[id]:
            print_count += 1
            if print_count > num_cols:
                print_count = 0
                print(print_buffer)
                print_buffer = ""
            else:
                print_buffer += detail
                if len(detail) < col_length:
                    for i in range(col_length - len(detail)):
                        print_buffer += " "
        if print_count > 0:
            print(print_buffer)


obj_root_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tiler-obj"
)

lod_list = [Lod(dir) for dir in obj_root_dir.iterdir() if dir.is_dir()]

for lod in lod_list:
    metadata_path = lod.dir / "metadata.json"
    tile_exists_list = []
    if metadata_path.exists():
        with open(metadata_path, "r") as file:
            json_dict = json.load(file)
            min = json_dict["WorldBounds"]["MinCorner"]
            max = json_dict["WorldBounds"]["MaxCorner"]
            lod.box = Box(
                Vec3(min["X"], min["Y"], min["Z"]),
                Vec3(max["X"], max["Y"], max["Z"]),
            )
            setsize = json_dict["SetSize"]
            lod.slices = Vec3(setsize["X"], setsize["X"], setsize["X"])
            tile_exists_list = json_dict["CubeExists"]
    tile_list = slice_box_into_tiles(lod.box, lod.slices)
    for tile in tile_list:
        if tile_exists_list[tile.pos.x][tile.pos.y][tile.pos.z]:
            lod.tile_list.append(tile)

world_box = Box.from_joining_box_list([lod.box for lod in lod_list])

print_lod_details(lod_list, 6)