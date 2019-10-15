from subprocess import call
from os import path, listdir, scandir, remove
from collections import namedtuple
from glb import Glb
from vec3 import Vec3

class Obj ( object ):
    def __init__ (self, rootDirPath = None, lodDirName = None, fileName = None ):
        self.rootDirPath = rootDirPath
        self.lodDirName = lodDirName
        self.fileName = fileName
        self.tileName = fileName.split ( '.' ) [ 0 ]
        self.path = path.join ( rootDirPath, lodDirName, fileName )
        self.glbFileName = self.tileName + ".glb"
        self.gltfFileName = self.tileName + ".gltf"
        self.albedoMapPath = path.join ( rootDirPath, lodDirName, ( self.tileName + "_albedo.jpg" ) )
        self.normalMapPath = path.join ( rootDirPath, lodDirName, ( self.tileName + "_normal.jpg" ) )
        self.glb = None

    def convertToGlb ( self, glbRootDirPath):
        call ( [
            "node", "C:/Users/harzival/Desktop/uniscanTo3DTiles/dependencies/obj2gltf/bin/obj2gltf.js", 
            "--binary",
            "--unlit",
            "-i", self.path,
            "--baseColorTexture", self.albedoMapPath,
            "--normalTexture", self.normalMapPath,
            "-o", path.join ( glbRootDirPath, self.lodDirName, self.glbFileName ) ] )
        self.glb = Glb ( glbRootDirPath, self.lodDirName, self.glbFileName )
        return self.glb


    def convertToGltf ( self, obj, glbRootDirPath):
        call ( [
            "node", "C:/Users/harzival/Desktop/uniscanTo3DTiles/dependencies/obj2gltf/bin/obj2gltf.js", 
            "--unlit",
            "-i", self.path,
            "--baseColorTexture", self.albedoMapPath,
            "--normalTexture", self.normalMapPath,
            "-o", path.join ( glbRootDirPath, self.lodDirName, self.gltfFileName ) ] )
        self.glb = Glb ( glbRootDirPath, self.lodDirName, self.glbFileName )
        return self.glb

    @staticmethod
    def getObjListFromRootPath ( rootDirPath ):
        objArray = []
        for lodDir in scandir ( rootDirPath ):
            for fileName in listdir ( lodDir ):
                if fileName.endswith ( ".obj" ):
                    obj = Obj ( rootDirPath, lodDir.name, fileName )
                    print ( "UNISCAN: Adding tile {0} from {1} to the serialiser queue.".format ( obj.tileName, obj.lodDirName ) )
                    objArray.append ( obj )
        return objArray
    
    def getMtlData ( self ):
        openedObjFile = open ( self.path )
        # Get the line in the mesh's file which starts with "usemtl ".
        # Return a string containing the line without the "usemtl " prefix.
        for i, line in enumerate ( openedObjFile ):
            if line.startswith("usemtl"):
                mtlData = "newmtl {0}\n{1}\n{2}\n{3}\n{4}\n{5}".format (
                    line.replace ( "usemtl ", "" ).rstrip( '\n' ),
                    "Ka 1 1 1",
                    "Kd 1 1 1",
                    "d 1", 
                    "Ns 0",
                    "illum 1" )
                openedObjFile.close()
                return mtlData

    def writeNewMtlData ( self ):
        mtlPath = self.path.replace ( ".obj", ".mtl" )
        if path.exists ( mtlPath ):
            print ( "UNISCAN: MTL file for OBJ already exists, will now delete and recreate it." )
            remove ( mtlPath )
        else:
            print ( "UNISCAN: MTL file for OBJ does not exist, will now create it." )
        try:
            mtlFile = open ( mtlPath, "x")
            mtlFile.write ( getMtlData ( self.path ) )
            mtlFile.close ()
        except IOError as error:
            print ( error )
        except:
            print ( "UNISCAN: Unknown error creating MTL")

    def calcMinMax ( self ):
        Point = namedtuple('Point', ['x', 'y', 'z'])
        min = Vec3 (0,0,0)
        max = Vec3 (0,0,0)
        for i, line in enumerate ( open ( self.path, 'r' ) ):
            if ( line [:2] == "v " ):
                vertexValues = line [ 2: ].rstrip ( "\n" ).split ( " " )
                vertex = Point ( float ( vertexValues [0] ), float( vertexValues [1] ), float ( vertexValues [ 2 ] ) )
                if ( i == 0 ):
                    min = Vec3 ( vertex.x, vertex.y, vertex.z )
                    max = Vec3 ( vertex.x, vertex.y, vertex.z )
                else:
                    if ( vertex.x > max.x ):
                        max.x = vertex.x
                    if ( vertex.y > max.y ):
                        max.y = vertex.y
                    if ( vertex.z > max.z ):
                        max.z = vertex.z 
                    if ( vertex.x < min.x ):
                        min.x = vertex.x
                    if ( vertex.y < min.y ):
                        min.y = vertex.y
                    if ( vertex.z < min.z ):
                        min.z = vertex.z 
        return min.transformAxisZUp(), max.transformAxisZUp()