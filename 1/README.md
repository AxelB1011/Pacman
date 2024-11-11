In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:
```python autograder.py```

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

## Files you'll edit:
- search.py: Where all of your search algorithms will reside.
- searchAgents.py: Where all of your search-based agents will reside.

## Files you might want to look at:
- pacman.py: The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.
- game.py: The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
- util.py: Useful data structures for implementing search algorithms.

# Welcome to Pacman

After downloading the code and changing to the directory, you should be able to play a game of Pacman by typing the following at the command line:
```python pacman.py```

Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman's first step in mastering his domain.

The simplest agent in searchAgents.py is called the GoWestAgent, which always goes West (a trivial reflex agent). This agent can occasionally win:
```python pacman.py --layout testMaze --pacman GoWestAgent```

But, things get ugly for this agent when turning is required:
```python pacman.py --layout tinyMaze --pacman GoWestAgent```

If Pacman gets stuck, you can exit the game by typing CTRL-c into your terminal.

There are 8 parts in this project:

1. In searchAgents.py, you'll find a fully implemented SearchAgent, which plans out a path through Pacman's world and then executes that path step-by-step. The depth-first search (DFS) algorithm in the ```depthFirstSearch``` function in ```search.py``` implements the graph search version of DFS, which avoids expanding any already visited states. DFS quickly finds a solution for: 
```
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
```

2. The breadth-first search (BFS) algorithm in the ```breadthFirstSearch``` function in ```search.py``` again implements the graph search version that avoids expanding any already visited states. BFS quickly finds a solution for: 
```
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```

3. While BFS will find a fewest-actions path to the goal, we might want to find paths that are "best" in other senses. Consider mediumDottedMaze and mediumScaryMaze. The uniform-cost graph search algorithm in the ```uniformCostSearch``` function in ```search.py``` does just that. UCS quickly finds a solution for: 
```
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```

4. The A* search algorithms in the ```aStarSearch``` function in ```search.py``` finds the optimal solution slightly faster than uniform cost search. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The nullHeuristic heuristic function in search.py is a trivial example. We can test the A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as ```manhattanHeuristic``` in ```searchAgents.py```):
```
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

5. The real power of A* will only be apparent with a more challenging search problem. Now, it's time to formulate a new problem and design a heuristic for it.

In corner mazes, there are four dots, one in each corner. Our new search problem is to find the shortest path through the maze that touches all four corners (whether the maze actually has food there or not). Note that for some mazes like tinyCorners, the shortest path does not always go to the closest food first! The shortest path through tinyCorners takes 28 steps.

The ```CornersProblem``` search problem in ```searchAgents.py``` defines an abstract state representation that encodes all the information necessary to detect whether all four corners have been reached without encoding irrelevant information. Now, our search agent solves:
```
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

6. Now, we implement a non-trivial, consistent heuristic for the CornersProblem in cornersHeuristic.
```
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

Note: AStarCornersAgent is a shortcut for
```
-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic.
```

Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be admissible, the heuristic values must be lower bounds on the actual shortest path cost to the nearest goal (and non-negative). To be consistent, it must additionally hold that if an action has cost c, then taking that action can only cause a drop in heuristic of at most c.

Remember that admissibility isn't enough to guarantee correctness in graph search -- we need the stronger condition of consistency. However, admissible heuristics are usually also consistent, especially if they are derived from problem relaxations. Therefore it is usually easiest to start out by brainstorming admissible heuristics. Once we have an admissible heuristic that works well, we can check whether it is indeed consistent, too. The only way to guarantee consistency is with a proof. However, inconsistency can often be detected by verifying that for each node we expand, its successor nodes are equal or higher in in f-value. Moreover, if UCS and A* ever return paths of different lengths, the heuristic is inconsistent. This stuff is tricky!

The trivial heuristics are the ones that return zero everywhere (UCS) and the heuristic which computes the true completion cost. The former won't save us any time, while the latter will timeout the autograder.

7. Now we'll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we'll need a new search problem definition which formalizes the food-clearing problem: ```FoodSearchProblem``` in ```searchAgents.py```. A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman.

We fill in ```foodHeuristic``` in ```searchAgents.py``` with a consistent heuristic for the FoodSearchProblem. Try the agent on the trickySearch board:
```
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

8. Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we'd still like to find a reasonably good path, quickly. In this section, we write an agent that always greedily eats the closest dot in the ```findPathToClosestDot``` function in ```searchAgents.py```.

Our agent solves this maze (suboptimally!) in under a second with a path cost of 350:
```
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
```