from box import Box
from obj import Obj
from tileset import Tile, RootTile, Tileset
from misc import create_dir_if_absent
import os
import json


def main():
    obj_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/roompart/obj"
    )
    glb_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/roompart/glb"
    )
    b3dm_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/roompart/b3dm"
    )

    create_dir_if_absent(glb_root_path)
    create_dir_if_absent(b3dm_root_path)

    obj_list = Obj.get_obj_list_from_root_path(obj_root_path)

    lod_dict = {
        "L1": {"error": 1000, "order": 1, "tile_list": []},
        "L2": {"error": 100, "order": 2, "tile_list": []},
        "L3": {"error": 10, "order": 3, "tile_list": []},
    }

    for obj in obj_list:
        obj.write_new_mtl_data()
        create_dir_if_absent(os.path.join(glb_root_path, obj.lod_dir_name))
        glb = obj.convert_to_glb(glb_root_path)
        create_dir_if_absent(os.path.join(b3dm_root_path, glb.lod_dir_name))
        b3dm = glb.convert_to_b3dm(b3dm_root_path)
        box = obj.calc_geometry_bounding_box()
        lod_dict[b3dm.lod_dir_name]["tile_list"].append(
            Tile(box, lod_dict[b3dm.lod_dir_name]["error"], b3dm, [])
        )

    tile_list = []
    lod_list = list(lod_dict.keys())

    for i, lod_name in reversed(list(enumerate(lod_list))):
        if i != 0:
            parent_lod_name = lod_list[i - 1]
            for tile in lod_dict[lod_name]["tile_list"]:
                for parent_tile in lod_dict[parent_lod_name]["tile_list"]:
                    if parent_tile.name == tile.name:
                        parent_tile.child_tile_list.append(tile)
        else:
            for tile in lod_dict[lod_name]["tile_list"]:
                tile_list.append(tile)

    root_transform = [
        96.86356343768793,
        24.848542777253734,
        0,
        0,
        -15.986465724980844,
        62.317780594908875,
        76.5566922962899,
        0,
        19.02322243409411,
        -74.15554020821229,
        64.3356267137516,
        0,
        1215107.7612304366,
        -4736682.902037748,
        4081926.095098698,
        1,
    ]
    root_box = Box.create_parent_box_from_box_list(
        [tile.box for tile in tile_list]
    )

    root_tile = RootTile(root_transform, root_box, 10000, tile_list)

    tileset = Tileset("1.0", 100000, root_tile)

    with open(os.path.join(b3dm_root_path, "tileset.json"), 'w') as file:
        json.dump(dict(tileset), file, indent=2)


main()
