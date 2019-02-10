
from __future__ import print_function

import copy
import math
import matplotlib.pyplot as plt
import numpy as np

import LineIntersection2D

def two_point_distance(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    return math.sqrt( dx**2 + dy**2 )

class GridMapException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr( self.msg )

class BlockIndex(object):
    def __init__(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        self.r = r
        self.c = c

        self.size = 2
    
    def __str__(self):
        return "index({}, {})".format( self.r, self.c )

class BlockCoor(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.size = 2

    def __str__(self):
        return "coor({}, {})".format( self.x, self.y )

class BlockCoorDelta(object):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

        self.size = 2

    def __str__(self):
        return "CoorDelta({}, {})".format( self.dx, self.dy )

    def convert_to_direction_delta(self):
        dx = 0
        dy = 0

        if ( self.dx > 0 ):
            dx = 1.0
        elif ( dx < 0 ):
            dx = -1.0
        
        if ( self.dy > 0 ):
            dy = 1.0
        elif ( self.dy < 0 ):
            dy = -1.0
        
        return BlockCoorDelta( dx, dy )

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
        self.corners   = [] # A 4x2 2D list. Coordinates.
        self.blockRows = [] # A list contains rows of blocks.

        self.haveStaringPoint = False
        self.startingPointIdx = BlockIndex(0, 0)

        self.haveEndingPoint = False
        self.endingPointIdx  = BlockIndex(0, 0)

        self.obstacleIndices = []

        self.outOfBoundValue = outOfBoundValue

    def initialize(self, value = 1):
        if ( True == self.isInitialized ):
            raise GridMapException("Map already initialized.")

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
    
    def get_block(self, index):
        if ( isinstance( index, BlockIndex ) ):
            if ( index.r >= self.rows or index.c >= self.cols ):
                raise IndexError( "Index out of range. indx = [%d, %d]" % (index.r, index.c) )
            
            return self.blockRows[index.r][index.c]
        elif ( isinstance( index, (list, tuple) ) ):
            if ( index[GridMap2D.I_R] >= self.rows or \
                 index[GridMap2D.I_C] >= self.cols ):
                raise IndexError( "Index out of range. indx = [%d, %d]" % (index.r, index.c) )
            
            return self.blockRows[ index[GridMap2D.I_R] ][ index[GridMap2D.I_C] ]

    def is_normal_block(self, index):
        b = self.get_block(index)

        return isinstance( b, NormalBlock )

    def is_obstacle_block(self, index):
        b = self.get_block(index)

        return isinstance( b, ObstacleBlock )

    def is_starting_point(self, index):
        b = self.get_block(index)

        return isinstance( b, StartingPoint )

    def is_ending_point(self, index):
        b = self.get_block(index)

        return isinstance( b, EndingPoint )

    def get_step_size(self):
        """[x, y]"""
        return self.stepSize

    def get_index_starting_point(self):
        """Return a copy of the index of the starting point."""
        if ( False == self.haveStaringPoint ):
            raise GridMapException("No staring point set yet.")
        
        return copy.deepcopy( self.startingPointIdx )
    
    def get_index_ending_point(self):
        """Return a copy of the index of the ending point."""
        if ( False == self.haveEndingPoint ):
            raise GridMapException("No ending point set yet.")
        
        return copy.deepcopy( self.endingPointIdx )

    def is_in_ending_point(self, coor):
        """Return ture if coor is in the ending point."""

        if ( True == self.is_out_of_or_on_boundary(coor) ):
            return False
        
        loc = self.is_corner_or_principle_line(coor)
        if ( True == loc[0] or True == loc[1] or True == loc[2] ):
            return False

        idx = loc[3]
        if ( True == isinstance( self.blockRows[ idx.r ][ idx.c ], EndingPoint ) ):
            return True
        
        return False

    def set_starting_point_s(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        if ( True == self.haveStaringPoint ):
            # Overwrite the old staring point with a NormalBlock.
            self.overwrite_block( self.startingPointIdx.r, self.startingPointIdx.c, NormalBlock() )
        
        # Overwrite a block. Make it to be a starting point.
        self.overwrite_block( r, c, StartingPoint() )
        self.startingPointIdx.r = r
        self.startingPointIdx.c = c

        self.haveStaringPoint = True

    def set_starting_point(self, index):
        if ( isinstance( index, BlockIndex ) ):
            self.set_starting_point_s( index.r, index.c )
        elif ( isinstance( index, (list, tuple) ) ):
            self.set_starting_point_s( index[GridMap2D.I_R], index[GridMap2D.I_C] )
        else:
            raise TypeError("index should be an object of BlockIndex or a list or a tuple.")

    def set_ending_point_s(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )
        
        if ( True == self.haveEndingPoint ):
            # Overwrite the old staring point with a NormalBlock.
            self.overwrite_block( self.endingPointIdx.r, self.endingPointIdx.c, NormalBlock() )
        
        # Overwrite a block. Make it to be a starting point.
        self.overwrite_block( r, c, EndingPoint() )
        self.endingPointIdx.r = r
        self.endingPointIdx.c = c

        self.haveEndingPoint = True
    
    def set_ending_point(self, index):
        if ( isinstance( index, BlockIndex ) ):
            self.set_ending_point_s( index.r, index.c )
        elif ( isinstance( index, (list, tuple) ) ):
            self.set_ending_point_s( index[GridMap2D.I_R], index[GridMap2D.I_C] )
        else:
            raise TypeError("index should be an object of BlockIndex or a list or a tuple.")

    def add_obstacle_s(self, r, c):
        assert( isinstance(r, (int, long)) )
        assert( isinstance(c, (int, long)) )

        # Check if the location is a starting point.
        if ( r == self.startingPointIdx.r and c == self.startingPointIdx.c ):
            raise IndexError( "Cannot turn a starting point (%d, %d) into obstacle." % (r, c) )
        
        # Check if the location is a ending point.
        if ( r == self.endingPointIdx.r and c == self.endingPointIdx.c ):
            raise IndexError( "Cannot turn a ending point (%d, %d) into obstacle." % (r, c) )

        # Check if the destination is already an obstacle.
        if ( isinstance( self.get_block((r, c)), ObstacleBlock ) ):
            return

        self.overwrite_block( r, c, ObstacleBlock() )

        # Add the indices into self.obstacleIndices 2D list.
        add_element_to_2D_list( [r, c], self.obstacleIndices )

    def add_obstacle(self, index):
        if ( isinstance( index, BlockIndex ) ):
            self.add_obstacle_s( index.r, index.c )
        elif ( isinstance( index, (list, tuple) ) ):
            self.add_obstacle_s( index[GridMap2D.I_R], index[GridMap2D.I_C] )
        else:
            raise TypeError("index should be an object of BlockIndex or a list or a tuple.")

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
        temp.set_coor_size( c, r, self.stepSize[GridMap2D.I_Y], self.stepSize[GridMap2D.I_X] )

        self.blockRows[r][c] = temp

    def get_string_starting_point(self):
        if ( True == self.haveStaringPoint ):
            s = "Starting point at [%d, %d]." % ( self.startingPointIdx.r, self.startingPointIdx.c )
        else:
            s = "No starting point."

        return s

    def get_string_ending_point(self):
        if ( True == self.haveEndingPoint ):
            s = "Ending point at [%d, %d]." % ( self.endingPointIdx.r, self.endingPointIdx.c )
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

    def is_out_of_or_on_boundary_s(self, x, y):
        if ( x <= self.corners[0][GridMap2D.I_X] or \
             x >= self.corners[1][GridMap2D.I_X] or \
             y <= self.corners[0][GridMap2D.I_Y] or \
             y >= self.corners[3][GridMap2D.I_Y] ):
            return True
        
        return False

    def is_out_of_or_on_boundary(self, coor):
        """Overloaded function. Vary only in the argument list."""

        if ( isinstance(coor, BlockCoor) ):
            return self.is_out_of_or_on_boundary_s( coor.x, coor.y )
        elif ( isinstance(coor, (list, tuple)) ):
            return self.is_out_of_or_on_boundary_s( coor[GridMap2D.I_X], coor[GridMap2D.I_Y] )
        else:
            raise GridMapException("coor should be either an object of BlockCoor or a list")

    def is_out_of_boundary_s(self, x, y):
        if ( x < self.corners[0][GridMap2D.I_X] or \
             x > self.corners[1][GridMap2D.I_X] or \
             y < self.corners[0][GridMap2D.I_Y] or \
             y > self.corners[3][GridMap2D.I_Y] ):
            return True
        
        return False

    def is_out_of_boundary(self, coor):
        """Overloaded function. Vary only in the argument list."""

        if ( isinstance(coor, BlockCoor) ):
            return self.is_out_of_boundary_s( coor.x, coor.y )
        elif ( isinstance(coor, (list, tuple)) ):
            return self.is_out_of_boundary_s( coor[GridMap2D.I_X], coor[GridMap2D.I_Y] )
        else:
            raise GridMapException("coor should be either an object of BlockCoor or a list")

    def get_index_by_coordinates_s(self, x, y):
        """
        It is assumed that (x, y) is inside the map boundaries.
        x and y are real values.
        A list of two elements is returned. The values inside the returned
        list is the row and column indices of the block.
        """

        c = int( ( 1.0*x - self.origin[GridMap2D.I_X] ) / self.stepSize[GridMap2D.I_X] )
        r = int( ( 1.0*y - self.origin[GridMap2D.I_Y] ) / self.stepSize[GridMap2D.I_Y] )

        return BlockIndex(r, c)

    def get_index_by_coordinates(self, coor):
        """Overloaded funcion. Only varys in the argument list."""

        if ( isinstance(coor, BlockCoor) ):
            return self.get_index_by_coordinates_s( coor.x, coor.y )
        elif ( isinstance(coor, (list, tuple)) ):
            return self.get_index_by_coordinates_s( coor[GridMap2D.I_X], coor[GridMap2D.I_Y])
        else:
            raise TypeError("coor should be either an object of BlcokCoor or a list")

    def sum_block_values(self, idxList):
        """
        Sum the values according to the index list in idxList.

        It is processed as follows:
        * If neighboring block is out of boundary, an outOfBoundaryValue will be added.
        * If neighboring block is an obstacle, the value of an obstacle well be added.
        * If no neighboring block is either out of boundary or an obstacle, only one normal block will be counted.
        """

        # Number of indices.
        n = len( idxList )

        if ( 0 == n ):
            raise GridMapException("The length of idxList must not be zero.")

        if ( 1 == n ):
            idx = idxList[0]
            return self.blockRows[ idx.r ][ idx.c ].value

        flagHaveNormalBlock    = False
        flagHaveNonNormalBlock = False

        val   = 0 # The final value.
        valNB = 0 # The value of the normal block.

        for idx in idxList:
            # Check if idx is out of boundary.
            if ( idx.r >= self.rows or \
                 idx.c >= self.cols or \
                 idx.r < 0 or \
                 idx.c < 0 ):
                val += self.outOfBoundValue
                flagHaveNonNormalBlock = True
                continue

            # Get the actual block.
            b = self.blockRows[ idx.r ][ idx.c ]

            # Check if idx is a normal block.
            if ( isinstance( b, NormalBlock ) ):
                flagHaveNormalBlock = True
                valNB = b.value
                continue

            # Check if idx is an obstacle.
            if ( isinstance( b, ObstacleBlock ) ):
                val += b.value
                flagHaveNonNormalBlock = True
                continue

        # Check if all types of blocks are handled.
        if ( False == flagHaveNonNormalBlock and \
             False == flagHaveNormalBlock ):
            raise GridMapException("No blocks are recognized!")

        if ( False == flagHaveNonNormalBlock and \
             True  == flagHaveNormalBlock ):
            val += valNB
        
        return val


    def evaluate_coordinate_s(self, x, y):
        """
        This function returns the value coresponds to coor. The rules are as follows:
        (1) If coor is out of boundary but not exactly on the boundary, an exception will be raised.
        (2) If coor is sitting on a block corner, the values from the neighboring 4 blocks will be summed.
        (3) If coor is sitting on a horizontal or vertical line but not a block corner, the neighboring 2 blocks will be summed.
        (4) If coor is inside a block, the value of that block will be returned.

        For summation, it is processed as follows:
        * If neighboring block is out of boundary, an outOfBoundaryValue will be added.
        * If neighboring block is an obstacle, the value of an obstacle well be added.
        * If no neighboring block is either out of boundary or an obstacle, only one normal block will be counted.
        """

        # Check if (x, y) is out of boundary.
        if ( True == self.is_out_of_boundary_s( x, y ) ):
            raise GridMapException("Coordinate (%f, %f) out of boundary. Could not evaluate its value." % ( x, y ))
        
        # In or on the boundary.
        
        # Check if the coordinate is a corner, horizontal, or vertical line of the map.
        loc = self.is_corner_or_principle_line( BlockCoor( x, y ) )

        idxList = [] # The index list of neighoring blocks.
        idx = copy.deepcopy( loc[3] )

        if ( True == loc[0] ):
            # A corner.
            idxList.append( copy.deepcopy(idx) ); idx.c -= 1
            idxList.append( copy.deepcopy(idx) ); idx.r -= 1
            idxList.append( copy.deepcopy(idx) ); idx.c += 1
            idxList.append( copy.deepcopy(idx) )
        elif ( True == loc[1] ):
            # A horizontal line.
            idxList.append( copy.deepcopy(idx) ); idx.r -= 1
            idxList.append( copy.deepcopy(idx) )
        elif ( True == loc[2] ):
            # A vertical line.
            idxList.append( copy.deepcopy(idx) ); idx.c -= 1
            idxList.append( copy.deepcopy(idx) )
        else:
            # A normal block.
            idxList.append( idx )

        # Summation routine.
        val = self.sum_block_values( idxList )

        return val

    def evaluate_coordinate(self, coor):
        """Overloaded function. Only varys in argument list."""

        if ( isinstance( coor, BlockCoor ) ):
            return self.evaluate_coordinate_s( coor.x, coor.y )
        elif ( isinstance( coor, (list, tuple) ) ):
            return self.evaluate_coordinate_s( coor[GridMap2D.I_X], coor[GridMap2D.I_Y] )
        else:
            raise TypeError("coor should be either an object of BlockCoor or a list.")
    
    def convert_to_coordinates_s(self, r, c):
        """Convert the index into the real valued coordinates."""

        # Check if [r, c] is valid.
        assert( isinstance( r, (int, long) ) )
        assert( isinstance( c, (int, long) ) )
        # assert( r >= 0 and r < self.rows )
        # assert( c >= 0 and c < self.cols )

        return BlockCoor( c*self.stepSize[GridMap2D.I_X], r*self.stepSize[GridMap2D.I_Y] )

    def convert_to_coordinates(self, index):
        """
        Overloaded function. Only various in the argument list.
        """

        if ( isinstance(index, BlockIndex) ):
            return self.convert_to_coordinates_s( index.r, index.c )
        elif ( isinstance(index, (list, tuple)) ):
            return self.convert_to_coordinates_s( index[GridMap2D.I_R], index[GridMap2D.I_C] )
        else:
            raise TypeError("index must be either an ojbect of BlockIndex or a list.")

    def is_east_boundary(self, coor, eps = 1e-6):
        """Return True if coordinate x lies on the east boundary of the map."""

        assert( eps >= 0 )

        if ( 0 == eps ):
            return ( coor.x == self.corners[1][0] )
        else:
            return ( math.fabs( coor.x - self.corners[1][0] ) < eps )

    def is_north_boundary(self, coor, eps = 1e-6):
        """Return True if coordinate y lies on the north boundary of the map."""

        assert( eps >= 0 )

        if ( 0 == eps ):
            return ( coor.y == self.corners[2][1] )
        else:
            return ( math.fabs( coor.y - self.corners[2][1] ) < eps )
    
    def is_west_boundary(self, coor, eps = 1e-6):
        """Return True if coordinate x lies on the west boundary of the map."""

        assert( eps >= 0 )

        if ( 0 == eps ):
            return ( coor.x == self.corners[0][0] )
        else:
            return ( math.fabs( coor.x - self.corners[0][0] ) < eps )

    def is_south_boundary(self, coor, eps = 1e-6):
        """Return True if coordinate y lies on the south boundary of the map."""

        assert( eps >= 0 )

        if ( 0 == eps ):
            return ( coor.y == self.corners[0][1] )
        else:
            return ( math.fabs( coor.y - self.corners[0][1] ) < eps )

    def is_corner_or_principle_line(self, coor):
        """
        It is NOT rerquired that coor is inside the map.

        The return value contains 4 parts:
        (1) Ture if coor is precisely a corner.
        (2) Ture if coor lies on a horizontal principle line or is a corner.
        (3) Ture if coor lies on a vertical principle line or is a corner.
        (4) A BlockIndex object associated with coor.
        """

        # Get the index of (x, y).
        index = self.get_index_by_coordinates(coor)

        # Convert back to coordnates.
        coor2 = self.convert_to_coordinates(index)

        res = [ False, coor.y == coor2.y, coor.x == coor2.x, index ]

        res[0] = (res[1] == True) and (res[2] == True)

        return res

class GridMapEnv(object):
    def __init__(self, name = "DefaultGridMapEnv", gridMap = None):
        self.name = name
        self.map  = gridMap
        self.agentStartingLoc = None # Should be an object of BlockCoor.

        self.isTerminated = False
        self.nSteps = 0

        self.agentCurrentLoc = copy.deepcopy( self.agentStartingLoc )
        self.agentCurrentAct = None # Should be an object of BlockCoorDelta.

    def get_state_size(self):
        return self.agentCurrentLoc.size
    
    def get_action_size(self):
        return self.agentCurrentAct.size
    
    def reset(self):
        """Reset the evironment."""

        # Get the index of the starting point.
        index = self.map.get_index_starting_point()
        # Get the coordinates of index.
        coor = self.map.convert_to_coordinates(index)

        self.agentStartingLoc = BlockCoor( \
            coor.x + self.map.get_step_size[GridMap2D.I_X] / 2.0, \
            coor.y + self.map.get_step_size[GridMap2D.I_Y] / 2.0 \
        )
        
        # Reset the location of the agent.
        self.agentCurrentLoc = copy.deepcopy( self.agentStartingLoc )

        # Clear the cuurent action of the agent.
        self.agentCurrentAct = BlockCoorDelta( 0, 0 )

        # Clear step counter.
        self.nSteps = 0

        # Clear termination flag.
        self.isTerminated = False

    def step(self, action):
        """
        Return values are next state, reward value, termination flag, and None.
        action: An object of BlockCoorDelta.

        action will be deepcopied.
        """

        if ( True == self.isTerminated ):
            raise GridMapException("Episode already terminated.")
        
        self.agentCurrentAct = copy.deepcopy( action )

        newLoc, value, termFlag = self.try_move( self.agentCurrentLoc, self.agentCurrentAct )

        self.nSteps += 1

        if ( True == termFlag ):
            self.isTerminated = True

        return newLoc, value, termFlag, None

    def render(self, pause = 0):
        """Render with matplotlib.
        pause: Time measured in seconds to pause before close the rendered image.
        If pause < 1 then the rendered image will not be closed.
        """

        if ( self.map is None ):
            raise ValueError("self.map is None")

        from matplotlib.patches import Rectangle

        fig, ax = plt.subplots(1)

        for br in self.map.blockRows:
            for b in br:
                rect = Rectangle( (b.coor[0], b.coor[1]), b.size[1], b.size[0], fill = True)
                rect.set_facecolor(b.color)
                rect.set_edgecolor("k")
                ax.add_patch(rect)
        
        ax.autoscale()

        if ( pause < 1 ):
            plt.show()
        elif ( pause >= 1 ):
            print("Render %s for %f seconds." % (self.name, pause))
            plt.show( block = False )
            plt.pause( pause )
            plt.close()

    def can_move_east(self, coor):
        """
        coor is an object of BlockCoor.
        """

        if ( True == self.map.is_east_boundary(coor) ):
            return False
        
        if ( True == self.map.is_north_boundary(coor) or \
             True == self.map.is_south_boundary(coor) ):
            return False
            
        loc = self.map.is_corner_or_principle_line(coor)

        if ( (True == loc[0]) or (True == loc[1]) ):
            if ( isinstance( self.map.get_block( loc[3] ), ObstacleBlock ) ):
                return False
            
            index = copy.deepcopy(loc[3])
            index.r -= 1

            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            return True
        
        if ( True == loc[2] ):
            if ( isinstance( self.map.get_block( loc[3] ), ObstacleBlock ) ):
                return False

        return True
                
    def can_move_northeast(self, coor):
        """
        coor is an object of BlockCoor.
        """
        
        if ( True == self.map.is_east_boundary(coor) or \
             True == self.map.is_north_boundary(coor) ):
            return False
        
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            if ( isinstance( self.map.get_block(loc[3]), ObstacleBlock ) ):
                return False
            else:
                return True    
        
        if ( True == loc[1] ):
            if ( isinstance( self.map.get_block(loc[3]), ObstacleBlock ) ):
                return False
            else:
                return True

        if ( True == loc[2] ):
            if ( isinstance( self.map.get_block(loc[3]), ObstacleBlock ) ):
                return False
            else:
                return True

        return True

    def can_move_north(self, coor):
        """
        coor is an object of BlockCoor.
        """

        if ( True == self.map.is_north_boundary(coor) ):
            return False
        
        if ( True == self.map.is_east_boundary(coor) or \
             True == self.map.is_west_boundary(coor) ):
            return False
            
        loc = self.map.is_corner_or_principle_line(coor)

        if ( (True == loc[0]) or (True == loc[2]) ):
            if ( isinstance( self.map.get_block( loc[3] ), ObstacleBlock ) ):
                return False
            
            index = copy.deepcopy(loc[3])
            index.c -= 1

            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            return True
        
        if ( True == loc[1] ):
            if ( isinstance( self.map.get_block( loc[3] ), ObstacleBlock ) ):
                return False

        return True

    def can_move_northwest(self, coor):
        """
        coor is an object of BlockCoor.
        """
        
        if ( True == self.map.is_west_boundary(coor) or \
             True == self.map.is_north_boundary(coor) ):
            return False
        
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            index = copy.deepcopy(loc[3])
            index.c -= 1 # Left block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True    
        
        if ( True == loc[1] ):
            index = copy.deepcopy(loc[3])
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True

        if ( True == loc[2] ):
            index = copy.deepcopy(loc[3])
            index.c -= 1 # Left block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True

        return True

    def can_move_west(self, coor):
        """
        coor is an object of BlockCoor.
        """

        if ( True == self.map.is_west_boundary(coor) ):
            return False
        
        if ( True == self.map.is_north_boundary(coor) or \
             True == self.map.is_south_boundary(coor) ):
            return False
            
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            index = copy.deepcopy(loc[3])
            index.c -= 1 # Left block.
            
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            index.r -= 1 # Now bottom left block.

            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            return True
        
        if ( True == loc[1] ):
            index = copy.deepcopy(loc[3])
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False

            index.r -= 1 # Bottom block.
            
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False

        if ( True == loc[2] ):
            index = copy.deepcopy( loc[3] )
            index.c -= 1 # Left block.

            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False

        return True
    
    def can_move_southwest(self, coor):
        """
        coor is an object of BlockCoor.
        """
        
        if ( True == self.map.is_west_boundary(coor) or \
             True == self.map.is_south_boundary(coor) ):
            return False
        
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            index = copy.deepcopy(loc[3])
            index.c -= 1 # Left block.
            index.r -= 1 # Bottom left block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True    
        
        if ( True == loc[1] ):
            index = copy.deepcopy(loc[3])
            index.r -= 1 # Bottom block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True

        if ( True == loc[2] ):
            index = copy.deepcopy(loc[3])
            index.c -= 1 # Left block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True

        return True
    
    def can_move_south(self, coor):
        """
        coor is an object of BlockCoor.
        """

        if ( True == self.map.is_south_boundary(coor) ):
            return False
        
        if ( True == self.map.is_east_boundary(coor) or \
             True == self.map.is_west_boundary(coor) ):
            return False
            
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            index = copy.deepcopy(loc[3])
            index.r -= 1 # Bottom block.
            
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            index.c -= 1 # Now bottom left block.

            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False
            
            return True
        
        if ( True == loc[2] ):
            index = copy.deepcopy(loc[3])
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False

            index.c -= 1 # Left block.
            
            if ( isinstance( self.map.get_block( index ), ObstacleBlock ) ):
                return False

        if ( True == loc[1] ):
            index = copy.deepcopy( loc[3] )
            index.r -= 1 # Bottom block.

            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False

        return True

    def can_move_southeast(self, coor):
        """
        coor is an object of BlockCoor.
        """
        
        if ( True == self.map.is_east_boundary(coor) or \
             True == self.map.is_south_boundary(coor) ):
            return False
        
        loc = self.map.is_corner_or_principle_line(coor)

        if ( True == loc[0] ):
            index = copy.deepcopy(loc[3])
            index.r -= 1 # Bottom block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True    
        
        if ( True == loc[1] ):
            index = copy.deepcopy(loc[3])
            index.r -= 1 # Bottom block.
            if ( isinstance( self.map.get_block(index), ObstacleBlock ) ):
                return False
            else:
                return True

        if ( True == loc[2] ):
            if ( isinstance( self.map.get_block(loc[3]), ObstacleBlock ) ):
                return False
            else:
                return True

        return True

    def can_move(self, x, y, dx, dy):
        """Return True if the agent makes a valid line path 
        starts from (x, y) and goes to (x + dx, y + dy). Return False if 
        the agent could not go that direction."""

        coor = BlockCoor(x, y)

        # 8-way switch!
        if ( dx > 0 and dy == 0 ):
            # East direction.
            return self.can_move_east(coor)
        elif ( dx >0 and dy > 0 ):
            # Northeast direction.
            return self.can_move_northeast(coor)
        elif ( dx == 0 and dy > 0 ):
            # North direction.
            return self.can_move_north(coor)
        elif ( dx < 0 and dy > 0 ):
            # Northwest direction.
            return self.can_move_northwest(coor)
        elif ( dx < 0 and dy == 0 ):
            # West direction.
            return self.can_move_west(coor)
        elif ( dx < 0 and dy < 0 ):
            # Southwest direction.
            return self.can_move_southwest(coor)
        elif ( dx == 0 and dy < 0 ):
            # South direction.
            return self.can_move_south(coor)
        elif ( dx > 0 and dy < 0 ):
            # Southeast direction.
            return self.can_move_southeast(coor)
        else:
            raise ValueError("dx and dy may not both be zero at the same time.")

    def try_move(self, coorOri, coorDelta):
        """
        coorOri is an object of BlockCoor. Will be deepcopied.
        coorDelta is the delta.

        Return new location coordinate, block value, flag of termination.
        """

        coor = copy.deepcopy(coorOri)
        val  = 0 # The block value.

        # dx and dy.
        delta = coorDelta.convert_to_direction_delta()

        # Temporary indices.
        idxH = BlockIndex(0, 0)
        idxV = BlockIndex(0, 0)
        coorH = BlockCoor(0, 0)
        coorV = BlockCoor(0, 0)

        # Try to move.
        if ( True == self.can_move( coor.x, coor.y, delta.dx, delta.dy ) ):
            while ( True ):
                # Get the index of coor.
                index = self.map.get_index_by_coordinates( coor )

                # Get information on coor.
                loc = self.map.is_corner_or_principle_line( coor )

                # Get the targeting vertical and horizontal line index.
                if ( delta.dx >= 0 ):
                    idxV.c = index.c + int( delta.dx )
                else:
                    if ( True == loc[2] ):
                        # Starting from a vertical line.
                        idxV.c = index.c + int( delta.dx )
                    else:
                        idxV.c = index.c

                if ( delta.dy >= 0 ):
                    idxH.r = index.r + int( delta.dy )
                else:
                    if ( True == loc[1] ):
                        # Starting from a horizontal line.
                        idxH.r = index.r + int( delta.dy )
                    else:
                        idxH.r = index.r

                # Get the x coordinates for the vertical line.
                coorV = self.map.convert_to_coordinates( idxV )
                # Get the y coordinates for the horizontal line.
                coorH = self.map.convert_to_coordinates( idxH )

                # Find two possible intersections with these lines.
                [xV, yV], flagV = LineIntersection2D.line_intersect( \
                    coorOri.x, coorOri.y, coorOri.x + coorDelta.dx, coorOri.y + coorDelta.dy, \
                    coorV.x, self.map.corners[0][GridMap2D.I_Y], coorV.x, self.map.corners[3][GridMap2D.I_Y] )

                [xH, yH], flagH = LineIntersection2D.line_intersect( \
                    coorOri.x, coorOri.y, coorOri.x + coorDelta.dx, coorOri.y + coorDelta.dy, \
                    self.map.corners[0][GridMap2D.I_X], coorH.y, self.map.corners[1][GridMap2D.I_X], coorH.y )
                
                if ( LineIntersection2D.VALID_INTERSECTION == flagV ):
                    distV = two_point_distance( coor.x, coor.y, xV, yV )
                else:
                    distV = 0

                if ( LineIntersection2D.VALID_INTERSECTION == flagH ): 
                    distH = two_point_distance( coor.x, coor.y, xH, yH )
                else:
                    distH = 0

                if ( LineIntersection2D.VALID_INTERSECTION == flagV ):
                    if ( LineIntersection2D.VALID_INTERSECTION != flagH or \
                         distV < distH ):
                        # Check if (xV, yV) is on the boundary.
                        if ( True == self.map.is_out_of_or_on_boundary( BlockCoor( xV, yV ) ) ):
                            # Stop here.
                            coor.x, coor.y = xV, yV
                            break
                        
                        # Get the index at (xV, yV).
                        interIdxV = self.map.get_index_by_coordinates( BlockCoor(xV, yV) )

                        if ( delta.x < 0 ):
                            # Left direction.
                            interIdxV.c -= 1

                        if ( True == self.map.is_obstacle_block( interIdxV ) ):
                            # Stop here.
                            coor.x, coor.y = xV, yV
                            break
                        
                        coor.x, coor.y = xV, yV
                        continue
                        
                if ( LineIntersection2D.VALID_INTERSECTION == flagH ):
                    if ( LineIntersection2D.VALID_INTERSECTION == flagV and \
                         distV == distH ):
                        # Same distance.
                        # Check if (xH, yH) is on the boundary.
                        if ( True == self.map.is_out_of_or_on_boundary( BlockCoor( xH, yH ) ) ):
                            # Stop here.
                            coor.x, coor.y = xH, yH
                            break
                        
                        # Get the index at (xH, yH). 
                        interIdxH = self.map.get_index_by_coordinates( BlockCoor(xH, yH) )

                        # Since we are at a corner point, we simply checkout all four neighboring blocks.
                        flagCornerFoundObstacle = False

                        if ( False == flagCornerFoundObstacle and \
                             True == self.map.is_obstacle_block( interIdxH ) ):
                            flagCornerFoundObstacle = True
                        
                        interIdxH.c -= 1
                        if ( False == flagCornerFoundObstacle and \
                             True == self.map.is_obstacle_block( interIdxH ) ):
                            flagCornerFoundObstacle = True
                        
                        interIdxH.r -= 1
                        if ( False == flagCornerFoundObstacle and \
                             True == self.map.is_obstacle_block( interIdxH ) ):
                            flagCornerFoundObstacle = True
                        
                        interIdxH.c += 1
                        if ( False == flagCornerFoundObstacle and \
                             True == self.map.is_obstacle_block( interIdxH ) ):
                            flagCornerFoundObstacle = True
                        
                        if ( True == flagCornerFoundObstacle ):
                            # Stop here.
                            coor.x, coor.y = xH, yH
                            break
                        
                        coor.x, coor.y = xH, yH
                        continue
                    else:
                        # Not same distance.
                        # Check if (xH, yH) is on the boundary.
                        if ( True == self.map.is_out_of_or_on_boundary( BlockCoor( xH, yH ) ) ):
                            # Stop here.
                            coor.x, coor.y = xH, yH
                            break
                        
                        # Get the index at (xH, yH).
                        interIdxH = self.map.get_index_by_coordinates( BlockCoor(xH, yH) )

                        if ( delta.y < 0 ):
                            # Downwards direction.
                            interIdxH.r -= 1

                        if ( True == self.map.is_obstacle_block( interIdxH ) ):
                            # Stop here.
                            coor.x, coor.y = xH, yH
                            break
                        
                        coor.x, coor.y = xH, yH
                        continue
                
                # No valid intersectons. Stop here.
                coor.x = coorOri.x + coorDelta.dx
                coor.y = coorOri.y + coorDelta.dy
                break

            val = self.map.evaluate_coordinate( coor )
        else:
            # Cannot move.
            val = self.map.evaluate_coordinate( coor )

        # Check if it is in the ending point.
        flagTerm = False

        if ( True == self.map.is_in_ending_point( coor ) ):
            flagTerm = True

        return coor, val, flagTerm

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
    gm2d.set_starting_point((0, 0))
    gm2d.set_ending_point((9, 19))
    gm2d.add_obstacle((4, 10))
    gm2d.add_obstacle((5, 10))
    gm2d.add_obstacle((6, 10))

    # Describe the map.
    print(gm2d)

    # import ipdb; ipdb.set_trace()

    # Test GridMap2D.evaluate_coordinate
    print("Value of (   0,      0) is %f" % ( gm2d.evaluate_coordinate( (0, 0) ) ) )
    print("Value of (19.99,  9.99) is %f" % ( gm2d.evaluate_coordinate( (19.99, 9.99) ) ) )
    print("Value of (19.99,     0) is %f" % ( gm2d.evaluate_coordinate( (19.99, 0) ) ) )
    print("Value of (    0,  9.99) is %f" % ( gm2d.evaluate_coordinate( (0, 9.99) ) ) )
    print("Value of (   10,     4) is %f" % ( gm2d.evaluate_coordinate( (10, 4) ) ) )
    print("Value of (   10,     5) is %f" % ( gm2d.evaluate_coordinate( (10, 5) ) ) )
    print("Value of (   10,     6) is %f" % ( gm2d.evaluate_coordinate( (10, 6) ) ) )
    print("Value of (   10,   5.5) is %f" % ( gm2d.evaluate_coordinate( (10, 5.5) ) ) )
    print("Value of ( 10.5,     5) is %f" % ( gm2d.evaluate_coordinate( (10.5, 5) ) ) )
    print("Value of (10.99,  5.99) is %f" % ( gm2d.evaluate_coordinate( (10.99, 5.99) ) ) )
    print("Value of (   -1,    -1) is %f" % ( gm2d.evaluate_coordinate( (-1, -1) ) ) )
    print("Value of (    9, -0.01) is %f" % ( gm2d.evaluate_coordinate( (9, -0.01) ) ) )
    print("Value of (    9, 10.01) is %f" % ( gm2d.evaluate_coordinate( (9, 10.01) ) ) )
    print("Value of (-0.01,     5) is %f" % ( gm2d.evaluate_coordinate( (-0.01, 5) ) ) )
    print("Value of (20.01,     5) is %f" % ( gm2d.evaluate_coordinate( (20.01, 5) ) ) )

    # Create a GridMapEnv object.
    gme = GridMapEnv(gridMap = gm2d)

    # Render.
    gme.render()
