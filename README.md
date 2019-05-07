# GridMap: A simple 2D continuous maze environment for reinforcement learning training

## Introduction

GridMap is a simple 2D environment in which the user could build a maze for training reinforcement learning models. Although there is a 'Grid' built in the naming, GridMap is designed to work in a continuous coordinate space. 

In GridMap, a map is defined in a rectangular 2D plane with the plane boundaries as the map borders. Obstacles are specified by indexing and created as "blocks". A starting block and an ending block could be defined. There is an agent in the GridMap observing its continuous coordinate. The agent could make movement in the map without going into the obstacles and out of any boundaries. The agent starts it's journey from the starting block and its task is to find the ending block. 

The user could specify reward values for the following cases:

- Agent ends up in a normal grid.
- Agent goes out of boundary but blocked by the border.
- Agent goes into an obstacle but blocked by the obstacle.
- Agent goes back to the starting block.
- Agent goes into the ending block or arrives at a point that is in a circle pre-defined around the ending block.

GridMap use JSON files to save the environments along with the state-action pairs of the agent. The user could render the map and state-action history into a figure.

This simple 2D environment is used by the authors to prove their concepts in the research related to deep reinforcement learning.

## Install

```
python setup.py install --record files.txt
```

Currently, to uninstall, the user has to use the recorded file list stored in `files.txt` during the installation.

```
cat files.txt | xargs rm -rf
```

## Simple classes.

GridMap defines some simple basic classes to work with.

### Class BlockCoor
Represents a 2D coordinate.

### Class BlockCoorDelta
Represents a change of 2D coordinates.

### Class BlockIndex
Represents an index of a block.

### Class Block
Represents a Block in GridMap. `Block` is further inheritated to `NormalBlock`, `ObstacleBlock`, `StartingBlock`, and `EndingBlock`. A `Block` posses a value property as its 'value' for an agent ending up inside of on its border.

### Class GridMap2D
Represents the map with all kinds of blocks.

### Class GridMapEnv
Represents a GridMap environment which contains a map. GridMapEnv provides the user with the `reset()`, `step()`, and `render()` interfaces similar to those defined by the gym package.

### Class GME_NP
A helper class designed for reinforcement learning training.

## Create a map

A map with all grids as the `NormalBlock`s is created by defining an object of GridMap2D. The user has to specify the row and column numbers of the map, the grid size (`stepSize`) of the map. Optionally, a name of the map and the value of an agent being out of the boundary could be set as well.

After object creation, the `initialize()` method should be explicitly called to initialize the map.

Then the user could add obstacles by `add_obstacle()` member function and set the starting and ending block by using `set_starting_block()` and `set_ending_block()` functions.

GridMap2D provides various member functions to get access to the internal settings, like the values for different block types.

## Create an environment



## Saveing and loading environments

## Interact with the environment

### Basic interaction

### Settings

## Replay a state-action history
