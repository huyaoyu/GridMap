
from __future__ import print_function

import math
import numpy as np

VALID_INTERSECTION    = 0
FALL_OUT_INTERSECTION = 1
NO_VALID_INTERSECTION = 2

def line_intersect(x0, y0, x1, y1, x2, y2, x3, y3, eps = 1e-6):
    """
    Calculates the interscetion point of two line segments (x0, y0) - (x1, y1) and
    (x2, y2) - (x3, y3). 

    It is assumed that x1 >= x0, y1 >= y0, x3 >= x2, and y3 >= y2.
    
    The return values are [x, y] and a flag. flag == VALID_INTERSECTION means a valid intersection 
    point is found. flag == FALL_OUT_INTERSECTION means intersection doese not fall into the line segments. 
    flag == NO_VALID_INTERSECTION means parallel lines or other situations, such as degenerated line segments.

    The function will test if these two lines are parallel by
    comparing the differences of x2 - x0 and x3 - x1, y2 - y0 and y3 - y1. If these 
    difference falls with in a range specified by eps, then these two lines are
    considered to be parallel to each other. If parallel lines are detected, this 
    function returns NO_VALID_INTERSECTION as the value of flag. eps must be a positive number.

    In case of non-parallel lines, the function calculates the intersection point
    with the extended lines of the input line segments. Then the intersection point
    is tested against the extent of these two lines. If the intersection falls into both
    of these line segments, then it is treated as a valid intersection, flag will be VALID_INTERSECTION. 
    Otherwise, flag will be FALL_OUT_INTERSECTION.

    For both the cases of flag == VALID_INTERSECTION and flag == FALL_OUT_INTERSECTION, the
    returned [x, y] contains the intersection point. For other cases, [x, y] is [None, None].
    """

    # Test the order of input arguments.
    assert( x1 >= x0 )
    assert( y1 >= y0 )
    assert( x3 >= x2 )
    assert( y3 >= y2 )
    assert( eps > 0 )

    # Initialize the return values.
    x    = None
    y    = None
    flag = NO_VALID_INTERSECTION

    dx0 = x1 - x0
    dy0 = y1 - y0

    dx2 = x3 - x2
    dy2 = y3 - y2

    # Test if lines segments are degenerated.
    if ( math.sqrt( dx0**2 + dy0**2 ) < eps ):
        return [x, y], flag
    
    if ( math.sqrt( dx2**2 + dy2**2 ) < eps ):
        return [x, y], flag

    # Test if lines are parallel.
    if ( math.fabs( (x2 - x0) - (x3 - x1) ) < eps and \
         math.fabs( (y2 - y0) - (y3 - y1) ) < eps ):
        return [x, y], flag        

    # ========== Intersection calculation. ==========

    # Calculate the intersection.
    a11 = dy0; a12 = -dx0
    a21 = dy2; a22 = -dx2

    AI = np.array( \
        [ [  a22, -a12 ], \
          [ -a21,  a11 ] ],\
        dtype = np.float32 ) / ( a11*a22 - a12*a21 )
    RHS = np.array([ x0*y1 - x1*y0, x2*y3 - x3*y2 ], dtype = np.float32).reshape((2, 1))

    X = AI.dot( RHS )
    x = X[0, 0]; y = X[1, 0]

    # Test if the intersection falls into the line segments.
    if ( x >= x0 and x <= x1 and \
         x >= x2 and x <= x3 and \
         y >= y0 and y <= y1 and \
         y >= y2 and y <= y3 ):
        flag = VALID_INTERSECTION
    else:
        flag = FALL_OUT_INTERSECTION

    return [ x, y ], flag
