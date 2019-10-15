from os import path

class B3dm:
    def __init__ (self, rootDirPath = None, lodDirName = None, fileName = None ):
        self.rootDirPath = rootDirPath
        self.lodDirName = lodDirName
        self.fileName = fileName
        self.tileName = fileName.split ( '.' ) [ 0 ]
        self.path = path.join ( rootDirPath, lodDirName, fileName )
        self.box = None
