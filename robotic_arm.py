from serial.tools import list_ports
import serial
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector

# Find the Arduino board by looking for a port with "Arduino" in its description
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

