class Vec3 ( object ):

    def __init__ ( self, x = 0, y = 0, z = 0 ):
        self.x = x
        self.y = y
        self.z = z
        self.list = [ x, y, z ]

    def __add__ ( self, other ):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3 ( x, y, z )

    def __sub__ ( self, other ):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3 ( x, y, z )

    def zero ( self ):
        return self.__init__ ( 0, 0, 0 )

    def one ( self ):
        return self.__init__ ( 1, 1, 1 )
    
    def transformAxisZUp ( self ):
        return self.__init__ ( x =  self.x, y = -self.z, z = self.y )
    