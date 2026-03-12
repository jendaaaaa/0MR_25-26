import serial
import time

ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)
# ser = serial.Serial('COM3', ...)
time.sleep(2)
ser.reset_input_buffer()

while True:
    user_input = input("Enter cmd: ").strip()
    
    # if user_input in ["1", "0"]:
    
    if user_input == "1" or user_input == "0":
        ser.write(user_input.encode('utf-8'))
    
    # if ser.in_waiting > 0:
    #     message = ser.readline().decode()
    #     print(message)