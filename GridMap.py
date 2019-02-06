
from __future__ import print_function

import copy
import matplotlib.pyplot as plt
import numpy as np

class Block(object):
    def __init__(self, x = 0, y = 0, h = 1, w = 1):
        if ( ( not isinstance(x, (int, long)) ) or \
             ( not isinstance(y, (int, long)) ) or \
             ( not isinstance(h, (int, long)) ) or \
             ( not isinstance(w, (int, long)) ) ):
            raise TypeError("x, y, h, and w must be integers.")
        
        self.coor = [x, y]
        self.size = [h, w]
        self.corners = [ \
            [0, 0],\
            [0, 0],\
            [0, 0],\
            [0, 0]\
        ]

        self.update_corners()

        self.name  = "Default name"
        self.id    = 0
        self.color = "#FFFFFFFF" # RGBA order.
        self.value = 0

    def update_corners(self):
        x = self.coor[0]
        y = self.coor[1]
        h = self.size[0]
        w = self.size[1]
        
        self.corners = [ \
            [x,   y],\
            [x+w, y],\
            [x+w, y+h],\
            [x,   y+h]\
        ]

    def set_coor(self, x, y, flagUpdate = True):
        # Check the arguments.
        if ( (not isinstance(x, (int, long))) or (not isinstance(y, (int, long))) ):
            raise TypeError("x and y must be integers.")
        
        self.coor = [x, y]

        if ( True == flagUpdate ):
            self.update_corners()
    
    def set_size(self, h, w, flagUpdate = True):
        # Check the arguments.
        if ( ( not isinstance(h, (int, long)) ) or ( not isinstance(w, (int, long)) ) ):
            raise TypeError("h and w must be integers.")

        if ( h <= 0 or w <= 0 ):
            raise ValueError("h and w must be positive values, h = %d, w = %d" % (h, w))
        
        self.size = [h, w]
        if ( True == flagUpdate ):
            self.update_corners()

    def set_coor_size(self, x, y, h, w):
        self.set_coor( x, y, False )
        self.set_size( h, w )
    
    def get_coor(self, idx = 0):
        # Argument check.
        if ( not isinstance(idx, (int, long)) ):
            raise TypeError("idx must be an integer")
        
        if ( idx < 0 or idx > 3 ):
            raise IndexError("idx out of range, idx = %d" % (idx))
        
        return self.corners[idx]

class NormalBlock(Block):
    def __init__(self, x = 0, y = 0, h = 1, w = 1, value = 1):
        super(NormalBlock, self).__init__(x, y, h, w)

        # Member variables defined in the super classes.
        self.color = "#FFFFFFFF"
        self.name  = "NormalBlock"
        self.value = value
    
class ObstacleBlock(Block):
    def __init__(self, x = 0, y = 0, h = 1, w = 1, value = -100):
        super(ObstacleBlock, self).__init__(x, y, h, w)

        # Member variables defined in the super classes.
        self.color = "#FF0000FF"
        self.name  = "ObstacleBlock"
        self.value = value

class StartingPoint(Block):
    def __init__(self, x = 0, y = 0, h = 1, w = 1, value = 0):
        super(StartingPoint, self).__init__(x, y, h, w)

        # Member variables defined in the super classes.
        self.color = "#00FF00FF"
        self.name  = "StartingPoint"
        self.value = value

class EndingPoint(Block):
    def __init__(self, x = 0, y = 0, h = 1, w = 1, value = 100):
        super(EndingPoint, self).__init__(x, y, h, w)
    
        # Member variables defined in the super classes.
        self.color = "#0000FFFF"
        self.name  = "EndingPoint"
        self.value = value

class GridMap2D(object):
    def __init__(self, rows, cols, start = [0, 0], size = [1, 1]):
        assert( isinstance(rows, (int, long)) )
        assert( isinstance(cols, (int, long)) )
        assert( isinstance(start[0], (int, long)) )
        assert( isinstance(start[1], (int, long)) )
        assert( rows > 0 )
        assert( cols > 0 )

        self.rows      = rows
        self.cols      = cols
        self.start     = copy.deepcopy(start) # x and y coordinates of the starting coordinate.
        self.size      = copy.deepcopy(size)
        self.blockRows = [] # A list contains rows of blocks.

        self.haveStaringPoint = False
        self.startingPointIdx = [0, 0]

    def initialize(self, value = 1):
        # Drop current blockRows.
        self.blockRows = []

        # Generate indices for the blocks.
        rs = np.linspace(self.start[1], self.start[1] + self.rows - 1, self.rows, dtype = np.int)
        cs = np.linspace(self.start[0], self.start[0] + self.cols - 1, self.cols, dtype = np.int)
    
        h = self.size[0]
        w = self.size[1]

        for r in rs:
            temp = []
            for c in cs:
                b = NormalBlock( c*w, r*h, h, w, value )
                temp.append(b)
            
            self.blockRows.append(temp)
    
    def set_starting_point(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        if ( True == self.haveStaringPoint ):
            # Overwrite the old staring point with a NormalBlock.
            pass
        
        # Overwrite a block. Make it to be a starting point.
        self.overwrite_block( r, c, StartingPoint() )
        self.startingPointIdx = [ r, c ]

        self.haveStaringPoint = True

    def overwrite_block(self, r, c, b):
        """
        r: Row index.
        c: Col index.
        b: The new block.

        b will be assigned to the specified location by a deepcopy.
        The overwritten block does not share the same coordinates with b.
        The coordinates are assigned by the values of r and c.
        """

        assert( r < self.rows )
        assert( c < self.cols )

        temp = copy.deepcopy(b)
        b.set_coor_size( c, r, self.size[0], self.size[1] )

        self.blockRows[r][c] = copy.deepcopy(b)

class GridMapEnv(object):
    def __init__(self, name = "DefaultGridMapEnv", gridMap = None):
        self.name = name
        self.map  = gridMap
        self.agentStartingLoc = [0, 0]
    
    def render(self):
        """Render with matplotlib."""

        if ( self.map is None ):
            raise ValueError("self.map is None")

        from matplotlib.collections import PatchCollection
        from matplotlib.patches import Rectangle

        fig, ax = plt.subplots(1)

        for br in self.map.blockRows:
            for b in br:
                rect = Rectangle( (b.coor[0], b.coor[1]), b.size[1], b.size[0], fill = True)
                rect.set_facecolor(b.color)
                rect.set_edgecolor("k")
                ax.add_patch(rect)
        
        ax.autoscale()

        plt.show()

if __name__ == "__main__":
    print("Hello GridMap.")

    # import ipdb; ipdb.set_trace()

    # Create a GridMap2D object.
    gm2d = GridMap2D(10, 10)
    gm2d.initialize()

    # Create a starting point and an ending point.
    startingPoint = StartingPoint()
    endingPoint   = EndingPoint()

    # Create an obstacle block.
    obstacle = ObstacleBlock()

    # Overwrite blocks.
    gm2d.overwrite_block( 0,  0, startingPoint)
    gm2d.overwrite_block( 9,  9, endingPoint)
    gm2d.overwrite_block( 5,  5, obstacle)

    # Create a GridMapEnv object.
    gme = GridMapEnv(gridMap = gm2d)

    # Render.
    gme.render()
