import time

def ping_target(target):
    print(f"[network_tools.py] Pinging target {target}...")
        
def format_drive(target):
    print(f"[network_tools.py] Connecting to target {target}...")
    time.sleep(1)
    print(f"[network_tools.py] Connected to target {target}!")
    print(f"[network_tools.py] Formatting drive...")
    time.sleep(1)
    print(f"[network_tools.py] >>> Drive Formatted!")
    
# WRONG!
# defined in global scope -> being executed when imported to a different script!
# supposed to be only for testing the library
target = "192.168.1.12"
format_drive(target)

# CORRECT!
# inside entry point, runs only when called using 'python' command
if __name__ == "__main__":
    target = "192.168.1.12"
    format_drive(target)