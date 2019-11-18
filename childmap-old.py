from box import Box
from vec3 import Vec3
import json
from pathlib import Path
from box_plotter import BoxPlotter


def subdir_list(p):
    return [x for x in p.iterdir() if x.is_dir()]


obj_root_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tiler-obj"
)

lod_dir_list = subdir_list(obj_root_dir)

print(lod_dir_list)

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


def divide_box(box):
    a = box.min
    b = box.max
    c = box.mid

    return [
        box.create_from_min_max(Vec3(a.x, a.y, a.z), Vec3(c.x, c.y, c.z)),
        box.create_from_min_max(Vec3(c.x, a.y, a.z), Vec3(b.x, c.y, c.z)),
        box.create_from_min_max(Vec3(a.x, c.y, a.z), Vec3(c.x, b.y, c.z)),
        box.create_from_min_max(Vec3(c.x, c.y, a.z), Vec3(b.x, b.y, c.z)),
        box.create_from_min_max(Vec3(a.x, a.y, c.z), Vec3(c.x, c.y, b.z)),
        box.create_from_min_max(Vec3(c.x, a.y, c.z), Vec3(b.x, c.y, b.z)),
        box.create_from_min_max(Vec3(a.x, c.y, c.z), Vec3(c.x, b.y, b.z)),
        box.create_from_min_max(Vec3(c.x, c.y, c.z), Vec3(b.x, b.y, b.z)),
    ]


lod_box_list = divide_box(world_box)

plotter = BoxPlotter()
plotter.set_plot_size_limit_box(world_box)
for lod_box in lod_box_list:
    plotter.draw_edges(lod_box)
plotter.start()
