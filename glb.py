from subprocess import call
from os import path
from b3dm import B3dm


class Glb(object):
    def __init__(self, root_path=None, lod_dir_name=None, file_name=None):
        self.root_path = root_path
        self.lod_dir_name = lod_dir_name
        self.file_name = file_name
        self.tileName = file_name.split(".")[0]
        self.b3dm_file_name = self.tileName + ".b3dm"
        self.path = path.join(root_path, lod_dir_name, file_name)
        self.b3dm = None

    def convert_to_b3dm(self, b3dm_root_path):
        call(
            [
                "node",
                "C:/Users/harzival/Desktop/uniscanTo3DTiles"
                "/dependencies/3d-tiles-tools/"
                "tools/bin/3d-tiles-tools.js",
                "glbToB3dm",
                "--force",
                "-i",
                self.path,
                "-o",
                path.join(
                    b3dm_root_path, self.lod_dir_name, self.b3dm_file_name
                ),
            ]
        )
        self.b3dm = B3dm(
            b3dm_root_path, self.lod_dir_name, self.b3dm_file_name
        )
        return self.b3dm
