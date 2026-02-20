from matplotlib import pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from collections import deque
import time

class GridMap:
    def __init__(self, size=(50,50), start=(2,2), goal=(48,48)):
        self.rows, self.cols = size
        self.grid = np.zeros(size)
        self.start = start
        self.goal = goal
        
    def add_random_obstacles(self, density=0.2):
        noise = np.random.rand(self.rows, self.cols)
        self.grid[noise < density] = 1

        self.grid[self.start] = 0
        self.grid[self.goal] = 0
        
        num_walls = np.sum(self.grid == 1)
        print(f"Number of walls = {num_walls} | {(num_walls/self.grid.size):.2f} %")

    def add_cross(self, length, center = None):
        if not center:
            center_r, center_c = self.rows // 2, self.cols // 2
        else:
            center_r, center_c = center
        c_start = max(0, center_c - length)
        c_end   = min(self.cols, center_c + length + 1)
        self.grid[center_r, c_start:c_end] = 1
        r_start = max(0, center_r - length)
        r_end   = min(self.rows, center_r + length + 1)
        self.grid[r_start:r_end, center_c] = 1
        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def is_valid(self, node):
        r, c = node
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.grid[node] == 1:
            return False
        return True
    
    def create_visualization(self, path=None, title="Map", visited=None):
        display_grid = self.grid.copy()
        
        # only for visualization of visited states
        if visited:
            for i, (r,c) in enumerate(visited):
                display_grid[r, c] = 0.1 + (i / len(visited)) * 0.05
        
        if path:
            for i, (r,c) in enumerate(path):
                display_grid[r, c] = 0.4 + (i / len(path)) * 0.3
                
        display_grid[self.start] = 0.2
        display_grid[self.goal] = 0.8
        
        # we imagine the STATE SPACE as (x,y) but in numpy it is (row, column) -> (y, x)
        # we could change our mental model of the STATE SPACE or just use .transpose()
        
        # plus imshow is used for images where origin is LEFT TOP not LEFT BOTTOM
        # therefore moving DOWN is POSITIVE and UP is NEGATIVE
        
        plt.figure(figsize=(6, 6))
        plt.imshow(display_grid.transpose(), cmap='hot', interpolation='nearest')
        plt.title(title)
        
class BasePlanner(ABC):
    def __init__(self, grid_map: GridMap):
        self.map = grid_map
        # self.moves = [(0, -1), (-1, 0), (1, 0), (0, 1)] # WASD
        self.moves = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        
    @abstractmethod
    def solve(self):
        pass
    
    def _reconstruct_path(self, parent_map):
        path = []
        current = self.map.goal
        
        while current != self.map.start:
            path.append(current)
            current = parent_map[current]
        path.append(self.map.start)
        path.reverse()
        return path

class DFSPlanner(BasePlanner):
    def solve(self):
        print("Running DFS (Stack)...")
        stack = [self.map.start]
        visited = set()
        visited_list = [] # only for visualization of visited states!
        parent_map = {}
        
        while stack:
            current = stack.pop()
            visited.add(current)
            visited_list.append(current)
            
            if current == self.map.goal:
                print("Goal reached!")
                return self._reconstruct_path(parent_map), visited_list
            
            for move in self.moves:
                next_node = (current[0] + move[0], current[1] + move[1])
                
                if self.map.is_valid(next_node):
                    if next_node not in visited:
                        stack.append(next_node)
                        parent_map[next_node] = current
        
        print("Failed!")
        return None

class BFSPlannerSlow(BasePlanner):
    def solve(self):
        print("Running BFS (Queue)...")
        queue = [self.map.start]
        visited = set()
        visited_list = [] # only for visualization of visited states!
        parent_map = {}
        
        while queue:
            # pop(0) with List is very inefficient > all items have to move up 1 position
            current = queue.pop(0)
            
            if current == self.map.goal:
                print("Goal reached!")
                return self._reconstruct_path(parent_map), visited_list
            
            for move in self.moves:
                next_node = (current[0] + move[0], current[1] + move[1])
                
                if self.map.is_valid(next_node):
                    if next_node not in visited:
                        visited.add(current)
                        visited_list.append(current)
                        queue.append(next_node)
                        parent_map[next_node] = current

        print("Failed!")
        return None

class BFSPlanner(BasePlanner):
    def solve(self):
        print("Running BFS (Queue) using Deque...")
        queue = deque([self.map.start])
        visited = set()
        visited_list = [] # only for visualization of visited states!
        parent_map = {}
        
        while queue:
            # deque from collections is optimised for popleft
            current = queue.popleft()
            
            if current == self.map.goal:
                print("Goal reached!")
                return self._reconstruct_path(parent_map), visited_list
            
            if current in visited:
                continue
            
            visited.add(current)
            visited_list.append(current)
            
            for move in self.moves:
                next_node = (current[0] + move[0], current[1] + move[1])
                
                if self.map.is_valid(next_node):
                    if next_node not in visited:
                        queue.append(next_node)
                        parent_map[next_node] = current

        print("Failed!")
        return None

if __name__ == "__main__":
    world = GridMap(size=(100, 100), start=(10,10), goal=(90,40))
    world.add_random_obstacles(density=0.1)
    world.add_cross(30)
    world.add_cross(10, (30,10))
    world.add_cross(10, (70,90))
    
    dfs = DFSPlanner(world)
    bfs = BFSPlanner(world)
    path_dfs, visited_dfs = dfs.solve()
    path_bfs, visited_bfs = bfs.solve()
    
    # with visited
    world.create_visualization(path_dfs, "DFS Path (Stack)", visited_dfs)
    world.create_visualization(path_bfs, "BFS Path (Queue)", visited_bfs)
    
    # without visited
    # world.create_visualization(path_dfs, "DFS Path (Stack)")
    # world.create_visualization(path_bfs, "BFS Path (Queue)")

    plt.show()