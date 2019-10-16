from vec3 import Vec3

class Box:

    def __init__ ( self, data = [ 0 ] * 12 ):
        self.data = data
        self.center = Vec3 ( data [ 0 ], data [ 1 ], data [ 2 ] )
        self.xBoundDist = Vec3 ( data [ 3 ], data [ 4 ], data [ 5 ] )
        self.yBoundDist = Vec3 ( data [ 6 ], data [ 7 ], data [ 8 ] )
        self.zBoundDist = Vec3 ( data [ 9 ], data [ 10], data [ 11] )
        self.min = self.center - self.xBoundDist - self.yBoundDist - self.zBoundDist
        self.max = self.center + self.xBoundDist + self.yBoundDist + self.zBoundDist
        self.width  = abs ( self.min.x - self.max.x )
        self.depth  = abs ( self.min.y - self.max.y )
        self.height = abs ( self.min.z - self.max.z )
        self.xBoundPoint = self.center  + self.xBoundDist
        self.yBoundPoint = self.xBoundPoint + self.yBoundDist
        self.zBoundPoint = self.yBoundPoint + self.zBoundDist
        self.sidePoints = self.calcSidePoints ( self.min, self.max, self.center )
        self.cornerPoints = self.calcCornerPoints ( self.min, self.max )

    def calcSidePoints ( self, min, max, mid ):
        return [
            Vec3 ( min.x, mid.y, mid.z ),   # Side 1
            Vec3 ( mid.x, min.y, mid.z ),   # Side 2
            Vec3 ( mid.x, mid.y, min.z ),   # Side 3
            Vec3 ( max.x, mid.y, mid.z ),   # Side 4
            Vec3 ( mid.x, max.y, mid.z ),   # Side 5
            Vec3 ( mid.x, mid.y, max.z ) ]  # Side 6
    def calcCornerPoints ( self, min, max ):
        return [
            Vec3 ( min.x, min.y, min.z ),   # Corner 1
            Vec3 ( min.x, max.y, min.z ),   # Corner 2
            Vec3 ( min.x, min.y, max.z ),   # Corner 3
            Vec3 ( min.x, max.y, max.z ),   # Corner 4
            Vec3 ( max.x, min.y, min.z ),   # Corner 5
            Vec3 ( max.x, max.y, min.z ),   # Corner 6
            Vec3 ( max.x, min.y, max.z ),   # Corner 7
            Vec3 ( max.x, max.y, max.z ) ]  # Corner 8
    
    @classmethod
    def createFromMinMax ( cls, min, max ):
        center = Vec3 ( 
            ( min.x + max.x ) / 2.0, 
            ( min.y + max.y ) / 2.0, 
            ( min.z + max.z ) / 2.0 )
        return cls ( [
            center.x, center.y, center.z, 
            abs ( min.x - max.x ) / 2, 0, 0,
            0, abs ( min.y - max.y ) / 2, 0,
            0, 0, abs ( min.z - max.z ) / 2 ] )
    
    @classmethod
    def createParentBoxFromBoxList ( cls, boxList ):
        min = Vec3(0,0,0)
        max = Vec3(0,0,0)
        for i, box in enumerate ( boxList ):
            if ( i == 0 ):
                min = box.min
                max = box.max
            else:
                if ( box.max.x > max.x ):
                        max.x = box.max.x
                if ( box.max.y > max.y ):
                        max.y = box.max.y
                if ( box.max.z > max.z ):
                        max.z = box.max.z
                if ( box.min.x < min.x ):
                        min.x = box.min.x
                if ( box.min.y < min.y ):
                        min.y = box.min.y
                if ( box.min.z < min.z ):
                        min.z = box.min.z
        return cls.createFromMinMax ( min, max )
    
    