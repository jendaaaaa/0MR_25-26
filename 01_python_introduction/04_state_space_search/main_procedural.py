## working script using only functions

from matplotlib import pyplot as plt
import numpy as np

## state space
GRID_SIZE = (50, 50)
START_NODE = (2, 2)
GOAL_NODE = (40, 20)

## moves
L = (1, 0)
R = (-1, 0)
U = (0, -1)
D = (0, 1)

MOVES = [R,L,D,U]
# in DFS we take the last in stack -> last is UP -> we move up

grid = np.zeros(GRID_SIZE)
noise = np.random.rand(GRID_SIZE[0], GRID_SIZE[1])
grid[noise > 0.90] = 1
grid[4:20, 20] = 1
grid[(START_NODE[0]-3):(START_NODE[0] + 4),(START_NODE[1]-3):(START_NODE[1] + 4)] = 0

def solve_dfs(grid, start, goal):
    rows, cols = grid.shape
    
    # LIST as a STACK (LIFO = append to the end and pop from the end)
    stack = [start]
    
    # SET as a list of visited -> instant checking if 'x is in set'
    visited = set()
    
    # DICTIONARY for a path reconstruction (key=child, value=parent)
    parent_map = {}
    
    print(f"Starting search from [{start}] to [{goal}]...")
    
    while stack:
        # get current node (pop from stack)
        current = stack.pop()
        
        # check if we won
        if current == goal:
            print("Goal reached!")
            return reconstruct_path(parent_map, start, goal) 
        
        visited.add(current)
        
        # explore neighbours
        for move in MOVES:
            next_node = current[0] + move[0], current[1] + move[1]
            
            # check bounds
            if 0 <= next_node[0] < cols and 0 <= next_node[1] < rows:
                # check obstacles
                if grid[next_node] != 1:
                    # check visited
                    if next_node not in visited:
                        stack.append(next_node)
                        parent_map[next_node] = current
    
    print("Failed to find a path...")
    return None

def reconstruct_path(parent_map, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent_map[current]
    path.append(start)
    path.reverse()
    return path

final_path = solve_dfs(grid, START_NODE, GOAL_NODE)

if final_path:
    iterator = 0
    for r, c in final_path:
        grid[r,c] = 0.4 + iterator/len(final_path) * 0.2
        iterator += 1
    
    grid[START_NODE] = 0.7
    grid[GOAL_NODE] = 0.3

    # we imagine the STATE SPACE as (x,y) but in numpy it is (row, column) -> (y, x)
    # we could change our mental model of the STATE SPACE or just use .transpose()
    
    # plus imshow is used for images where origin is LEFT TOP not LEFT BOTTOM
    # therefore moving DOWN is POSITIVE and UP is NEGATIVE
    
    grid_rc = grid.transpose()
    
    plt.imshow(grid_rc, cmap='hot', interpolation='nearest')
    plt.show()