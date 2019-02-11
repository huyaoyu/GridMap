from __future__ import print_function

import numpy as np
import unittest

import EnvInterfaces
import GridMap

class TestGME_NP(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20

        gridMap = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)
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

        self.workingDir = "./WD_TestGME_NP"

        self.gmenp = EnvInterfaces.GME_NP( workingDir = self.workingDir )
        self.gmenp.map = gridMap
        self.gmenp.reset()

    def test_step(self):
        print("test_step")

        stepSizeX = self.gmenp.map.get_step_size()[GridMap.GridMap2D.I_X]
        stepSizeY = self.gmenp.map.get_step_size()[GridMap.GridMap2D.I_Y]

        # Reset the environment.
        self.gmenp.reset()

        totalVal = 0

        # Move north with 1 step.
        action = np.array( [0, stepSizeY] )
        coor, val, flagTerm, _ = self.gmenp.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 8 steps.
        action = np.array( [18 * stepSizeX, 0] )
        coor, val, flagTerm, _ = self.gmenp.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move north with 8 steps.
        action = np.array( [0, 8 * stepSizeY] )
        coor, val, flagTerm, _ = self.gmenp.step( action )
        self.assertFalse( flagTerm )
        totalVal += val

        # Move east with 1 step. In the ending block.
        action = np.array( [stepSizeX, 0] )
        coor, val, flagTerm, _ = self.gmenp.step( action )
        self.assertTrue( flagTerm )
        totalVal += val

        self.assertEqual( coor[0], self.gmenp.map.corners[2][GridMap.GridMap2D.I_X] - 0.5 * stepSizeX )
        self.assertEqual( coor[1], self.gmenp.map.corners[2][GridMap.GridMap2D.I_Y] - 0.5 * stepSizeY )
        self.assertEqual( totalVal, 103 )

        self.gmenp.render(3, flagSave=True)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestGME_NP )
    unittest.TextTestRunner().run( suite )
