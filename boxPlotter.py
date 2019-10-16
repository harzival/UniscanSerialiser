import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from vec3 import Vec3

class BoxPlotter:
    def __init__ ( self ):
        self.fig = plt.figure ()
        self.ax = plt.axes ( projection="3d" )
    
    def start ( self ):
        plt.show()
    
    def setGraphSizeLimitBox ( self, box ):
        def largestBetween ( a, b, c ):
            if   ( a >= b ) and ( a >= c ): return a
            elif ( b >= a ) and ( b >= c ): return b
            else                          : return c
        center = box.center
        size = largestBetween ( box.width, box.depth, box.height )
        radius = round ( size * ( 1.5 / 2 ), 5 )
        self.ax.set_xlim ( center.x - radius, center.x + radius )
        self.ax.set_ylim ( center.y - radius, center.y + radius )
        self.ax.set_zlim ( center.z - radius, center.z + radius )
    
    def drawLine ( self, start = Vec3.zero, end = Vec3.zero, color = "black"):
        self.ax.plot ( [ start.x, end.x ], [ start.y, end.y ], [ start.z, end.z ], color=color )
    
    def drawDistLines ( self, box ):
        self.drawLine ( box.center, box.xBoundPoint, "red" )
        self.drawLine ( box.xBoundPoint, box.yBoundPoint, "green" )
        self.drawLine ( box.yBoundPoint, box.zBoundPoint, "blue" )

    def drawEdgesFromCornerPoints ( self, cornerPoints ):
        pnts = cornerPoints
        self.drawLine ( pnts[0], pnts[1], color = "grey" )
        self.drawLine ( pnts[1], pnts[3], color = "grey" )
        self.drawLine ( pnts[2], pnts[0], color = "grey" )
        self.drawLine ( pnts[3], pnts[2], color = "grey" )
        self.drawLine ( pnts[4], pnts[5], color = "grey" )
        self.drawLine ( pnts[5], pnts[7], color = "grey" )
        self.drawLine ( pnts[6], pnts[4], color = "grey" )
        self.drawLine ( pnts[7], pnts[6], color = "grey" )
        self.drawLine ( pnts[0], pnts[4], color = "grey" )
        self.drawLine ( pnts[1], pnts[5], color = "grey" )
        self.drawLine ( pnts[2], pnts[6], color = "grey" )
        self.drawLine ( pnts[3], pnts[7], color = "grey" )    

    def drawEdges ( self, box ):
        self.drawEdgesFromCornerPoints ( box.cornerPoints )