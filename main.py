from box import Box
from obj import Obj
from boxPlotter import BoxPlotter
from misc import create_dir_if_absent
import os


def main():
    obj_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/development-mesh-data"
        "/testing/obj"
    )
    glb_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/development-mesh-data"
        "/testing/glb"
    )
    b3dm_root_path = (
        "C:/Users/harzival/Desktop"
        "/uniscanTo3DTiles/development-mesh-data"
        "/testing/b3dm"
    )

    create_dir_if_absent(glb_root_path)
    create_dir_if_absent(b3dm_root_path)

    obj_list = Obj.get_obj_list_from_root_path(obj_root_path)
    box_list = []

    for obj in obj_list:
        obj.write_new_mtl_data()
        create_dir_if_absent(os.path.join(glb_root_path, obj.lod_dir_name))
        obj.convert_to_glb(glb_root_path)
        create_dir_if_absent(
            os.path.join(b3dm_root_path, obj.glb.lod_dir_name)
        )
        obj.glb.convert_to_b3dm(b3dm_root_path)
        obj.glb.b3dm.box = obj.calc_geometry_bounding_box()
        box_list.append(obj.glb.b3dm.box)

    world_box = Box.create_parent_box_from_box_list(box_list)

    plotter = BoxPlotter()
    # plotter.set_plot_size_limit_box ( world_box )
    plotter.draw_edges(world_box)
    plotter.draw_edges(obj_list[0].glb.b3dm.box)
    plotter.start()


main()
