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

Once we have a GridMap2D object as a map, to create an environment, it could be as simple as referring to this map. When creating a `GridMapEnv` object, the user could set the name of the environment and set the working directory at the same time.

In our reinforcement learning study, it is required that the interactions between the environment and the reinforcement learning algorithm are carried out thought NumPy objects. To do this, we provide an interfacing class, `GME_NP` defined in `EnvInterfaces.py` file. There are no major differences between the creation of a `GridMapEnv` ojbect and a `GME_NP` object.

## Saving and loading environments

The user could use the member functions `save()` and `load()` to write or read back an environment and its associated map to of from the file system. When using `save()` the writing destination will be the location defined by the working directory. However, for `load()`, the user has to specify the filename of the environment as well as the directory where the file resides. 

Similar to GridMap2D objects, an environment is saved as a JSON file. The user is wellcome to take a look at it and see various settings `GridMapEnv` provides.

## Interact with the environment

Interactions with an `GridMapEnv` object or a `GME_NP` object are happen mainly through the following interface functions.

- `reset()`: Resets the environment, places the agent back to the starting block defined by the map. Clean the state-action history and the accumulated rewards from the environment. The initial state will be returned.

- `step()`: Make a single interaction, moving in a specific direction with a certain length of 'step', we define this as an 'action'. By default, the length of an action is not limited, however, the resultant of the action will be determined by the boundaries and the obstacles of the map. The rules of actions are listed later in this section. `step()` returns four objects, namely the new state, the value/reward, the termination flag, and a fourth object that is for compatibility with other system and not used currently. The user should check the termination flat every time he/she called `step()`. Calling `step()` with the environment being in the termination state will cause an exception to be raised. To restart, use `reset()`.

- `render()`: Drawn the map with all the state-action pairs happend up to the current time. This function is currently a naive implementation a has protentially poor performance in terms of graphics. Call this function at the beginning of the training to observe the map and call this function at the end of the training to see the state-action history. The user is encouraged to call `finialize()` if a call to `render()` is made before using `reset()` to start a new interaction session.

There are other interface functions that a user could use to interact with the environment or configure different settings.

### Basic interaction

As mentioned earlier, interactions are mainly taken out by using `reset()` to initialize, several `step()` to make actions and collect reward, some calls to `render()` to visually see the map and the interaction history.

By issuing `step()`, the user is moving the agent around in the map. `reset()` always place the agent at the center of the starting block. Each time the user calls `setp()`, an action defined as `BlockCoorDelta` should be supplied. The environment determines the resultant state, the 2D coordinate, of the agent based on the current state and the action the user chooses to take. The following rules are applied:

The agent tries to move in the direction defined by the action,
- If the agent goes out of any boundaries of the map before it reaches the destination, it stops at the boundary along its way. The agent receives a reward/penalty from the environment (configured as a property of the map, the value for being outof boundary).

- If the agent is at a boundary and the action makes it try to go further into the outer region of the map, the agent would not move at all and will receive a reward/penalty from the environment as being out of the boundary.

- If the agent chooses to stay at a boundary, it receives the same reward/penalty as being out of boundary.

- If the agent goes across an obstacle as directed by the action, it stops at the grid lines of the obstacle along its way. The agenet receives a reward/penalty from the environment defined by the obstacle block the agent is hitting on.

- If the agent is at a grid line of an obstacle and it tries to go across the obstacle, it will not move at all and will receive a reward/penalty from the envrionment as being hitting an obstacle.

- If the agent stays at the grid line of an obstacle, it is the same as hitting the obstacle.

- If the agent moves to the destination (not an ending block) defined by the action and does not go out of boundary or go into any obstacles, the environment gives it a reward/panelty defined by this `NormalBlcok`.

- If the agent makes to the ending block before going out of boundary or hitting any obstacles, the agent receives a reward and the current session terminates. A termination flag is set. Any further call to `step()` result in rasing an exception. Use `render()` to see the result and `reset()` to start over.

Since we are in a continuous space, there are some special cases:

- If the agent tries to move along a boundary, this is treated as going out of boundary. The agent will not move at all and will receive a reward/penalty from the environment.

- If the agent tries to move along a grid line of an obstacle, this is treated as hitting the obstacle. The agent will not move at all and will recieve a reward/penalty from the environment.

- If the agent go across the ending block, it is not considered as a termination. No reward will be given regarding the crossing over the ending block.

- If the agent stops right at the grid line of the ending block, it is not considered as reach the ending block.

- If the agent goes across the ending block and goes out of the boundary neighboring the ending block. The agent will stop at the boundary. This is not considered as being inside the ending block. It is considered as being out of boundary and the agent receives the reward/penalty of being out of boundary.

- If the agent goes across the ending block and hits an obstacle neighboring the ending block. The agent will stop at the grid line of the obstacle. This is not considered as being inside the ending block. It is considered as being hitting the obstacle and the agent receives the reward/penalty of hitting that obstacle.

- If the agent lands at the intersection point of two or three obstacles, it will receive rewards/penalties from all the obstacles.

- If the angnt lands at the intersection point of a boundary and an obstacle, it will receive both rewards/penalties for being out of boundary and hitting an obstacle at the same time.

### Settings

## Replay a state-action history
