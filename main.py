from box import Box
from lod import Lod
from tileset import Tile, RootTile, Tileset
from misc import create_dir_if_absent
import os
import argparse
import logging
import json

obj_root_path = (
    "C:/Users/harzival/Desktop" "/uniscanTo3DTiles/html-src" "/dog/obj"
)
glb_root_path = (
    "C:/Users/harzival/Desktop" "/uniscanTo3DTiles/html-src" "/dog/glb"
)
b3dm_root_path = (
    "C:/Users/harzival/Desktop" "/uniscanTo3DTiles/html-src" "/dog/tileset"
)

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


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    create_dir_if_absent(glb_root_path)
    create_dir_if_absent(b3dm_root_path)

    lod_list = Lod.get_lod_list(obj_root_path, [1000, 100, 10])
    for i, lod in enumerate(lod_list):
        lod.populate_obj_list()
        for obj in lod.obj_list:
            obj.write_new_mtl_data()
            create_dir_if_absent(os.path.join(glb_root_path, obj.lod_dir_name))
            glb = obj.convert_to_glb(glb_root_path)
            create_dir_if_absent(
                os.path.join(b3dm_root_path, glb.lod_dir_name)
            )
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
    with open(os.path.join(b3dm_root_path, "tileset.json"), "w") as file:
        json.dump(dict(tileset), file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TilesetExporter",
        epilog="Creates a Tileset that complies with the "
        "3D Tiles' standard from a collection of OBJ meshes.",
        fromfile_prefix_chars="@",
    )
    # TODO Specify your real parameters here.

    parser.add_argument(
        "input",
        type=str,
        help="Path to root of directory containing list of OBJ mesh files",
    )

    parser.add_argument(
        "output",
        type=str,
        help="Path to directory where the output tilese"
        "t.json and .b3dm mesh files should placed",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Set logging show debug messages.",
        action="store_true",
    )

    parser.add_argument(
        "-rt",
        "--root-transform",
        type=float,
        nargs=16,
        metavar=0,
        help="A transform on earth's surface specified with 16 f"
        "loats as per the 3D Tiles' standard's Transform",
        required=True,
    )

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)

# [ 'LOD_ORDER', 'LOD_DIR', 'GEOM_ERROR', 'CHILD_TILE_COUNT' ]
