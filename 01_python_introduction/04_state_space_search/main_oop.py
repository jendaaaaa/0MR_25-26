from matplotlib import pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from collections import deque
import time

class GridMap:
    def __init__(self, size=(50,50), start=(2,2), goal=(25,25)):
        self.rows, self.cols = size
        self.start = start
        self.goal = goal
        self.grid = np.zeros(size)
        
    def add_random_obstacles(self, density=0.2):
        noise = np.random.rand(self.rows, self.cols)
        self.grid[noise < density] = 1
        self.grid[self.start] = 0
        self.grid[self.goal] = 0
        
        num_walls = np.sum(self.grid == 1)
        print(f"Number of walls = {num_walls} | {(num_walls/self.grid.size):.2f} %")
        
    def is_valid(self, node):
        r, c = node
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.grid[node] == 1:
            return False
        return True
    
    def visualize(self, path=None, title="Map", visited=None):
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
        
        plt.figure(figsize=(6, 6))
        plt.imshow(display_grid, cmap='hot', interpolation='nearest')
        plt.title(title)
        plt.show()
        
class BasePlanner(ABC):
    def __init__(self, grid_map: GridMap):
        self.map = grid_map
        # self.moves = [(0, -1), (-1, 0), (1, 0), (0, 1)] # WASD
        self.moves = [(0, 1), (-1, 0), (1, 0), (0, -1)] # WDSA
        
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
                        stack.append(next_node)
                        parent_map[next_node] = current
        
        print("Failed!")
        return None

class BFSPlanner(BasePlanner):
    def solve(self):
        print("Running BFS (Queue)...")
        queue = [self.map.start]
        visited = set()
        visited_list = [] # only for visualization of visited states!
        parent_map = {}
        
        while queue:
            current = queue.pop(0)
            
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

class BFSPlannerEfficient(BasePlanner):
    def solve(self):
        print("Running BFS (Queue) using Deque...")
        queue = deque([self.map.start])
        visited = set()
        visited_list = [] # only for visualization of visited states!
        parent_map = {}
        
        while queue:
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
    world = GridMap(size=(100, 100), start=(10,10), goal=(90,90))
    # world = GridMap()
    world.add_random_obstacles(density=0.1)
    
    dfs = DFSPlanner(world)
    path_dfs, _ = dfs.solve()
    world.visualize(path_dfs, "DFS Path (Stack)")
    
    bfs = BFSPlanner(world)
    start = time.time()
    path_bfs, visited_bfs = bfs.solve()
    print(f"Time to solve with List = {(time.time() - start)} s")
    # world.visualize(path_bfs, "BFS Path (Queue)")
    
    bfs_efficient = BFSPlannerEfficient(world)
    start_efficient = time.time()
    path_bfs_eff, visited_bfs_eff = bfs_efficient.solve()
    print(f"Time to solve with Deque = {(time.time() - start_efficient)} s")
    world.visualize(path_bfs_eff, "BFS Path (Queue)", visited_bfs_eff)