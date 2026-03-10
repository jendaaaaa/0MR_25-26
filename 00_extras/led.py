import serial
import time

# --- CONFIGURATION ---
# For Mac: '/dev/cu.usbserial-0001'
# For Windows: 'COM3' (Check Device Manager!)
port_name = '/dev/cu.usbserial-0001'
baud_rate = 115200

try:
    ser = serial.Serial(port_name, baud_rate, timeout=1)
    time.sleep(2)  # Critical: Give the ESP8266 time to reboot after connecting
    
    print(f"--- Connected to {port_name} ---")
    print("Commands: '1' to turn LED ON, '0' to turn LED OFF, 'q' to quit")

    while True:
        user_input = input("Enter Command: ").strip()

        if user_input.lower() == 'q':
            break
        
        if user_input in ['1', '0']:
            # Send the character to the NodeMCU
            ser.write(user_input.encode('utf-8'))
            
            # Wait a moment and read the confirmation from the chip
            time.sleep(0.1)
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                # response = ser.readline().decode().strip()
                print(f"NodeMCU Response: {response}")
        else:
            print("Invalid input! Use 1, 0, or q.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")