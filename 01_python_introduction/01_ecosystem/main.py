print("[main.py] importing modules...")

import numpy as np
import network_tools as nt

print("[main.py] executing script...")

print(f"pi = {np.pi}")

my_pc = "192.168.1.12"
target = "192.168.1.24"
nt.ping_target(target)