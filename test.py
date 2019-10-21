from box import Box
from obj import Obj

path = "C:/Users/harzival/Desktop/uniscanTo3DTiles/html-src/Tileset"
lod_dir_name = ""
name = "1_1_2.obj"

obj = Obj(path, lod_dir_name, name)

box = obj.calc_geometry_bounding_box()

print(box.data)

print(dict(box))





