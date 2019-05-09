from __future__ import print_function

import copy
import math
import os
import unittest

import GridMap

class TestGridMap2D(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20
        self.map = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)

        self.map.set_value_normal_block(-1)
        self.map.set_value_starting_block(0)
        self.map.set_value_ending_block(100)
        self.map.set_value_obstacle_block(-100)

        self.map.initialize()

        # Overwrite blocks.
        self.map.set_starting_block((0, 0))
        self.map.set_ending_block((9, 19))
        self.map.add_obstacle((0, 10))
        self.map.add_obstacle((4, 10))
        self.map.add_obstacle((5,  0))
        self.map.add_obstacle((5,  9))
        self.map.add_obstacle((5, 10))
        self.map.add_obstacle((5, 11))
        self.map.add_obstacle((5, 19))
        self.map.add_obstacle((6, 10))
        self.map.add_obstacle((9, 10))

        # # Describe the map.
        # print(gm2d)

    def test_evaluate_coordinates(self):
        print("test_evaluate_coordinates")

        self.assertEqual( self.map.evaluate_coordinate( (    0,    0) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (  0.5,  0.5) ),    0 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99, 9.99) ),  100 )
        self.assertEqual( self.map.evaluate_coordinate( ( 20.0, 10.0) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99, 0.01) ),   -1 )
        self.assertEqual( self.map.evaluate_coordinate( ( 0.01, 9.99) ),   -1 )
        self.assertEqual( self.map.evaluate_coordinate( ( 0.00, 10.0) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    4) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    5) ), -300 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    6) ), -300 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    7) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( ( 10.5,    4) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( ( 10.5,    7) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (    9,  4.5) ),   -1 )
        self.assertEqual( self.map.evaluate_coordinate( (10.99, 4.99) ), -100 )

        self.assertRaises( GridMap.GridMapException, self.map.evaluate_coordinate, (   -1,   -1) )
        self.assertRaises( GridMap.GridMapException, self.map.evaluate_coordinate, (    9,-0.01) )
        self.assertRaises( GridMap.GridMapException, self.map.evaluate_coordinate, (    9,10.01) )
        self.assertRaises( GridMap.GridMapException, self.map.evaluate_coordinate, (-0.01,    5) )
        self.assertRaises( GridMap.GridMapException, self.map.evaluate_coordinate, (20.01,    5) )

    def test_get_block(self):
        print("test_get_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.StartingBlock) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.EndingBlock) )
        
        index.r = 5; index.c = 10
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.ObstacleBlock) )

    def test_is_normal_block(self):
        print("test_is_normal_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertFalse( self.map.is_normal_block( index ) )
        
        index.r = 4
        index.c = 9
        self.assertTrue( self.map.is_normal_block( index ) )

        index.r = 4
        index.c = 10
        self.assertFalse( self.map.is_normal_block( index ) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertFalse( self.map.is_normal_block( index ) )

    def test_is_obstacle_block(self):
        print("test_is_obstacle_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertFalse( self.map.is_obstacle_block( index ) )
        
        index.r = 4
        index.c = 9
        self.assertFalse( self.map.is_obstacle_block( index ) )

        index.r = 4
        index.c = 10
        self.assertTrue( self.map.is_obstacle_block( index ) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertFalse( self.map.is_obstacle_block( index ) )

    def test_is_starting_block(self):
        print("test_is_starting_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertTrue( self.map.is_starting_block( index ) )
        
        index.r = 4
        index.c = 9
        self.assertFalse( self.map.is_starting_block( index ) )

        index.r = 4
        index.c = 10
        self.assertFalse( self.map.is_starting_block( index ) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertFalse( self.map.is_starting_block( index ) )

    def test_is_ending_block(self):
        print("test_is_starting_block")
        
        index = GridMap.BlockIndex( 0, 0 )
        self.assertFalse( self.map.is_ending_block( index ) )
        
        index.r = 4
        index.c = 9
        self.assertFalse( self.map.is_ending_block( index ) )

        index.r = 4
        index.c = 10
        self.assertFalse( self.map.is_ending_block( index ) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertTrue( self.map.is_ending_block( index ) )

    def test_get_step_size(self):
        print("test_get_step_size")

        self.assertEqual( self.map.get_step_size(), [1, 1] )

    def test_get_index_starting_block(self):
        print("test_get_index_starting_block")

        self.assertEqual( self.map.get_index_starting_block().r, 0 )
        self.assertEqual( self.map.get_index_starting_block().c, 0 )

    def test_get_index_ending_block(self):
        print("test_get_index_ending_block")

        self.assertEqual( self.map.get_index_ending_block().r, self.rows-1 )
        self.assertEqual( self.map.get_index_ending_block().c, self.cols-1 )

    def test_is_in_ending_block(self):
        print("test_is_in_ending_block")

        coor = GridMap.BlockCoor( \
            (self.cols-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_X], \
            (self.rows-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_in_ending_block( coor ) )

        # Not in ending block.
        coor.x = (self.cols-1) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.y = (self.rows-1) * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.x = self.cols * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.x = (self.cols-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.x = (self.cols-1.0) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = (self.rows-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.x = (self.cols-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = (self.rows-1.0) * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

        coor.x = (self.cols-0.0) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = (self.rows-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_in_ending_block( coor ) )

    def test_is_around_ending_block(self):
        print("test_is_around_ending_block")

        coor = GridMap.BlockCoor( \
            (self.cols-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_X], \
            (self.rows-0.5) * self.map.get_step_size()[GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_around_ending_block( coor, 1.0 ) )

        coorTemp = copy.deepcopy( coor )

        # Out of the range of the ending point in terms of x-coordinate.
        coor.x = (self.cols-2) * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_around_ending_block( coor, 1.0 ) )

        # Out of the range of the ending point in terms of y-coordinate.
        coor = copy.deepcopy( coorTemp )
        coor.y = (self.rows-2) * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_around_ending_block( coor, 1.0 ) )

        # Right out of the range of the ending point in terms of x-coordinate.
        coor = copy.deepcopy( coorTemp )
        stepX = self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.x = (self.cols-1.6) * stepX
        self.assertFalse( self.map.is_around_ending_block( coor, stepX ) )

        # Right out of the range of the ending point in terms of y-coordinate.
        coor = copy.deepcopy( coorTemp )
        stepY = self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        coor.y = (self.rows-1.6) * stepY
        self.assertFalse( self.map.is_around_ending_block( coor, stepY ) )

        # Right in the range of the ending point in terms of x-coordinate.
        coor = copy.deepcopy( coorTemp )
        stepX = self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.x = (self.cols-1.4) * stepX
        self.assertTrue( self.map.is_around_ending_block( coor, stepX ) )

        # Right in the range of the ending point in terms of y-coordinate.
        coor = copy.deepcopy( coorTemp )
        stepY = self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        coor.y = (self.rows-1.4) * stepY
        self.assertTrue( self.map.is_around_ending_block( coor, stepY ) )

        # Right out of the range of the ending point in terms of x- anc y-coordinates.
        coor = copy.deepcopy( coorTemp )
        stepX = self.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepY = self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        coor.x = (self.cols-1.6) * stepX
        coor.y = (self.rows-1.6) * stepY
        self.assertFalse( self.map.is_around_ending_block( coor, math.sqrt( stepX**2 + stepY**2 ) ) )

    def test_set_starting_block(self):
        print("test_set_starting_block")

        # Get the index of the original starting block.
        idxOri = self.map.get_index_starting_block()

        # Set new starting block.
        idxNew = GridMap.BlockIndex( 1, 2 )
        self.map.set_starting_block( idxNew )

        # Test the new set starting block.
        idxNew2 = self.map.get_index_starting_block()
        self.assertEqual( idxNew2.r, idxNew.r )
        self.assertEqual( idxNew2.c, idxNew.c )

        # The original point must be a NormalBlock.
        # import ipdb; ipdb.set_trace()
        self.assertTrue( isinstance( self.map.get_block(idxOri), GridMap.NormalBlock ) )

        # Recover the original staring point.
        self.map.set_starting_block( idxOri )

        # The idxNew point now should be a NormalBlock.
        self.assertTrue( isinstance( self.map.get_block(idxNew), GridMap.NormalBlock ) )

    def test_set_ending_block(self):
        print("test_set_ending_block")

        # Get the index of the original ending block.
        idxOri = self.map.get_index_ending_block()

        # Set new ending block.
        idxNew = GridMap.BlockIndex( self.rows - 2, self.cols - 3 )
        self.map.set_ending_block( idxNew )

        # Test the new set ending block.
        idxNew2 = self.map.get_index_ending_block()
        self.assertEqual( idxNew2.r, idxNew.r )
        self.assertEqual( idxNew2.c, idxNew.c )

        # The original point must be a NormalBlock.
        # import ipdb; ipdb.set_trace()
        self.assertTrue( isinstance( self.map.get_block(idxOri), GridMap.NormalBlock ) )

        # Recover the original ending block.
        self.map.set_ending_block( idxOri )

        # The idxNew point now should be a NormalBlock.
        self.assertTrue( isinstance( self.map.get_block(idxNew), GridMap.NormalBlock ) )

    def test_is_out_of_or_on_boundary(self):
        print("test_is_out_of_or_on_boundary")

        coor   = GridMap.BlockCoor( 0.01, 0.01 )
        coorIn = copy.deepcopy( coor )

        # In boundaries.
        self.assertFalse( self.map.is_out_of_or_on_boundary( coorIn ) )

        # Out of the east boundary.
        coor.x = self.cols*self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coorIn.x = coor.x - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        # Out of the north boundary.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coor.x = 0.01
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coorIn.x = coor.x
        coorIn.y = coor.y - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        coorIn.x = 0.01
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )
        
        # Out of the west boundary.
        coor.x = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[3][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coor.y = 0.01
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coorIn.x = coor.x + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X] + 0.01
        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        # Out of the south boundary.
        coor.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_or_on_boundary(coor) )

        coorIn.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = coor.y + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y] + 0.01
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

        coorIn.x = coor.x
        self.assertFalse( self.map.is_out_of_or_on_boundary(coorIn) )

    def test_is_out_of_boundary(self):
        print("test_is_out_of_boundary")

        coor   = GridMap.BlockCoor( 0.01, 0.01 )
        coorIn = copy.deepcopy( coor )

        # In boundaries.
        self.assertFalse( self.map.is_out_of_boundary( coorIn ) )

        # Out of the east boundary.
        coor.x = self.cols*self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_out_of_boundary(coor) )

        coor.x += 0.01
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        # Out of the north boundary.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertFalse( self.map.is_out_of_boundary(coor) )

        coor.y += 0.01
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x
        coorIn.y = coor.y - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.x = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )
        
        # Out of the west boundary.
        coor.x = 0
        coor.y = self.map.corners[3][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_out_of_boundary(coor) )

        coor.x = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.y = 0.01
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X] + 0.01
        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        # Out of the south boundary.
        coor.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = 0
        self.assertFalse( self.map.is_out_of_boundary(coor) )

        coor.y = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = coor.y + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y] + 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.x = coor.x
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

    def test_get_index_by_coordinates(self):
        print("test_get_index_by_coordinates")

        # (0, 0) should be [0, 0]
        coor = GridMap.BlockCoor( 0, 0 )

        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, 0 )
        self.assertEqual( index.c, 0 )

        # (0.5, 0.5) * step_size should be [0, 0]
        coor.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, 0 )
        self.assertEqual( index.c, 0 )

        # corner - ( 0.5, 0.5 ) * step_size should be the upper right corner.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, self.rows - 1 )
        self.assertEqual( index.c, self.cols - 1 )

    def test_convert_to_coordinates(self):
        print("test_convert_to_coordinates")

        # [0, 0] should be (0.0, 0.0)
        index = GridMap.BlockIndex( 0, 0 )

        coor = self.map.convert_to_coordinates(index)
        self.assertEqual( coor.x, 0.0 )
        self.assertEqual( coor.y, 0.0 )

        # [ rows-1, cols-1 ] should be upper right corner - step_size.
        index.r = self.rows - 1
        index.c = self.cols - 1
        coor = self.map.convert_to_coordinates(index)
        self.assertEqual( coor.x, \
            self.map.corners[2][GridMap.GridMap2D.I_X] - self.map.get_step_size()[GridMap.GridMap2D.I_X] )
        self.assertEqual( coor.y, \
            self.map.corners[2][GridMap.GridMap2D.I_Y] - self.map.get_step_size()[GridMap.GridMap2D.I_Y] )
        
    def test_is_xxx_boundary(self):
        print("test_is_xxx_boundary")

        coorNB = GridMap.BlockCoor(0, 0)

        # East boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[1][GridMap.GridMap2D.I_X], \
            self.map.corners[1][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_east_boundary( coor ) )

        coor.y = 0.5 * ( \
            self.map.corners[1][GridMap.GridMap2D.I_Y] + \
            self.map.corners[2][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_east_boundary( coor ) )        

        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_east_boundary( coor ) )

        coorNB.x = coor.x - 0.01
        coorNB.y = coor.y
        self.assertFalse( self.map.is_east_boundary( coorNB ) )

        # North boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[2][GridMap.GridMap2D.I_X], \
            self.map.corners[2][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_north_boundary( coor ) )

        coor.x = 0.5 * ( \
            self.map.corners[2][GridMap.GridMap2D.I_X] + \
            self.map.corners[3][GridMap.GridMap2D.I_X] )
        self.assertTrue( self.map.is_north_boundary( coor ) )        

        coor.x = self.map.corners[3][GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_north_boundary( coor ) )

        coorNB.x = coor.x
        coorNB.y = coor.y - 0.01
        self.assertFalse( self.map.is_north_boundary( coorNB ) )

        # West boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[3][GridMap.GridMap2D.I_X], \
            self.map.corners[3][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_west_boundary( coor ) )

        coor.y = 0.5 * ( \
            self.map.corners[0][GridMap.GridMap2D.I_Y] + \
            self.map.corners[3][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_west_boundary( coor ) )        

        coor.y = self.map.corners[0][GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_west_boundary( coor ) )

        coorNB.x = coor.x + 0.01
        coorNB.y = coor.y
        self.assertFalse( self.map.is_west_boundary( coorNB ) )

        # South boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[0][GridMap.GridMap2D.I_X], \
            self.map.corners[0][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_south_boundary( coor ) )

        coor.x = 0.5 * ( \
            self.map.corners[0][GridMap.GridMap2D.I_X] + \
            self.map.corners[1][GridMap.GridMap2D.I_X] )
        self.assertTrue( self.map.is_south_boundary( coor ) )        

        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_south_boundary( coor ) )

        coorNB.x = coor.x
        coorNB.y = coor.y + 0.01
        self.assertFalse( self.map.is_south_boundary( coorNB ) )

    def test_is_corner_or_principle_line(self):
        print("test_is_corner_or_principle_line")

        # (0, 0).
        coor = GridMap.BlockCoor(0, 0)

        loc = self.map.is_corner_or_principle_line(coor)
        self.assertTrue( loc[0] )
        self.assertTrue( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, 0 )
        self.assertEqual( loc[3].c, 0 )

        # Upper right corner.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y] - \
            self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        loc = self.map.is_corner_or_principle_line( coor )
        self.assertTrue( loc[0] )
        self.assertTrue( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, self.rows-1 )
        self.assertEqual( loc[3].c, self.cols-1 )

        # Upper left corner.
        coor.x = self.map.corners[3][GridMap.GridMap2D.I_X] + \
            self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[3][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]

        loc = self.map.is_corner_or_principle_line( coor )
        self.assertFalse( loc[0] )
        self.assertFalse( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, self.rows-1 )
        self.assertEqual( loc[3].c, 1 )

        # Lower right corner.
        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[1][GridMap.GridMap2D.I_Y] + \
            self.map.get_step_size()[GridMap.GridMap2D.I_Y]

        loc = self.map.is_corner_or_principle_line( coor )
        self.assertFalse( loc[0] )
        self.assertTrue( loc[1] )
        self.assertFalse( loc[2] )
        self.assertEqual( loc[3].r, 1 )
        self.assertEqual( loc[3].c, self.cols-1 )

    def test_dump_read_JSON(self):
        print("test_dump_read_JSON")

        if ( not os.path.isdir( "./WD_TestGridMap2D" ) ):
            os.makedirs("./WD_TestGridMap2D")

        self.map.dump_JSON( "./WD_TestGridMap2D/Map.json" )

        # Read the file back.
        tempMap = GridMap.GridMap2D(rows=1, cols=1)
        tempMap.read_JSON( "./WD_TestGridMap2D/Map.json" )
        print(tempMap)

class TestGridMap2D_WithPotential(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20
        self.map = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)

        self.map.set_value_normal_block(-1)
        self.map.set_value_starting_block(0)
        self.map.set_value_ending_block(100)
        self.map.set_value_obstacle_block(-100)

        self.map.initialize()

        # Potential value settings.
        self.map.enable_potential_value( valMax=10, valPerStep=1 )

        # Overwrite blocks.
        self.map.set_starting_block((0, 0))
        self.map.set_ending_block((9, 19))
        self.map.add_obstacle((0, 10))
        self.map.add_obstacle((4, 10))
        self.map.add_obstacle((5,  0))
        self.map.add_obstacle((5,  9))
        self.map.add_obstacle((5, 10))
        self.map.add_obstacle((5, 11))
        self.map.add_obstacle((5, 19))
        self.map.add_obstacle((6, 10))
        self.map.add_obstacle((9, 10))

        # # Describe the map.
        # print(gm2d)

    def test_block_value_with_potential(self):
        print("test_block_value_with_potential")

        idx = GridMap.BlockIndex(8, 19)
        v = self.map.get_block(idx).value

        self.assertEqual( v, 8 )

        idx.r = 9
        idx.c = 18
        v = self.map.get_block(idx).value

        self.assertEqual( v, 8 )

class TestGridMapEnv(unittest.TestCase):
    def setUp(self):
        self.haveGUI = False # Change this to False when testing on a remote servet that has no GUI.
        self.rows = 10
        self.cols = 20
        gridMap = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)

        gridMap.set_value_normal_block(-1)
        gridMap.set_value_starting_block(0)
        gridMap.set_value_ending_block(100)
        gridMap.set_value_obstacle_block(-100)

        gridMap.initialize()
        # Overwrite blocks.
        gridMap.set_starting_block((0, 0))
        gridMap.set_ending_block((9, 19))
        gridMap.add_obstacle((0, 10))
        gridMap.add_obstacle((4, 10))
        gridMap.add_obstacle((5,  0))
        gridMap.add_obstacle((5,  9))
        gridMap.add_obstacle((5, 10))
        gridMap.add_obstacle((5, 11))
        gridMap.add_obstacle((5, 19))
        gridMap.add_obstacle((6, 10))
        gridMap.add_obstacle((9, 10))

        # stepX = gridMap.get_step_size()[ GridMap.GridMap2D.I_X ]
        # stepY = gridMap.get_step_size()[ GridMap.GridMap2D.I_Y ]
        # radius = math.sqrt( stepX**2 + stepY**2 )

        self.workingDir = "./WD_TestGridMapEnv"

        self.gme = GridMap.GridMapEnv( gridMap = gridMap, workingDir = self.workingDir )
        self.gme.reset()

        # # Describe the map.
        # print(self.gme.map)

        # Predefined points to be tested.
        self.points = []
        self.points.append( GridMap.BlockCoor( 12.0, 5.5 ) )
        self.points.append( GridMap.BlockCoor( 12.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.5, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 6.5 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.5, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 6.5 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.5, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 5.5 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor(  9.5, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 4.5 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 10.5, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 4.5 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 11.5, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 12.0, 5.0 ) )

        self.boundaryPoints = []
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0,  0.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0,  4.5 ) )
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  9.5, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0,  4.5 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0,  0.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  9.5,  0.0 ) )

    def test_dummy(self):
        print("test_dummy")

        if ( True == self.haveGUI ):
            self.gme.render(1)

        self.assertTrue( True )
    
    def test_can_move_to_east(self):
        print("test_can_move_to_east")

        # East direction.
        dx = 1.0
        dy = 0.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )
    
    def test_can_move_to_northeast(self):
        print("test_can_move_to_northeast")

        # Northeast direction.
        dx = 1.0
        dy = 1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_north(self):
        print("test_can_move_to_north")

        # Nort direction.
        dx = 0.0
        dy = 1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_northwest(self):
        print("test_can_move_to_northwest")

        # Northwest direction.
        dx = -1.0
        dy =  1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        # import ipdb; ipdb.set_trace()

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_west(self):
        print("test_can_move_to_west")

        # West direction.
        dx = -1.0
        dy =  0.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_southwest(self):
        print("test_can_move_to_southwest")

        # Southwest direction.
        dx = -1.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_south(self):
        print("test_can_move_to_south")

        # South direction.
        dx =  0.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_southeast(self):
        print("test_can_move_to_southeast")

        # Southeast direction.
        dx =  1.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_try_move(self):
        """Test try_move()."""

        print("test_try_move")

        sizeW = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        sizeH = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # From staring point move half a block.
        coor = GridMap.BlockCoor( \
            self.gme.map.corners[0][GridMap.GridMap2D.I_X] + 0.5 * sizeW, \
            self.gme.map.corners[0][GridMap.GridMap2D.I_Y] + 0.5 * sizeH )
        
        coorDelta = GridMap.BlockCoorDelta( sizeW, sizeH )

        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -1 )
        self.assertEqual( flagTerm, False )

        # Move into ending block.
        coor.x = self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 1.5 * sizeW
        coor.y = self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 1.5 * sizeH
        
        coorDelta.dx = sizeW
        coorDelta.dy = sizeH

        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, 100 )
        self.assertEqual( flagTerm, True )

        # From staring point move half a block south.
        coor.x = self.gme.map.corners[0][GridMap.GridMap2D.I_X] + 0.5 * sizeW
        coor.y = self.gme.map.corners[0][GridMap.GridMap2D.I_Y] + 0.5 * sizeH
        
        coorDelta.dx = 0
        coorDelta.dy = -sizeH

        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, 0 )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

        # From staring point move half a block west.
        coor.x = self.gme.map.corners[0][GridMap.GridMap2D.I_X] + 0.5 * sizeW
        coor.y = self.gme.map.corners[0][GridMap.GridMap2D.I_Y] + 0.5 * sizeH
        
        coorDelta.dx = -sizeW
        coorDelta.dy = 0

        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        self.assertEqual( coorNew.x, 0 )
        self.assertEqual( coorNew.y, coor.y )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

    def test_try_move_long_distance_with_no_obstacles(self):
        print("test_try_move_long_distance_with_no_obstacles")

        sizeW = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        sizeH = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # Above the starting block.
        coor = GridMap.BlockCoor( 0.5*sizeW, 1.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            self.gme.map.corners[1][GridMap.GridMap2D.I_X] - self.gme.map.corners[0][GridMap.GridMap2D.I_X] - sizeW, \
            0.5 * sizeH )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -1 )
        self.assertEqual( flagTerm, False )

        # To the riight of the starting block.
        coor = GridMap.BlockCoor( 1.5*sizeW, 0.5*sizeH )

        # New delta.
        coorDelta.dx = 0.5 * sizeW
        coorDelta.dy = self.gme.map.corners[3][GridMap.GridMap2D.I_Y] - self.gme.map.corners[0][GridMap.GridMap2D.I_Y] - sizeH

        # Tyr to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -1 )
        self.assertEqual( flagTerm, False )

        # === Going backwards. From east to west, from north to south. ===

        # Below the ending block.
        coor = GridMap.BlockCoor( \
            self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5*sizeW, \
            self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 1.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            -(self.gme.map.corners[1][GridMap.GridMap2D.I_X] - self.gme.map.corners[0][GridMap.GridMap2D.I_X] - sizeW), \
            0.5 * sizeH )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -1 )
        self.assertEqual( flagTerm, False )

        # To the west of the ending block.
        coor = GridMap.BlockCoor( \
            self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 1.5*sizeW, \
            self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            0.5 * sizeW, \
            -(self.gme.map.corners[3][GridMap.GridMap2D.I_Y] - self.gme.map.corners[0][GridMap.GridMap2D.I_Y] - sizeH) )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -1 )
        self.assertEqual( flagTerm, False )

    def test_try_move_long_distance_out_of_boundary(self):
        print("test_try_move_long_distance_out_of_boundary")

        sizeW = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        sizeH = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # Above the starting block.
        coor = GridMap.BlockCoor( 0.5*sizeW, 1.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            self.gme.map.corners[1][GridMap.GridMap2D.I_X] - self.gme.map.corners[0][GridMap.GridMap2D.I_X] - 0.5*sizeW, \
            0.5 * sizeH )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

        # To the right of the starting block.
        coor = GridMap.BlockCoor( 1.5*sizeW, 0.5*sizeH )

        # New delta.
        coorDelta.dx = 0.5 * sizeW
        coorDelta.dy = self.gme.map.corners[3][GridMap.GridMap2D.I_Y] - self.gme.map.corners[0][GridMap.GridMap2D.I_Y] - 0.5*sizeH

        # Tyr to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

        # === Going backwards. From esat to west, from north to south. ===

        # Below the ending block.
        coor = GridMap.BlockCoor( \
            self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5*sizeW, \
            self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 1.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            -(self.gme.map.corners[1][GridMap.GridMap2D.I_X] - self.gme.map.corners[0][GridMap.GridMap2D.I_X] - 0.5*sizeW), \
            0.5 * sizeH )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

        # To the west of the ending block.
        coor = GridMap.BlockCoor( \
            self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 1.5*sizeW, \
            self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5*sizeH )

        # Delta of movements.
        coorDelta = GridMap.BlockCoorDelta( \
            0.5 * sizeW, \
            -(self.gme.map.corners[3][GridMap.GridMap2D.I_Y] - self.gme.map.corners[0][GridMap.GridMap2D.I_Y] - 0.5*sizeH) )
        
        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, coor.x + coorDelta.dx )
        self.assertEqual( coorNew.y, coor.y + coorDelta.dy )
        self.assertEqual( val, -200 )
        self.assertEqual( flagTerm, False )

    def test_move_to_obstacle(self):
        print("test_move_to_obstacle")

        # ==============================================================
        # Starting at (7.0, 3.0), aimming at (11.0, 5.0), 
        # should be stopped by the vertical line of obstacle at (10.0, 4.5).
        # ==============================================================

        coor = GridMap.BlockCoor( 7.0, 3.0 )
        coorDelta = GridMap.BlockCoorDelta( 4.0, 2.0)

        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -100 )
        self.assertEqual( flagTerm, False )

        # ==============================================================
        # Starting at (8.0, 2.0), aimming at (10.0, 6.0), 
        # should be stopped by the horizontal line of obstacle at (9.5, 5.0).
        # ==============================================================

        coor = GridMap.BlockCoor( 8.0, 2.0 )
        coorDelta = GridMap.BlockCoorDelta( 2.0, 4.0)

        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, 9.5 )
        self.assertEqual( coorNew.y, 5.0 )
        self.assertEqual( val, -100 )
        self.assertEqual( flagTerm, False )

        # ==============================================================
        # Starting at (8.0, 2.0), aimming at (11.0, 5.0), 
        # should be stopped by the southwest corner of obstacle at (10.0, 4.0).
        # ==============================================================

        coor = GridMap.BlockCoor( 8.0, 2.0 )
        coorDelta = GridMap.BlockCoorDelta( 3.0, 3.0)

        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertEqual( flagTerm, False )

        # ==============================================================
        # Starting at (8.0, 3.0), aimming at (10.0, 5.0), 
        # should be stopped by the southwest corner of obstacle at (10.0, 5.0).
        # This corner is an intersection of three obstacle blocks.
        # The aimming point is exactly the intersection point.
        # ==============================================================

        coor = GridMap.BlockCoor( 8.0, 3.0 )
        coorDelta = GridMap.BlockCoorDelta( 2.0, 2.0)

        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -300 )
        self.assertEqual( flagTerm, False )

        # ==============================================================
        # Starting at (7.0, 7.0), aimming at (10.0, 4.0), 
        # should be stopped by the southwest corner of obstacle at (9.0, 5.0).
        # The stopping point is exactly on the path way.
        # ==============================================================

        coor = GridMap.BlockCoor( 7.0, 7.0 )
        coorDelta = GridMap.BlockCoorDelta( 3.0, -3.0)

        # Try to move.
        coorNew, val, flagTerm = self.gme.try_move( coor, coorDelta )

        # Assertions.
        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertEqual( flagTerm, False )

    def test_move_to_obstacle_in_horizontal_and_vertical_directions(self):
        print("test_move_to_obstacle_in_horizontal_and_vertical_directions")

        # Precisely from west to east, stopped by vertical line.
        coor  = GridMap.BlockCoor( 8.5, 4.5 )
        delta = GridMap.BlockCoorDelta( 2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from west to east, stopped by vertical line of the boundary.
        coor  = GridMap.BlockCoor( 18.5, 4.5 )
        delta = GridMap.BlockCoorDelta( 2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 20.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Precisely from west to east, stopped by corner.
        coor  = GridMap.BlockCoor( 8.5, 4.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from west to east, stopped by corner.
        # Obstacle is below the horizontal line.
        coor  = GridMap.BlockCoor( 8.5, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  7.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === From east to west. ===

        # Precisely from east to west, stopped by vertical line.
        coor  = GridMap.BlockCoor( 12.5, 6.5 )
        delta = GridMap.BlockCoorDelta( -2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from east to west, stopped by vertical line of the boundary.
        coor  = GridMap.BlockCoor( 1.5, 6.5 )
        delta = GridMap.BlockCoorDelta( -2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  0.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Precisely from east to west, stopped by corner.
        # The obstacle is under the horizontal line.
        coor  = GridMap.BlockCoor( 12.5, 7.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  7.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from east to west, stopped by corner.
        coor  = GridMap.BlockCoor( 12.5, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 0.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === From south to north. ===

        # Precisely from south to north, stopped by horizontal line.
        coor  = GridMap.BlockCoor( 9.5, 3.5 )
        delta = GridMap.BlockCoorDelta( 0.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from south to north, stopped by horizontal line of the boundary.
        coor  = GridMap.BlockCoor( 11.5, 8.5 )
        delta = GridMap.BlockCoorDelta( 0.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.5 )
        self.assertEqual( coorNew.y, 10.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Precisely from south to north, stopped by corner.
        coor  = GridMap.BlockCoor( 9.0, 3.5 )
        delta = GridMap.BlockCoorDelta( 0.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from south to north, stopped by corner.
        # The obstacle is to the west of the vertical line.
        coor  = GridMap.BlockCoor( 12.0, 3.5 )
        delta = GridMap.BlockCoorDelta( 0.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 12.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === From north to south. ===

        # Precisely from north to south, stopped by horizontal line.
        coor  = GridMap.BlockCoor( 9.5, 7.5 )
        delta = GridMap.BlockCoorDelta( 0.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from north to south, stopped by horizontal line of the boundary.
        coor  = GridMap.BlockCoor( 9.5, 1.5 )
        delta = GridMap.BlockCoorDelta( 0.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  0.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Precisely from south to north, stopped by corner.
        coor  = GridMap.BlockCoor( 9.0, 7.5 )
        delta = GridMap.BlockCoorDelta( 0.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Precisely from south to north, stopped by corner.
        # The obstacle is to the west of the vertical line.
        coor  = GridMap.BlockCoor( 12.0, 7.5 )
        delta = GridMap.BlockCoorDelta( 0.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 12.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

    def test_move_to_obstacle_in_northeast_direction(self):
        print("test_move_to_obstacle_in_northeast_direction")

        # Stopped by corner, obstacle is in northwest.
        coor  = GridMap.BlockCoor( 10.0, 3.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northeast.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 9.0, 3.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by vertical line, obstacle is in east.
        coor  = GridMap.BlockCoor( 9.0, 4.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northeast.
        # Three obstacles.
        coor  = GridMap.BlockCoor( 9.0, 4.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by horizontal line, obstacle is in north.
        coor  = GridMap.BlockCoor( 9.0, 4.0 )
        delta = GridMap.BlockCoorDelta( 1.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southeast.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 8.0, 5.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === Boundary involved. ===

        # Stopped by vertical line of boundary.
        # Boundary is in east.
        coor  = GridMap.BlockCoor( 19.0, 4.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 20.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Stopped by a corner shared by an obstacle and the boundary.
        # The obstacle in in north. 
        # The Boundary is in east.
        coor  = GridMap.BlockCoor( 19.0, 4.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 20.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by horizontal line of boundary.
        # Boundary is in north
        coor  = GridMap.BlockCoor( 9.0, 9.0 )
        delta = GridMap.BlockCoorDelta( 1.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y, 10.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Stopped by a corner shared by an obstacle and the boundary.
        # The obstacle in in east. 
        # The Boundary is in north.
        coor  = GridMap.BlockCoor( 9.0, 9.0 )
        delta = GridMap.BlockCoorDelta( 2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y, 10.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

    def test_move_to_obstacle_in_northwest_direction(self):
        print("test_move_to_obstacle_in_northwest_direction")

        # Stopped by corner, obstacle is in southwest.
        coor  = GridMap.BlockCoor( 13.0, 5.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 12.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northwest.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 13.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 12.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by horizontal line, obstacle is in north.
        coor  = GridMap.BlockCoor( 12.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -1.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.5 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northwest.
        # Three obstacles.
        coor  = GridMap.BlockCoor( 12.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by vertical line, obstacle is in west.
        coor  = GridMap.BlockCoor( 12.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northeast.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 11.0, 3.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  4.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === Boundary involved. ===

        # Stopped by horizontal line of the boundary
        # The boundary is in north.
        coor  = GridMap.BlockCoor( 12.0, 9.0 )
        delta = GridMap.BlockCoorDelta( -1.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.5 )
        self.assertEqual( coorNew.y, 10.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Stopped by corner shared by an obstacle and the boundary.
        # The obstacle is in southwest.
        # The boundary is in north.
        coor  = GridMap.BlockCoor( 12.0, 9.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y, 10.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by corner shared by an obstacle and the boundary.
        # The obstacle is in northeast.
        # The boundary is in west.
        coor  = GridMap.BlockCoor( 1.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  0.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by vertical line of the boundary
        # The boundary is in west.
        coor  = GridMap.BlockCoor( 1.0, 4.0 )
        delta = GridMap.BlockCoorDelta( -2.0, 1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  0.0 )
        self.assertEqual( coorNew.y,  4.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

    def test_move_to_obstacle_in_southwest_direction(self):
        print("test_move_to_obstacle_in_southwest_direction")

        # Stopped by corner, obstacle is in southeast.
        coor  = GridMap.BlockCoor( 11.0, 8.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  7.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southwest.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 12.0, 8.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  7.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by vertical line, obstacle is in west.
        coor  = GridMap.BlockCoor( 12.0, 7.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southwest.
        # Three obstacles.
        coor  = GridMap.BlockCoor( 12.0, 7.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by horizontal line, obstacle is in south.
        coor  = GridMap.BlockCoor( 12.0, 7.0 )
        delta = GridMap.BlockCoorDelta( -1.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.5 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in northwest.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 13.0, 6.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 12.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === Boundary involved. ===

        # Stopped by vertical line of boundary
        # The boundary is in west.
        coor  = GridMap.BlockCoor( 1.0, 7.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  0.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Stopped by shared corner of an obstacle and the boundary.
        # The obstacle is in southeast.
        # The boundary is in west.
        coor  = GridMap.BlockCoor( 1.0, 7.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  0.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by shared corner of an obstacle and the boundary.
        # The obstacle is in northwest.
        # The boundary is in south.
        coor  = GridMap.BlockCoor( 12.0, 1.0 )
        delta = GridMap.BlockCoorDelta( -2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  0.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by Horizontal line of boundary
        # The boundary is in south.
        coor  = GridMap.BlockCoor( 12.0, 1.0 )
        delta = GridMap.BlockCoorDelta( -1.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.5 )
        self.assertEqual( coorNew.y,  0.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

    def test_move_to_obstacle_in_southeast_direction(self):
        print("test_move_to_obstacle_in_southeast_direction")

        # Stopped by corner, obstacle is in northeast.
        coor  = GridMap.BlockCoor( 8.0, 6.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  5.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southeast.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 8.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by horizontal line, obstacle is in south.
        coor  = GridMap.BlockCoor( 9.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 1.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southeast.
        # Three obstacles.
        coor  = GridMap.BlockCoor( 9.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by vertical line, obstacle is in east.
        coor  = GridMap.BlockCoor( 9.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # Stopped by corner, obstacle is in southwest.
        # Only one obstacle.
        coor  = GridMap.BlockCoor( 10.0, 8.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 11.0 )
        self.assertEqual( coorNew.y,  7.0 )
        self.assertEqual( val, -100 )
        self.assertFalse( ft )

        # === Boundary involved. ===

        # Stopped by horizontal line of the boundary.
        # The boundary is in south.
        coor  = GridMap.BlockCoor( 9.0, 1.0 )
        delta = GridMap.BlockCoorDelta( 1.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x,  9.5 )
        self.assertEqual( coorNew.y,  0.0 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

        # Stopped by a corner shared by an obstacle and the boundary.
        # The obstacle is in northeast.
        # The boundary is in south.
        coor  = GridMap.BlockCoor( 9.0, 1.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 10.0 )
        self.assertEqual( coorNew.y,  0.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by a corner shared by an obstacle and the boundary.
        # The obstacle is in southwest.
        # The boundary is in east.
        coor  = GridMap.BlockCoor( 19.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -2.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 20.0 )
        self.assertEqual( coorNew.y,  6.0 )
        self.assertEqual( val, -300 )
        self.assertFalse( ft )

        # Stopped by vertical line of the boundary.
        # The boundary is in east.
        coor  = GridMap.BlockCoor( 19.0, 7.0 )
        delta = GridMap.BlockCoorDelta( 2.0, -1.0 )
        coorNew, val, ft = self.gme.try_move( coor, delta )

        self.assertEqual( coorNew.x, 20.0 )
        self.assertEqual( coorNew.y,  6.5 )
        self.assertEqual( val, -200 )
        self.assertFalse( ft )

    def test_step_from_start_to_end(self, flagSilence = False, flagRender = True):
        if ( False == flagSilence ):
            print("test_step_from_start_to_end")

        stepSizeX = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepSizeY = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # Reset the environment.
        self.gme.reset()

        totalVal = 0

        # Move north with 1 step.
        action = GridMap.BlockCoorDelta( 0, stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 8 steps.
        action = GridMap.BlockCoorDelta( 18 * stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 8 steps.
        action = GridMap.BlockCoorDelta( 0, 8 * stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 1 step. In the ending block.
        action = GridMap.BlockCoorDelta( stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertTrue( flagTerm )
        totalVal += val

        self.assertEqual( coor.x, self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5 * stepSizeX )
        self.assertEqual( coor.y, self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5 * stepSizeY )
        self.assertEqual( totalVal, 97 )

        if ( True == flagRender ):
            if ( True == self.haveGUI ):
                self.gme.render(3, flagSave=True)

    def test_step_from_start_to_end_02(self):
        print("test_step_from_start_to_end_02")

        stepSizeX = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepSizeY = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # Reset the environment.
        self.gme.reset()

        totalVal = 0

        # Move east with 1 step.
        action = GridMap.BlockCoorDelta( stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 8 steps.
        action = GridMap.BlockCoorDelta( 0, 8 * stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 18 steps.
        action = GridMap.BlockCoorDelta( 18 * stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 1 step. In the ending block.
        action = GridMap.BlockCoorDelta( 0, stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertTrue( flagTerm )
        totalVal += val

        self.assertEqual( coor.x, self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5 * stepSizeX )
        self.assertEqual( coor.y, self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5 * stepSizeY )
        self.assertEqual( totalVal, 97 )

        if ( True == self.haveGUI ):
            self.gme.render(3, flagSave=True, fn="test_step_from_start_to_end_02")

    def test_step_from_start_to_end_radius(self, flagSilence = False, flagRender = True):
        if ( False == flagSilence ):
            print("test_step_from_start_to_end_radius")

        stepSizeX = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepSizeY = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        radius = math.sqrt( stepSizeX**2 + stepSizeY**2 ) / 2
        if ( False == flagSilence ):
            print( "radius = %f." % ( radius ) )

        # Reset the environment.
        self.gme.enable_ending_point_radius(radius)
        self.gme.reset()

        totalVal = 0

        # Move north with 1 step.
        action = GridMap.BlockCoorDelta( 0, stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 8 steps.
        action = GridMap.BlockCoorDelta( 18 * stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 8 steps.
        action = GridMap.BlockCoorDelta( 0, 8 * stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 1 step. In the ending block.
        action = GridMap.BlockCoorDelta( stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertTrue( flagTerm )
        totalVal += val

        self.assertEqual( coor.x, self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5 * stepSizeX )
        self.assertEqual( coor.y, self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5 * stepSizeY )
        self.assertEqual( totalVal, 97 )

        if ( True == flagRender ):
            if ( True == self.haveGUI ):
                self.gme.render(3, flagSave=True)

        # Disable ending point radius mdoe.
        self.gme.disable_ending_point_radius()

    def test_step_from_start_to_end_radius_02(self):
        print("test_step_from_start_to_end_radius_02")

        stepSizeX = self.gme.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepSizeY = self.gme.map.get_step_size()[GridMap.GridMap2D.I_Y]

        radius = math.sqrt( stepSizeX**2 + stepSizeY**2 ) / 2
        print( "radius = %f." % ( radius ) )

        # Reset the environment.
        self.gme.enable_ending_point_radius(radius)
        self.gme.reset()

        totalVal = 0

        # Move east with 1 step.
        action = GridMap.BlockCoorDelta( stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 8 steps.
        action = GridMap.BlockCoorDelta( 0, 8 * stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 18 steps.
        action = GridMap.BlockCoorDelta( 18 * stepSizeX, 0 )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 1 step. In the ending block.
        action = GridMap.BlockCoorDelta( 0, stepSizeY )
        coor, val, flagTerm, _ = self.gme.step( action )
        self.assertTrue( flagTerm )
        totalVal += val

        self.assertEqual( coor.x, self.gme.map.corners[2][GridMap.GridMap2D.I_X] - 0.5 * stepSizeX )
        self.assertEqual( coor.y, self.gme.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5 * stepSizeY )
        self.assertEqual( totalVal, 97 )

        if ( True == self.haveGUI ):
            self.gme.render(3, flagSave=True, fn="test_step_from_start_to_end_02")

        # Disable ending point radius mode.
        self.gme.disable_ending_point_radius()

    def test_save_load(self):
        print("test_save_load")

        # Explicitly invoke a test function.
        self.test_step_from_start_to_end(True, False)

        # Save the environment.
        self.gme.save()

        # Create a temporary environment.
        tempGme = GridMap.GridMapEnv()
        tempGme.load( self.workingDir )

        # Show the temporary environment.
        print(tempGme)

class TestGridMapEnv_RLTrain(unittest.TestCase):
    def setUp(self):
        self.rows = 11
        self.cols = 11
        gridMap = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)

        gridMap.set_value_normal_block(-1)
        gridMap.set_value_starting_block(0)
        gridMap.set_value_ending_block(100)
        gridMap.set_value_obstacle_block(-100)

        gridMap.initialize()
        # Overwrite blocks.
        gridMap.set_starting_block((0, 0))
        gridMap.set_ending_block((10, 10))
        gridMap.add_obstacle(( 2,  8))
        gridMap.add_obstacle(( 2,  7))
        gridMap.add_obstacle(( 2,  6))
        gridMap.add_obstacle(( 2,  5))
        gridMap.add_obstacle(( 3,  5))
        gridMap.add_obstacle(( 4,  5))
        gridMap.add_obstacle(( 5,  5))
        gridMap.add_obstacle(( 6,  5))
        gridMap.add_obstacle(( 7,  5))
        gridMap.add_obstacle(( 8,  5))
        gridMap.add_obstacle(( 8,  4))
        gridMap.add_obstacle(( 8,  3))
        gridMap.add_obstacle(( 8,  2))

        self.workingDir = "./WD_TestGridMapEnv_RLTrain"

        self.gme = GridMap.GridMapEnv( gridMap = gridMap, workingDir = self.workingDir )
        self.gme.reset()

    def test_special_movement_01(self):
        print("test_special_movement_01")

        # Failed case from RL training.
        # Coor = ( 4.33993915488, 1.57951883618 )
        # CoorDelta = ( 0.277159383515, -1.70042657517 )
        # Expected: Stop at the boundary.

        coor = GridMap.BlockCoor( 4.33993915488, 1.57951883618 )
        action = GridMap.BlockCoorDelta( 0.277159383515, -1.70042657517 )

        # Overwite the internal state.
        self.gme.agentCurrentLoc = copy.deepcopy( coor )

        # Step.
        # import ipdb; ipdb.set_trace()
        coorNew, val, flagTerm, _ = self.gme.step( action )

        print(coorNew)

    def test_special_movement_02(self):
        print("test_special_movement_02")

        # Failed case from RL training.
        # coor(0.5, 0.5)
        # CoorDelta(1.42219106864, 0.700193069679)
        # Issue: Never stop.

        coor = GridMap.BlockCoor( 0.5, 0.5 )
        action = GridMap.BlockCoorDelta( 1.42219106864, 0.700193069679 )

        # Overwite the internal state.
        self.gme.agentCurrentLoc = copy.deepcopy( coor )

        # Step.
        # import ipdb; ipdb.set_trace()
        coorNew, val, flagTerm, _ = self.gme.step( action )

        print(coorNew)

    def test_special_movement_03(self):
        print("test_special_movement_03")

        # Failed case from RL training.
        # coor(9.11443961519, 7.76228759008)
        # CoorDelta(2.02919137172, -0.276896302745)
        # Issue: Never stop.

        coor = GridMap.BlockCoor( 9.11443961519, 7.76228759008 )
        action = GridMap.BlockCoorDelta( 2.02919137172, -0.276896302745 )

        # Overwite the internal state.
        self.gme.agentCurrentLoc = copy.deepcopy( coor )

        # Step.
        # import ipdb; ipdb.set_trace()
        coorNew, val, flagTerm, _ = self.gme.step( action )

        print(coorNew)

    def test_special_movement_04(self):
        print("test_special_movement_04")

        # Failed case from RL training.
        # coor(11.0, 10.9998531342)
        # CoorDelta(-0.000502182123979, 0.736209217276)
        # Issue: Evaluation out of boundary point exception in try_move().

        coor = GridMap.BlockCoor( 11.0, 10.9998531342 )
        action = GridMap.BlockCoorDelta( -0.000502182123979, 0.736209217276 )

        # Overwite the internal state.
        self.gme.agentCurrentLoc = copy.deepcopy( coor )

        # Step.
        # import ipdb; ipdb.set_trace()
        coorNew, val, flagTerm, _ = self.gme.step( action )

        print(coorNew)

class TestGridMapEnv_README(unittest.TestCase):
    def setUp(self):
        self.workingDir = "./WD_TestGridMapEnv_README"

        self.gme = GridMap.GridMapEnv( gridMap=None, workingDir=self.workingDir )
        self.gme.load( self.workingDir, "GMEnv.json" )
        self.gme.reset()

    def test_render(self):
        print("test_render.")

        self.gme.render(flagSave=True)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestGridMap2D )
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase( TestGridMap2D_WithPotential ) )
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase( TestGridMapEnv ) )
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase( TestGridMapEnv_RLTrain ) )
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase( TestGridMapEnv_README ) )
    unittest.TextTestRunner().run( suite )
