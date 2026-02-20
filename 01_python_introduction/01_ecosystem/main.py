# Python code runs from top to bottom
print("[main.py] importing modules...")

import numpy as np
import network_tools as nt
# we only want to import the library and use some of the methods
# but the code in GLOBAL SCOPE is executed here!

print("[main.py] executing script...")
print(f"pi = {np.pi}")

my_pc = "192.168.1.12"
target = "192.168.1.24"
nt.ping_target(target)
# instead of just pinging the target, we formatted remote drive!