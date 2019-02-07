
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
        
        self.assertEqual( x, 1.0, "x == 1.0" )
        self.assertEqual( y, 1.0, "y == 1.0" )
        self.assertEqual( flag, LineIntersection2D.VALID_INTERSECTION, "flag should be VALID_INTERSECTION")
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
        
        self.assertIsNone( x, "x is None" )
        self.assertIsNone( y, "y is None" )
        self.assertEqual( flag, LineIntersection2D.NO_VALID_INTERSECTION, "flag should be NO_VALID_INTERSECTION")
        # self.assertTrue( False, "Manually fail the test function." )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestLineIntersection )
    unittest.TextTestRunner().run( suite )
