import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

def ping_target(target):
    print(Fore.GREEN + f"[network_tools.py] Pinging target {target}...")
        
def format_drive(target):
    print(Back.YELLOW + f"[network_tools.py] Connecting to target {target}...")
    time.sleep(1)
    print(Back.GREEN + f"[network_tools.py] Connected to target {target}!")
    print(Back.RED + Fore.WHITE + f"[network_tools.py] Formatting drive...")
    time.sleep(1)
    print(Back.RED + Fore.WHITE + f"[network_tools.py] >>> Drive Formatted!")
    print(Style.RESET_ALL)
    
# # testing script (WRONG - outside entry point)
target = "192.168.1.12"
format_drive(target)

if __name__ == "__main__":
    # testing script (CORRECT - inside entry point, runs only when called using 'python' command)
    target = "192.168.1.12"
    format_drive(target)