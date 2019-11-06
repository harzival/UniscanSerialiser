from os import path, listdir, scandir, remove
from obj import Obj

class Lod(object):
    def __init__(self, lod_dir_name=None, geometric_error=None, obj_root_path=None):
        self.lod_dir_name = lod_dir_name
        self.geometric_error = geometric_error
        self.obj_root_path = obj_root_path
        self.obj_list = []
        self.tile_list = []
    
    @staticmethod
    def get_lod_list (root_path, geometric_error_list):
        lod_list = []
        for i, lod_dir in enumerate(scandir(root_path)):
            lod_list.append(Lod(lod_dir.name, geometric_error_list[i], root_path))
        return lod_list

    def populate_obj_list(self):
        self.obj_list = Obj.get_obj_list_from_lod_path(self.obj_root_path, self.lod_dir_name)
        return self

    @staticmethod
    def sort_tiles_into_tree_heirarchy (lod_list):
        tile_list = []
        for i, lod in reversed(list(enumerate(lod_list))):
            if i !=0:
                parent_lod = lod_list[i - 1]
                for tile in lod.tile_list:
                    for parent_tile in parent_lod.tile_list:
                        if parent_tile.name == tile.name:
                            parent_tile.child_tile_list.append(tile)
            else:
                for tile in lod.tile_list:
                    tile_list.append(tile)
        return tile_list