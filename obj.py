from subprocess import call
from os import path, listdir, scandir, remove
from collections import namedtuple
from glb import Glb
from vec3 import Vec3
from box import Box


class Obj(object):
    def __init__(self, root_path=None, lod_dir_name=None, file_name=None):
        self.root_path = root_path
        self.lod_dir_name = lod_dir_name
        self.file_name = file_name
        self.tileName = file_name.split(".")[0]
        self.path = path.join(root_path, lod_dir_name, file_name)
        self.glb_file_name = self.tileName + ".glb"
        self.gltf_file_name = self.tileName + ".gltf"
        self.albedo_map_path = path.join(
            root_path, lod_dir_name, (self.tileName + "_albedo.jpg")
        )
        self.normal_map_path = path.join(
            root_path, lod_dir_name, (self.tileName + "_normal.jpg")
        )
        self.glb = None

    def convert_to_glb(self, glb_root_path):
        call(
            [
                "node",
                "C:/Users/harzival/Desktop/"
                "uniscanTo3DTiles/dependencies/obj2gltf/bin/obj2gltf.js",
                "--binary",
                "--unlit",
                "-i",
                self.path,
                "--baseColorTexture",
                self.albedo_map_path,
                "--normalTexture",
                self.normal_map_path,
                "-o",
                path.join(
                    glb_root_path, self.lod_dir_name, self.glb_file_name
                ),
            ]
        )
        self.glb = Glb(glb_root_path, self.lod_dir_name, self.glb_file_name)
        return self.glb

    def convert_to_gltf(self, obj, glb_root_path):
        call(
            [
                "node",
                "C:/Users/harzival/Desktop/"
                "uniscanTo3DTiles/dependencies/obj2gltf/bin/obj2gltf.js",
                "--unlit",
                "-i",
                self.path,
                "--baseColorTexture",
                self.albedo_map_path,
                "--normalTexture",
                self.normal_map_path,
                "-o",
                path.join(
                    glb_root_path, self.lod_dir_name, self.gltf_file_name
                ),
            ]
        )
        self.glb = Glb(glb_root_path, self.lod_dir_name, self.glb_file_name)
        return self.glb

    @staticmethod
    def get_obj_list_from_root_path(root_path):
        obj_list = []
        for lod_dir in scandir(root_path):
            for file_name in listdir(lod_dir):
                if file_name.endswith(".obj"):
                    obj = Obj(root_path, lod_dir.name, file_name)
                    print(
                        "UNISCAN: Adding tile"
                        " {0} from {1} to the serialiser queue.".format(
                            obj.tileName, obj.lod_dir_name
                        )
                    )
                    obj_list.append(obj)
        return obj_list

    def get_mtl_data(self):
        opened_obj_file = open(self.path)
        # Get the line in the mesh's file which starts with "usemtl ".
        # Return a string containing the line without the "usemtl " prefix.
        for i, line in enumerate(opened_obj_file):
            if line.startswith("usemtl"):
                mtl_data = "newmtl {0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(
                    line.replace("usemtl ", "").rstrip("\n"),
                    "Ka 1 1 1",
                    "Kd 1 1 1",
                    "d 1",
                    "Ns 0",
                    "illum 1",
                )
                opened_obj_file.close()
                return mtl_data

    def write_new_mtl_data(self):
        mtl_path = self.path.replace(".obj", ".mtl")
        if path.exists(mtl_path):
            print(
                "UNISCAN: MTL file for OBJ already exists,"
                " will now delete and recreate it."
            )
            remove(mtl_path)
        else:
            print(
                "UNISCAN: MTL file for OBJ does not exist,"
                " will now create it."
            )
        try:
            mtl_file = open(mtl_path, "x")
            mtl_file.write(self.get_mtl_data())
            mtl_file.close()
        except IOError as error:
            print(error)
        except Exception:
            print("UNISCAN: Unknown error creating MTL")

    def calc_geometry_bounding_box(self):
        Point = namedtuple("Point", ["x", "y", "z"])
        min = Vec3.zero
        max = Vec3.zero
        vertex_count = 0
        for line in open(self.path, "r"):
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
        return Box.create_from_min_max(
            min.transform_axis_z_up(), max.transform_axis_z_up()
        )
