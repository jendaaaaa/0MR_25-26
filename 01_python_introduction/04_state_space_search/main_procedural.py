## working script using only functions

from matplotlib import pyplot as plt
import numpy as np

## state space
GRID_SIZE = (50, 50)
START_NODE = (24, 24)
GOAL_NODE = (10, 10)

## moves
L = (1, 0)
R = (-1, 0)
U = (0, -1)
D = (0, 1)

MOVES = [R,L,D,U]

grid = np.zeros(GRID_SIZE)
noise = np.random.rand(GRID_SIZE[0], GRID_SIZE[1])
grid[noise > 0.90] = 1
grid[START_NODE] = 0.2
grid[GOAL_NODE] = 0.8

# >> draw and add this later
grid[4:20, 20] = 1

# >> draw and add this later
grid[(START_NODE[0]-3):(START_NODE[0] + 4),(START_NODE[1]-3):(START_NODE[1] + 4)] = 0

def solve_dfs(grid, start, goal):
    rows, cols = grid.shape
    
    # LIST as a STACK (LIFO)
    # append to the end and pop from the end
    stack = [start]
    
    # SET as a list of visited - instant checking if 'x is in set'
    visited = set()
    
    # DICTIONARY for a path reconstruction
    # key = child node, value = parent node
    parent_map = {}
    
    print(f"Starting search from [{start}] to [{goal}]...")
    
    while stack:
        # 1. get current node (pop from stack)
        current = stack.pop()
        
        # BFS
        # current = stack.pop(0)
        
        # 2. check if we won
        if current == goal:
            print("Goal reached!")
            return reconstruct_path(parent_map, start, goal)
        
        # 3. check if visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # 4. explore neighbours
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
                        
                        # BFS
                        # if next_node not in parent_map:
                        #     parent_map[next_node] = current
    
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
    # return path
    return path

final_path = solve_dfs(grid, START_NODE, GOAL_NODE)

if final_path:
    iterator = 0
    for r, c in final_path:
        grid[r,c] = 0.5 + iterator/len(final_path) * 0.2
        iterator += 1
    
    grid[START_NODE] = 0.2
    grid[GOAL_NODE] = 0.8

    plt.imshow(grid, cmap='hot', interpolation='nearest')
    plt.show()