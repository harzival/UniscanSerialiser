from os import path


class B3dm:
    def __init__(self, root_path=None, lod_dir_name=None, file_name=None):
        self.root_path = root_path
        self.lod_dir_name = lod_dir_name
        self.file_name = file_name
        self.tile_name = file_name.split(".")[0]
        self.path = path.join(root_path, lod_dir_name, file_name)
        self.box = None
