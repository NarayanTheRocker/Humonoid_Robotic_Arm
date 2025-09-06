# Robotic Arm Gesture Control with Computer Vision
This project demonstrates a physical robotic arm controlled by human hand gestures using advanced computer vision techniques, without the need for physical sensors or gloves. The system uses a webcam to capture hand movements and translates them into commands for an Arduino Uno, which in turn controls the robotic arm.

How It Works
The system operates in a three-step process:

Hand Detection: The Python script uses the cvzone.HandTrackingModule to detect a human hand in real-time from a webcam feed. This module, built upon OpenCV and MediaPipe, accurately identifies the hand and its key landmarks.

Gesture-to-Data Conversion: The script analyzes which fingers are raised and converts this information into a simple, encoded string (e.g., $01100). This string represents the state of the five fingers (thumb, index, middle, ring, pinky), with 1 for a raised finger and 0 for a down one.

Serial Communication: The generated string is sent from the computer to an Arduino Uno board via serial communication. The serial.tools library is used to automatically find the correct serial port for the Arduino. The Arduino receives this data and uses it to control the servo motors on the robotic arm.

Requirements
Hardware
A physical robotic arm with servo motors

Arduino Uno board

Webcam or integrated laptop camera

USB cable for the Arduino

Software
Python 3.x

Arduino IDE

Python Libraries
You can install the required Python libraries using pip:

pip install cvzone
pip install pyserial

The Code
Python Script
The following Python script is the core of the computer vision and serial communication component. It handles hand detection, gesture encoding, and sending the data to the Arduino.

from serial.tools import list_ports
import serial
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector

# Find the Arduino board by looking for a port with "Arduino Uno" in its description
for port, desc, hwid in sorted(list_ports.comports()):
    if "Arduino Uno" in desc:
        arduino_port = port
        print(f"Arduino found in port {arduino_port}")
        break
else:
    print("Arduino not found!")
    exit()
    
ser = serial.Serial(arduino_port, 9600, timeout=1)

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1, detectionCon=0.7)

while True:
    success, img = cap.read()
    lmList, bbox = detector.findHands(img)

    if lmList:
        fingers = [0 if finger else 1 for finger in detector.fingersUp(lmList[0])]
        fingers_data = ''.join(str(i) for i in fingers)
        fingers_str = '$' + fingers_data
        ser.write(fingers_str.encode())
        print("Sending data: ", fingers_str)
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)

ser.close()


Arduino Sketch
You will need to write and upload a corresponding Arduino sketch to the board. This sketch must be able to:

Read the serial data sent from the Python script.

Parse the incoming string to get the five finger values.

Control the servo motors on the robotic arm based on these values.

The Python script sends a string that starts with a $ character, which can be used as a start marker for your Arduino's serial parser. The following five characters will be 0 or 1, representing each finger's state.
