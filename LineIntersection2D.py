
from __future__ import print_function

import numpy as np

def line_intersect(x0, y0, x1, y1, x2, y2, x3, y3, eps = 1e-6):
    """
    Calculates the interscetion point of two line segments (x0, y0) - (x1, y1) and
    (x2, y2) - (x3, y3). 
    
    The return values are [x, y] and a flag. flag == True means a valid intersection 
    point is fund. flag == False means otherwise.

    The function will test if these two lines are parallel by
    comparing the differences of x2 - x0 and x3 - x1, y2 - y0 and y3 - y1. If these 
    difference falls with in a range specified by eps, then these two lines are
    considered to be parallel to each other. If parallel lines are detected, this 
    function returns False as the value of flag.

    In case of non-parallel lines, the function calculates the intersection point
    with the extended lines of the input line segments. Then the intersection point
    is test against the extent of these two lines.
    """
