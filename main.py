from vec3 import Vec3
from box import Box
from obj import Obj
from glb import Glb
from boxPlotter import BoxPlotter
from b3dm import B3dm
from misc import createDirIfDoesNotExist

import os

def main ():
    objRootDirPath = "C:/Users/harzival/Desktop/uniscanTo3DTiles/development-mesh-data/testing/obj"
    glbRootDirPath = "C:/Users/harzival/Desktop/uniscanTo3DTiles/development-mesh-data/testing/gltf"
    b3dmRootDirPath = "C:/Users/harzival/Desktop/uniscanTo3DTiles/development-mesh-data/testing/b3dm"

    createDirIfDoesNotExist ( glbRootDirPath )
    createDirIfDoesNotExist ( b3dmRootDirPath )

    objList = Obj.getObjListFromRootPath ( objRootDirPath )
    boxList = []

    for obj in objList:
        obj.writeNewMtlData ()
        createDirIfDoesNotExist ( os.path.join ( glbRootDirPath, obj.lodDirName ) )
        obj.convertToGlb ( glbRootDirPath )
        createDirIfDoesNotExist ( os.path.join ( b3dmRootDirPath, obj.glb.lodDirName ) )
        obj.glb.convertToB3dm ( b3dmRootDirPath )
        obj.glb.b3dm.box = obj.calcMinMaxBoundingBox()
        boxList.append ( obj.glb.b3dm.box )
    
    worldBox = Box.createParentBoxFromBoxList ( boxList )

    plotter = BoxPlotter ()
    plotter.setGraphSizeLimitBox ( worldBox )

    plotter.drawEdges ( objList[0].glb.b3dm.box )
    plotter.start()


main()
