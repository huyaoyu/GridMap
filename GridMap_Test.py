from __future__ import print_function

import GridMap

import unittest

class TestGridMap2D(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20
        self.map = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)
        self.map.initialize()

        # Create a starting point and an ending point.
        startingPoint = GridMap.StartingPoint()
        endingPoint   = GridMap.EndingPoint()

        # Create an obstacle block.
        obstacle = GridMap.ObstacleBlock()

        # Overwrite blocks.
        self.map.set_starting_point(0, 0)
        self.map.set_ending_point(9, 19)
        self.map.add_obstacle(4, 10)
        self.map.add_obstacle(5, 10)
        self.map.add_obstacle(6, 10)

        # # Describe the map.
        # print(gm2d)

    def test_evaluate_coordinates(self):
        print("test_evaluate_coordinates")

        self.assertEqual( self.map.evaluate_coordinate( (    0,    0) ),    0 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99, 9.99) ),  100 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99,    0) ),    1 )
        self.assertEqual( self.map.evaluate_coordinate( (    0, 9.99) ),    1 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    4) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    6) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,  5.5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( ( 10.5,    5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (10.99, 5.99) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   -1,   -1) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (    9,-0.01) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (    9,10.01) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (-0.01,    5) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (20.01,    5) ), -200 )

    def test_get_block(self):
        print("test_get_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.StartingPoint) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.EndingPoint) )
        
        index.r = 5; index.c = 10
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.ObstacleBlock) )

    def test_get_step_size(self):
        print("test_get_step_size")

        self.assertEqual( self.map.get_step_size(), [1, 1] )

    def test_get_index_starting_point(self):
        print("test_get_index_starting_point")

        self.assertEqual( self.map.get_index_starting_point(), [0, 0] )

    def test_get_index_ending_point(self):
        print("test_get_index_ending_point")

        self.assertEqual( self.map.get_index_ending_point(), [ self.rows-1, self.cols-1 ] )

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestGridMap2D )
    unittest.TextTestRunner().run( suite )