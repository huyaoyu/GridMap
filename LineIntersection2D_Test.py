
from __future__ import print_function

import LineIntersection2D

import unittest

class TestLineIntersection(unittest.TestCase):
    def setUp(self):
        self.eps = 1e-6

    def test_normal_intersection(self):
        """Test if a normal intersection could be calculated."""

        print("test_normal_intersection")

        x0 = 1; y0 = 0
        x1 = 1; y1 = 2
        x2 = 0; y2 = 1
        x3 = 2; y3 = 1

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )
        
        self.assertEqual( flag, LineIntersection2D.VALID_INTERSECTION, "flag should be VALID_INTERSECTION")
        self.assertEqual( x, 1.0, "x == 1.0" )
        self.assertEqual( y, 1.0, "y == 1.0" )
        # self.assertTrue( False, "Manually fail the test function." )

    def test_x_axis_parallel(self):
        """Test the case of two parallel lines."""

        print("test_x_axis_parallel")

        x0, y0 = 0, 1
        x1, y1 = 2, 1
        x2, y2 = 0, 2
        x3, y3 = 2, 2

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )
        
        self.assertEqual( flag, LineIntersection2D.PARALLAL, "flag should be PARALLAL")
        self.assertIsNone( x, "x is None" )
        self.assertIsNone( y, "y is None" )
        
    def test_y_axis_parallel(self):
        """Test the case of two parallel lines."""

        print("test_y_axis_parallel")

        x0, y0 = 0, 0
        x1, y1 = 0, 2
        x2, y2 = 2, 0
        x3, y3 = 2, 2

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )
        
        self.assertEqual( flag, LineIntersection2D.PARALLAL, "flag should be PARALLAL")
        self.assertIsNone( x, "x is None" )
        self.assertIsNone( y, "y is None" )

    def test_parallel(self):
        """Test the case of two parallel lines."""

        print("test_parallel")

        x0, y0 = 0, 0
        x1, y1 = 1, 2
        x2, y2 = 1, 0
        x3, y3 = 2, 2

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )
        
        self.assertEqual( flag, LineIntersection2D.PARALLAL, "flag should be PARALLAL")
        self.assertIsNone( x, "x is None" )
        self.assertIsNone( y, "y is None" )

    def test_intersection_01(self):
        """Test the case of two valid intersection."""

        print("test_intersection_01")

        x0, y0 = 0, 0
        x1, y1 = 1, 2
        x2, y2 = 0, 2
        x3, y3 = 1, 0

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )

        self.assertEqual( flag, LineIntersection2D.VALID_INTERSECTION )
        self.assertEqual( x, 0.5, "x == 0.5" )
        self.assertEqual( y, 1.0, "y == 1.0" )
    
    def test_intersection_02(self):
        """Test the case of two valid intersection."""

        print("test_intersection_02")

        x0, y0 = 1, 2
        x1, y1 = 0, 0
        x2, y2 = 0, 2
        x3, y3 = 1, 0

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )

        self.assertEqual( flag, LineIntersection2D.VALID_INTERSECTION, "flag = {}".format(flag) )
        self.assertEqual( x, 0.5, "x is expected to be 0.5, x = {}".format(x) )
        self.assertEqual( y, 1.0, "y is expected to be 1.0, y = {}".format(y) )
        
    def test_fall_out_01(self):
        """Test the case of fall out intersection."""

        print("test_fall_out_01")

        x0, y0 = 1, 0
        x1, y1 = 0, 1
        x2, y2 = 0, 0
        x3, y3 = -1, -1

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )

        self.assertEqual( flag, LineIntersection2D.FALL_OUT_INTERSECTION )
        self.assertEqual( x, 0.5 )
        self.assertEqual( y, 0.5 )

    def test_fall_out_02(self):
        """Test the case of fall out intersection."""

        print("test_fall_out_02")

        x0, y0 = -1, 1
        x1, y1 = 0, 0
        x2, y2 = 1, 0
        x3, y3 = 0, -1

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )

        self.assertEqual( flag, LineIntersection2D.FALL_OUT_INTERSECTION )
        self.assertEqual( x, 0.5 )
        self.assertEqual( y, -0.5 )
    
    def test_common_point(self):
        """Test intersection at common end points."""

        print("test_common_point")

        x0, y0 = -1, -1
        x1, y1 = -2, -2
        x2, y2 = 1, 0.5
        x3, y3 = -1, -1

        [x, y], flag = LineIntersection2D.line_intersect( \
            x0, y0, x1, y1, x2, y2, x3, y3, self.eps )

        self.assertEqual( flag, LineIntersection2D.VALID_INTERSECTION )
        self.assertEqual( x, -1.0 )
        self.assertEqual( y, -1.0 )

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestLineIntersection )
    unittest.TextTestRunner().run( suite )
