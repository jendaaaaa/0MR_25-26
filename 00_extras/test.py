import serial
import time

# Replace 'COM3' with the port you saw in Arduino IDE
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)
time.sleep(2) # Wait for connection to settle

print("Listening for NodeMCU...")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")
except KeyboardInterrupt:
    print("\nClosing connection.")
    ser.close()