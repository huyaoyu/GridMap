
from __future__ import print_function

import numpy as np

import GridMap

class GME_NP(GridMap.GridMapEnv):
    def __init__(self, name="GridMapEnv with NumPy", gridMap = None, workingDir="./"):
        super(GME_NP, self).__init__( name, gridMap, workingDir )

        # # Create map.
        # self.map = GridMap.GridMap2D( 10, 20 )

        # Member variables for compatibility.
        self.observation_space = np.array([0, 0]) # self.observation_spac.shape should be a tuple showing the shape of the state variable.

    def step(self, action):
        """
        Override super class.
        """

        act = GridMap.BlockCoorDelta( action[0], action[1] )

        coor, val, flagTerm, dummy = super(GME_NP, self).step( act )

        state = np.array( [coor.x, coor.y], dtype=np.float32 )

        return state, val, flagTerm, dummy

    def reset(self):
        res = super(GME_NP, self).reset()

        return np.array([ res.x, res.y ])
    