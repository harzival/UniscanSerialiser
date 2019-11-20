from box import Box
from vec3 import Vec3
import json
from pathlib import Path
from box_plotter import BoxPlotter


def box_tiler(box, x_parts, y_parts, z_parts):
    box_list = []

    def split_line(a, b, n):
        d = abs(b - a) / n
        return [(i * d, (i + 1) * d) for i in range(n)]
    for w in split_line(box.min.x, box.max.x, x_parts):
        for d in split_line(box.min.y, box.max.y, y_parts):
            for h in split_line(box.min.z, box.max.z, z_parts):
                box_list.append(Box.create_from_min_max(
                    Vec3(w[0], d[0], h[0]),
                    Vec3(w[1], d[1], h[1])))
    return box_list


def subdir_list(p):
    return [x for x in p.iterdir() if x.is_dir()]


obj_root_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tiler-obj"
)

lod_dir_list = subdir_list(obj_root_dir)

metadata_path_list = []

for lod_dir in lod_dir_list:
    metadata_path = lod_dir / "metadata.json"
    if metadata_path.exists():
        metadata_path_list.append(metadata_path)

world_box_list = []
lod_setsize_list = []

for metadata_path in metadata_path_list:
    with open(metadata_path, "r") as file:
        metadata_dict = json.load(file)
        bounds_dict = metadata_dict["WorldBounds"]
        min = Vec3(
            bounds_dict["XMin"], bounds_dict["YMin"], bounds_dict["ZMin"]
        )
        max = Vec3(
            bounds_dict["XMax"], bounds_dict["YMax"], bounds_dict["ZMax"]
        )
        world_box = Box.create_from_min_max(min, max)
        world_box_list.append(world_box)
        setsize = Vec3(
            metadata_dict["SetSize"]["X"],
            metadata_dict["SetSize"]["Y"],
            metadata_dict["SetSize"]["Z"])
        lod_setsize_list.append(setsize)

world_box = Box.create_parent_box_from_box_list(world_box_list)

box_list = Box.tiler(world_box, 3, 3, 3)

plotter = BoxPlotter()
plotter.set_plot_size_limit_box(world_box)
for box in box_list:
    plotter.draw_edges(box)
plotter.draw_edges(world_box)
plotter.start()


# class Lod:
#     def __init__(self, lod_dir_path):
#         self.lod_dir_path = lod_dir_path
#         self.box_list


# def subdivide_line(a, b, n):
#     length = abs(b - a) / n
#     return [(i * length, (i + 1) * length) for i in range(n)]


# def subdivide_box(min, max):
#     box_list = []
#     width_list = subdivide_line(min.x, max.x, 4)
#     depth_list = subdivide_line(min.y, max.y, 3)
#     height_list = subdivide_line(min.z, max.z, 2)
#     for width in width_list:
#         for depth in depth_list:
#             for height in height_list:
#                 min = Vec3(width[0], depth[0], height[0])
#                 max = Vec3(width[1], depth[1], height[1])
#                 box = Box.create_from_min_max(min, max)
#                 box_list.append(box)
#     return box_list


# min = Vec3(0, 0, 0)
# max = Vec3(2, 2, 2)
# box = Box.create_from_min_max(min, max)
# box_list = subdivide_box(box.min, box.max)
# plotter = BoxPlotter()
# plotter.set_plot_size_limit_box(box)
# for box in box_list:
#     plotter.draw_edges(box)
# plotter.start()


# subdivide_box(min, max)

# min = [0, 0]
# max = [2, 2]

# plane_list = []


# def subdivide_plane(min, max):
#     width = abs(max[0] - min[0]) / 3
#     depth = abs(max[1] - min[1]) / 2
#     width_list = [(i * width, (i + 1) * width) for i in range(3)]
#     for width in width_list:
#         depth_list = [(i * depth, (i + 1) * depth) for i in range(2)]
#         for depth in depth_list:
#             plane_list.append([[width[0], depth[0]], [width[1], depth[1]]])


# subdivide_plane(min, max)
# print(plane_list)
