# NodeMCU Installation Guide

This guide provides step-by-step instructions for setting up the NodeMCU (ESP8266) with the Arduino IDE, including troubleshooting steps for common connection issues.

---

## Arduino IDE Setup

Follow these steps to configure your environment:

1.  **Download Arduino IDE**: Get the software from the [official website](https://www.arduino.cc/en/software/).
2.  **Open Preferences**: Navigate to **File > Preferences** (or press `CTRL` + `.`).
3.  **Add Board URL**: In the "Additional boards manager URLs" field, paste the following link:
    `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
4.  **Install Board Package**: 
    * Open the **Boards Manager** (second icon on the left panel).
    * Search for **esp8266**.
    * Click **Install**.
5.  **Select Your Board**:
    * Go to **Tools > Board > esp8266 > NodeMCU 1.0 (ESP-12E Module)**.
    * Go to **Tools > Port** and select the active **COMx** port.
6.  **Upload**: Click **Sketch > Upload** (or press `CTRL` + `U`).



---

## Troubleshooting

### No Port Visible
If your computer does not recognize the NodeMCU, you likely need the **CP2102 driver**:
* **Download**: [Silicon Labs VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)

### Installation Failures
If the IDE is giving you trouble, you can use these web-based alternatives:
* **Binary Uploader**: [Adafruit WebSerial ESPTool](https://adafruit.github.io/Adafruit_WebSerial_ESPTool/)
* **Serial Monitor**: [Google Chrome Serial Terminal](https://googlechromelabs.github.io/serial-terminal/)

---

## Test Program

Copy and paste the code below into a new sketch to verify your connection. After uploading, open the **Serial Monitor** and set the baud rate to **115200**.

```cpp
void setup() {
  // Initialize serial communication at 115200 bits per second
  Serial.begin(115200);
}

void loop() {
  // Send the string to the computer
  Serial.println("Hello from NodeMCU!");
  
  // Wait for 1 second
  delay(1000);
}