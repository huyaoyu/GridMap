
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

def add_element_to_2D_list(ele, li):
    """
    This function tests the existance of ele in list li.
    If ele is not in li, then ele is appended to li.

    li is a 2D list. ele is supposed to have the same number of elements with 
    each element in list li.

    ele: A list.
    li: The targeting 2D list.
    """

    # Test if li is empty.
    nLi  = len( li )

    if ( 0 == nLi ):
        li.append( ele )
        return
    
    # Use nLi again.
    nLi = len( li[0] )

    nEle = len(ele)

    assert( nLi == nEle and nLi != 0 )

    # Try to find ele in li.
    for e in li:
        count = 0

        for i in range(nEle):
            if ( ele[i] == e[i] ):
                count += 1
            
        if ( nEle == count ):
            return
    
    li.append( ele )

class GridMap2D(object):
    I_R = 0
    I_C = 1
    I_X = 0
    I_Y = 1

    def __init__(self, rows, cols, origin = [0, 0], stepSize = [1, 1], name = "Default Name", outOfBoundValue = -100):
        assert( isinstance(rows, (int, long)) )
        assert( isinstance(cols, (int, long)) )
        assert( isinstance(origin[0], (int, long)) )
        assert( isinstance(origin[1], (int, long)) )
        assert( rows > 0 )
        assert( cols > 0 )

        self.isInitialized = False

        self.name      = name # Should be a string.

        self.rows      = rows
        self.cols      = cols
        self.origin    = copy.deepcopy(origin) # x and y coordinates of the starting coordinate.
        self.stepSize  = copy.deepcopy(stepSize) # Step sizes in x and y direction. Note the order of x and y.
        self.corners   = [] # A 4x2 2D list.
        self.blockRows = [] # A list contains rows of blocks.

        self.haveStaringPoint = False
        self.startingPointIdx = [0, 0]

        self.haveEndingPoint = False
        self.endingPointIdx  = [0, 0]

        self.obstacleIndices = []

        self.outOfBoundValue = outOfBoundValue

    def initialize(self, value = 1):
        if ( True == self.isInitialized ):
            raise Exception("Map already initialized.")

        # Drop current blockRows.
        self.blockRows = []

        # Generate indices for the blocks.
        rs = np.linspace(self.origin[GridMap2D.I_Y], self.origin[GridMap2D.I_Y] + self.rows - 1, self.rows, dtype = np.int)
        cs = np.linspace(self.origin[GridMap2D.I_X], self.origin[GridMap2D.I_X] + self.cols - 1, self.cols, dtype = np.int)
    
        h = self.stepSize[GridMap2D.I_Y]
        w = self.stepSize[GridMap2D.I_X]

        for r in rs:
            temp = []
            for c in cs:
                b = NormalBlock( c*w, r*h, h, w, value )
                temp.append(b)
            
            self.blockRows.append(temp)
        
        # Calcluate the corners.
        self.corners.append( [        cs[0]*w,      rs[0]*h ] )
        self.corners.append( [ (cs[-1] + 1)*w,      rs[0]*h ] )
        self.corners.append( [ (cs[-1] + 1)*w, (rs[-1]+1)*h ] )
        self.corners.append( [        cs[0]*w, (rs[-1]+1)*h ] )
    
    def get_step_size(self):
        """[x, y]"""
        return self.stepSize

    def get_index_starting_point(self):
        if ( False == self.haveStaringPoint ):
            raise Exception("No staring point set yet.")
        
        return self.startingPointIdx
    
    def get_index_ending_point(self):
        if ( False == self.haveEndingPoint ):
            raise Exception("No ending point set yet.")
        
        return self.endingPointIdx

    def set_starting_point(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        if ( True == self.haveStaringPoint ):
            # Overwrite the old staring point with a NormalBlock.
            self.overwrite_block( self.startingPointIdx[GridMap2D.I_R], self.startingPointIdx[GridMap2D.I_C], NormalBlock() )
        
        # Overwrite a block. Make it to be a starting point.
        self.overwrite_block( r, c, StartingPoint() )
        self.startingPointIdx = [ r, c ]

        self.haveStaringPoint = True

    def set_ending_point(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        if ( True == self.haveEndingPoint ):
            # Overwrite the old staring point with a NormalBlock.
            self.overwrite_block( self.endingPointIdx[GridMap2D.I_R], self.endingPointIdx[GridMap2D.I_C], NormalBlock() )
        
        # Overwrite a block. Make it to be a starting point.
        self.overwrite_block( r, c, EndingPoint() )
        self.endingPointIdx = [ r, c ]

        self.haveEndingPoint = True

    def add_obstacle(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )

        # Check if the location is a starting point.
        if ( r == self.startingPointIdx[GridMap2D.I_R] and c == self.startingPointIdx[GridMap2D.I_C] ):
            raise IndexError( "Cannot turn a starting point (%d, %d) into obstacle." % (r, c) )
        
        # Check if the location is a ending point.
        if ( r == self.endingPointIdx[GridMap2D.I_R] and c == self.endingPointIdx[GridMap2D.I_C] ):
            raise IndexError( "Cannot turn a ending point (%d, %d) into obstacle." % (r, c) )

        self.overwrite_block( r, c, ObstacleBlock() )

        # Add the indices into self.obstacleIndices 2D list.
        add_element_to_2D_list( [r, c], self.obstacleIndices )

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
        b.set_coor_size( c, r, self.stepSize[GridMap2D.I_Y], self.stepSize[GridMap2D.I_X] )

        self.blockRows[r][c] = copy.deepcopy(b)

    def get_string_starting_point(self):
        if ( True == self.haveStaringPoint ):
            s = "Starting point at [%d, %d]." % ( self.startingPointIdx[GridMap2D.I_R], self.startingPointIdx[GridMap2D.I_C] )
        else:
            s = "No starting point."

        return s

    def get_string_ending_point(self):
        if ( True == self.haveEndingPoint ):
            s = "Ending point at [%d, %d]." % ( self.endingPointIdx[GridMap2D.I_R], self.endingPointIdx[GridMap2D.I_C] )
        else:
            s = "No ending point."

        return s

    def get_string_obstacles(self):
        n = len( self.obstacleIndices )

        if ( 0 == n ):
            s = "No obstacles."
            return s
        
        s = "%d obstacles:\n" % (n)

        for obs in self.obstacleIndices:
            s += "[%d, %d]\n" % (obs[GridMap2D.I_R], obs[GridMap2D.I_C])
        
        return s

    def get_string_corners(self):
        s = "Corners:\n"
        
        for c in self.corners:
            s += "[%f, %f]\n" % ( c[GridMap2D.I_X], c[GridMap2D.I_Y] )

        return s

    def __str__(self):
        title = "GridMap2D \"%s\"." % (self.name)

        strDimensions = \
"""r = %d, c = %d.
origin = [%d, %d], size = [%d, %d].""" \
% (self.rows, self.cols, self.origin[GridMap2D.I_X], self.origin[GridMap2D.I_Y], self.stepSize[GridMap2D.I_X], self.stepSize[GridMap2D.I_Y])

        # Get the string for staring point.
        strStartingPoint = self.get_string_starting_point()

        # Get the string for ending point.
        strEndingPoint = self.get_string_ending_point()

        # Get the string for obstacles.
        strObstacles = self.get_string_obstacles()

        # Get the string for the corners.
        strCorners = self.get_string_corners()

        s = "%s\n%s\n%s\n%s\n%s\n%s\n" \
            % ( title, strDimensions, strStartingPoint, strEndingPoint, strObstacles, strCorners )

        return s

    def is_out_of_boundary(self, x, y):
        if ( x <  self.corners[0][GridMap2D.I_X] or \
             x >= self.corners[1][GridMap2D.I_X] or \
             y <  self.corners[0][GridMap2D.I_Y] or \
             y >= self.corners[3][GridMap2D.I_Y] ):
            return True
        
        return False

    def get_index_by_coordinates(self, x, y):
        """
        It is assumed that (x, y) is inside the map boundaries.
        x and y are real values.
        A list of two elements is returned. The values inside the returned
        list is the row and column indices of the block.
        """

        c = int( ( 1.0*x - self.origin[GridMap2D.I_X] ) / self.stepSize[GridMap2D.I_X] )
        r = int( ( 1.0*y - self.origin[GridMap2D.I_Y] ) / self.stepSize[GridMap2D.I_Y] )

        return [r, c]

    def evaluate_coordinate(self, x, y):
        """
        This function evaluate coordinate (x, y) according to the under lying map.
        A value will be returned as the result of evaluation.
        x and y are real numbers rather than integers.
        If (x, y) is out of the boundary of the map, the outOfBoundValue will be returned.
        """

        # Check if (x, y) is out of boundary.
        if ( True == self.is_out_of_boundary( x, y ) ):
            return self.outOfBoundValue
        
        # In the boundary.
        # Calculate the integer index of block where (x, y) stays in.
        [r, c] = self.get_index_by_coordinates(x, y)

        # Get the value of the [r, c]] block.
        return self.blockRows[r][c].value
    
    def convert_to_coordinates(self, r, c):
        """Convert the index into the real valued coordinates."""

        # Check if [r, c] is valid.
        assert( isinstance( r, (int, long) ) )
        assert( isinstance( c, (int, long) ) )
        assert( r >= 0 and r < self.rows )
        assert( c >= 0 and c < self.cols )

        return [ c*self.stepSize[GridMap2D.I_X], r*self.stepSize[GridMap2D.I_Y] ]

class GridMapEnv(object):
    def __init__(self, name = "DefaultGridMapEnv", gridMap = None):
        self.name = name
        self.map  = gridMap
        self.agentStartingLoc = [0, 0]

        self.isTerminated = False
        self.nSteps = 0

        self.agentCurrentLoc = copy.deepcopy( self.agentStartingLoc )
        self.agentCurrentAct = [0, 0]

    def get_state_size(self):
        return len( self.agentCurrentLoc )
    
    def get_action_size(self):
        return len( self.agentCurrentAct )
    
    def reset(self):
        """Reset the evironment."""

        # Get the index of the starting point.
        [rs, cs] = self.map.get_index_starting_point()
        # Get the coordinates of [rs, cs].
        [cx, cy] = self.map.convert_to_coordinates(rs, cs)

        self.agentStartingLoc = [\
            cx + self.map.get_step_size[0] / 2.0, \
            cy + self.map.get_step_size[1] / 2.0 \
            ]
        
        # Reset the location of the agent.
        self.agentCurrentLoc = copy.deepcopy( self.agentStartingLoc )

        # Clear the cuurent action of the agent.
        self.agentCurrentAct = [0, 0]

        # Clear step counter.
        self.nSteps = 0

        # Clear termination flag.
        self.isTerminated = False

    def step(self, action):
        """Return values are next state, reward value, termination flag, and None."""

        

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

    # Create a GridMap2D object.
    gm2d = GridMap2D(10, 20, outOfBoundValue=-200)
    gm2d.initialize()

    # Create a starting point and an ending point.
    startingPoint = StartingPoint()
    endingPoint   = EndingPoint()

    # Create an obstacle block.
    obstacle = ObstacleBlock()

    # Overwrite blocks.
    gm2d.set_starting_point(0, 0)
    gm2d.set_ending_point(9, 19)
    gm2d.add_obstacle(4, 10)
    gm2d.add_obstacle(5, 10)
    gm2d.add_obstacle(6, 10)

    # Describe the map.
    print(gm2d)

    # import ipdb; ipdb.set_trace()

    # Test GridMap2D.evaluate_coordinate
    print("Value of (   0,      0) is %f" % ( gm2d.evaluate_coordinate(0, 0) ) )
    print("Value of (19.99,  9.99) is %f" % ( gm2d.evaluate_coordinate(19.99, 9.99) ) )
    print("Value of (19.99,     0) is %f" % ( gm2d.evaluate_coordinate(19.99, 0) ) )
    print("Value of (    0,  9.99) is %f" % ( gm2d.evaluate_coordinate(0, 9.99) ) )
    print("Value of (   10,     4) is %f" % ( gm2d.evaluate_coordinate(10, 4) ) )
    print("Value of (   10,     5) is %f" % ( gm2d.evaluate_coordinate(10, 5) ) )
    print("Value of (   10,     6) is %f" % ( gm2d.evaluate_coordinate(10, 6) ) )
    print("Value of (   10,   5.5) is %f" % ( gm2d.evaluate_coordinate(10, 5.5) ) )
    print("Value of ( 10.5,     5) is %f" % ( gm2d.evaluate_coordinate(10.5, 5) ) )
    print("Value of (10.99,  5.99) is %f" % ( gm2d.evaluate_coordinate(10.99, 5.99) ) )
    print("Value of (   -1,    -1) is %f" % ( gm2d.evaluate_coordinate(-1, -1) ) )
    print("Value of (    9, -0.01) is %f" % ( gm2d.evaluate_coordinate(9, -0.01) ) )
    print("Value of (    9, 10.01) is %f" % ( gm2d.evaluate_coordinate(9, 10.01) ) )
    print("Value of (-0.01,     5) is %f" % ( gm2d.evaluate_coordinate(-0.01, 5) ) )
    print("Value of (20.01,     5) is %f" % ( gm2d.evaluate_coordinate(20.01, 5) ) )

    # Create a GridMapEnv object.
    gme = GridMapEnv(gridMap = gm2d)

    # Render.
    gme.render()
