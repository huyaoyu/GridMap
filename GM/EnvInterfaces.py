
from __future__ import print_function

import math
import numpy as np

import GridMap

def get_two_random_indices(r, c):
    """Return a 2x2 NumPy array, containing two different index pair."""

    res = np.zeros((2, 2), dtype=np.int)

    while ( res[ 0, 0 ] == res[ 1, 0 ] and \
            res[ 0, 1 ] == res[ 1, 1 ] ):
        res[0, 0] = np.random.randint( 0, r )
        res[0, 1] = np.random.randint( 0, c )
        res[1, 0] = np.random.randint( 0, r )
        res[1, 1] = np.random.randint( 0, c )

    return res

class GME_NP(GridMap.GridMapEnv):
    def __init__(self, name="GridMapEnv with NumPy", gridMap = None, workingDir="./"):
        super(GME_NP, self).__init__( name, gridMap, workingDir )

        # # Create map.
        # self.map = GridMap.GridMap2D( 10, 20 )

        self.maxStuckCount      = 0
        self.stuckPenaltyFactor = -10
        self.stuckCount         = 0
        self.stuckState         = None

        # Member variables for compatibility.
        self.observation_space = np.array([0, 0]) # self.observation_spac.shape should be a tuple showing the shape of the state variable.

    def enable_stuck_check(self, maxStuckCount, penaltyFactor ):
        if ( maxStuckCount < 0 ):
            raise GridMap.GridMapException("Max stuck count must be non-negative number.")

        self.maxStuckCount      = maxStuckCount
        self.stuckPenaltyFactor = penaltyFactor
    
    def disable_stuck_check(self):
        self.maxStuckCount      = 0
        self.stuckPenaltyFactor = 1.0

    def step(self, action):
        """
        Override super class.
        """

        act = GridMap.BlockCoorDelta( action[0], action[1] )

        coor, val, flagTerm, dummy = super(GME_NP, self).step( act )

        state = np.array( [coor.x, coor.y], dtype=np.float32 )

        # Check stuck states.
        if ( 0 != self.maxStuckCount ):
            if ( self.stuckState is None ):
                self.stuckState = state
            else:
                if ( state[0] == self.stuckState[0] and \
                    state[1] == self.stuckState[1] ):
                    self.stuckCount += 1
                else:
                    self.stuckCount = 0
                    self.stuckState = None
                
                if ( self.maxStuckCount == self.stuckCount ):
                    val = self.stuckPenaltyFactor * math.fabs( val )
                    flagTerm = True

        return state, val, flagTerm, dummy

    def reset(self):
        res = super(GME_NP, self).reset()

        # Clear the stuck states.
        self.stuckCount = 0
        self.stuckState = None

        return np.array([ res.x, res.y ])

    def set_trajectory(self, t):
        """
        t is a numpy ndarray of shape (x, 2). t stores the position (state) history of the agent.
        This function substitutes the self.agentLocs member variable with t. Converts numpy ndarray 
        into BlockCoor objects.
        """

        n = t.shape[0]

        temp = []

        for i in range(n):
            temp.append( self.make_a_coor( t[i, 0], t[i, 1] ) )

        self.agentLocs = temp
        self.nSteps    = n

    def random_map(self):
        # There must be a map.
        if ( self.map is None ):
            raise GridMap.GridMapException("Map must not be None for randomizing.")

        # Get the randomized indices of the staring and ending blocks.
        indices = get_two_random_indices( self.map.rows, self.map.cols )

        # Reset the staring block.
        self.map.set_starting_block( GridMap.BlockIndex( indices[0,0], indices[0,1] ) )
        
        # Reset the ending block.
        self.map.set_ending_block( GridMap.BlockIndex( indices[1,0], indices[1,1] ) )

    