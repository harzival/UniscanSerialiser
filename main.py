from box import Box
from obj import Obj
from lod import Lod
from tileset import Tile, RootTile, Tileset
from misc import create_dir_if_absent
import os
import json

obj_root_path = (
    "C:/Users/harzival/Desktop"
    "/uniscanTo3DTiles/html-src"
    "/dog/obj"
)
glb_root_path = (
    "C:/Users/harzival/Desktop"
    "/uniscanTo3DTiles/html-src"
    "/dog/glb"
)
b3dm_root_path = (
    "C:/Users/harzival/Desktop"
    "/uniscanTo3DTiles/html-src"
    "/dog/tileset"
)

<<<<<<< HEAD
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
=======
def main():
    obj_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/dog/obj"
    )
    glb_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/dog/glb"
    )
    b3dm_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/html-src"
        "/tileset-example"
    )
>>>>>>> origin/master

def main():
    create_dir_if_absent(glb_root_path)
    create_dir_if_absent(b3dm_root_path)
    
    lod_list = Lod.get_lod_list(obj_root_path, [1000,100,10])
    for i, lod in enumerate(lod_list):
        lod.populate_obj_list()
        for obj in lod.obj_list:
            obj.write_new_mtl_data()
            create_dir_if_absent(os.path.join(glb_root_path, obj.lod_dir_name))
            glb = obj.convert_to_glb(glb_root_path)
            create_dir_if_absent(os.path.join(b3dm_root_path, glb.lod_dir_name))
            b3dm = glb.convert_to_b3dm(b3dm_root_path)
            box = obj.calc_geometry_bounding_box()
            tile = Tile(box, lod.geometric_error, b3dm, [])
            lod.tile_list.append(tile)
            lod_list[i] = lod

    tile_list = Lod.sort_tiles_into_tree_heirarchy(lod_list)
    root_box = Box.create_parent_box_from_box_list(
        [tile.box for tile in tile_list]
    )
    root_tile = RootTile(root_transform, root_box, 10000, tile_list)
    tileset = Tileset("1.0", 100000, root_tile)
    with open(os.path.join(b3dm_root_path, "tileset.json"), 'w') as file:
        json.dump(dict(tileset), file, indent=2)

main()
