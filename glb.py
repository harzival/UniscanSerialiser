from subprocess import call
from os import path
from b3dm import B3dm

class Glb ( object ):
    def __init__ (self, rootDirPath = None, lodDirName = None, fileName = None ):
        self.rootDirPath = rootDirPath
        self.lodDirName = lodDirName
        self.fileName = fileName
        self.tileName = fileName.split ( '.' ) [ 0 ]
        self.b3dmFileName = self.tileName + ".b3dm"
        self.path = path.join ( rootDirPath, lodDirName, fileName )
        self.b3dm = None


    def convertToB3dm ( self, b3dmRootDirPath):
        call ( [
            "node", "C:/Users/harzival/Desktop/uniscanTo3DTiles/dependencies/3d-tiles-tools/tools/bin/3d-tiles-tools.js", 
            "glbToB3dm", "--force",
            "-i", self.path,
            "-o", path.join ( b3dmRootDirPath, self.lodDirName, self.b3dmFileName ) ] ) 
        self.b3dm = B3dm ( b3dmRootDirPath, self.lodDirName, self.b3dmFileName )  
        return self.b3dm