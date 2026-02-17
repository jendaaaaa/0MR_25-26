import numpy as np
import time

#########################################
# list (heterogeneous, mutable)
print("----- LIST -----\n")


mission = ["Calibrate", "Move Home", "Wait"]
mission.append("Measure") 
current_task = mission.pop(0) 

print(f"Doing: {current_task}")
print(f"Remaining: {mission}")

#########################################
# not an array
print("\n----- LIST is not an ARRAY -----\n")

# do not use for vectors
x_list = [1.5, 2.0, 3.0]
print("Python List")
print(x_list)         # basic vector
x_list = x_list * 2
print(x_list)         # not a dot product!

# instead use numpy array
print("Numpy Array")
x_numpy = np.array([1.5, 2.0, 3.0])
print(x_numpy)
x_numpy = x_numpy * 2
print(x_numpy)        # thats what we wanted!

#########################################
# numpy array (homogeneous, mutable)
print("\n----- NUMPY ARRAY -----\n")
# this is how we write matrixes and vectors
A = np.array([
    [0.0, 1.0],
    [-2.0, -0.5]
])

x = np.array([
    [10.0],
    [0.0]
])

dx = A @ x
print("dx = ")
print(dx)

#########################################
# list vs array comparison
print("\n----- LIST vs ARRAY -----\n")
size = 1_000_000

list_data = list(range(size))
array_data = np.array(list_data)

## LIST
start = time.time()
list_result = []
for x in list_data:
    list_result.append(x * 2)
    
stop = time.time()
list_time = stop - start
print(f"List time: {list_time} s")

## ARRAY
start = time.time()
array_result = array_data * 2
stop = time.time()
array_time = stop - start
print(f"Array time: {array_time} s")

print(f"Array is {(list_time / array_time):.1f}x faster!")

#########################################
# tuples (heterogeneous, not mutable)
print("\n----- TUPLES -----\n")

start_node = (1, 1)
goal_node = (20, 20)

print(start)
# start[1] = 0
# print(start)

start = (2, 1, 2)
print(start)

#########################################
# sets (unique objects, mutable)
print("\n----- SETS -----\n")

EMPTY = 0
OBSTACLE = 1

obstacles = {(1,1), (2,1), (4,2), (1,3)}
current_position = (1,1)

if current_position in obstacles:
    print("CRASH!")
    

#########################################
# dicts (key, value)
print("\n----- DICTS -----\n")

# just like JSON - config files etc.
robot_config = {
    "name": "BOT_01",
    "max_vel": 2.5,
    "pid": {
        "kp": 1.0,
        "kd": 0.1
    }
}
print(robot_config["name"])

# or as the parent map CHILD: PARENT
start = (0,0)
current_node = start
parent_map = {}

next_node = (0,1)
parent_map[next_node] = current_node
print(f"Step 1 Map: {parent_map}")

current_node = next_node
next_node = (1,1)
parent_map[next_node] = current_node
print(f"Step 2 Map: {parent_map}")

current_node = next_node
next_node = (1,2)
parent_map[next_node] = current_node
print(f"Step 3 Map: {parent_map}\n")

# backtracking
current_node = next_node
print(current_node)

parent = parent_map[current_node]
print(f"{current_node} came from {parent}")

grandparent = parent_map[parent]
print(f"{parent} came from {grandparent}")




#########################################
# enumerate (index loop)
print("\n----- ENUMERATE -----\n")

waypoints = ["Start", "Check_1", "Check_2", "Goal"]

# enumerate function gives you a counter automatically
for i, point in enumerate(waypoints):
    print(f"Target {i}: {point}")
    
# instead of
for i in range(len(waypoints)):
    print(f"Target {i}: {point}")




#########################################
# zip (parallel loop)
print("\n----- ZIP -----\n")

sensors = [0.1, 0.5, 0.9, 0.2] # lidar distances
times   = [0.0, 0.1, 0.2, 0.3] # timestamps

# "zip" them together
for dist, t in zip(sensors, times):
    velocity = dist / (t + 0.01) # avoid zero division
    print(f"Time: {t}s | Vel: {velocity:.2f}")




#########################################
# unpacking tuples
print("\n----- UNPACKING TUPLES -----\n")

def get_robot_state():
    return 10.5, 20.3, 90.0 # x, y, theta (implicitly returns tuple)

# unpack into 3 variables in one line
x, y, theta = get_robot_state()

# ignore values with underscore '_'
x, y, _ = get_robot_state()



#########################################
# list comprehensions
print("\n----- LIST COMPREHENSIONS -----\n")

readings_m = [1.2, 0.5, 3.1, 0.0]

# [ EXPRESSION for ITEM in LIST ]
readings_mm = [r * 1000 for r in readings_m] 

# You can even add an IF statement inside
valid_readings = [r for r in readings_m if r > 0]

print(f"Valid: {valid_readings}") # output: [1.2, 0.5, 3.1]