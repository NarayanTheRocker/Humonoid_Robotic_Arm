from serial.tools import list_ports
import serial
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

def find_arduino():
    """Find the Arduino board and return its port."""
    for port, desc, hwid in sorted(list_ports.comports()):
        if "Arduino Uno" in desc:  # Modify this if you are using a different Arduino
            print(f"Arduino found on port {port}")
            return port
    return None

# Initialize Arduino connection
arduino_port = find_arduino()
if not arduino_port:
    print("Arduino not found!")
    exit()

try:
    ser = serial.Serial(arduino_port, 9600, timeout=1)
    time.sleep(2)  # Allow time for Arduino to reset
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    exit()

# Initialize hand detector
cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1, detectionCon=0.7)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from the camera.")
        break

    # Detect hand and landmarks
    lmList, bbox = detector.findHands(img)

    if lmList:
        # Get the state of fingers (1 for open, 0 for closed)
        fingers = detector.fingersUp(lmList[0])
        fingers_data = ''.join(str(int(finger)) for finger in fingers)
        fingers_str = f'${fingers_data}'
        print(f"Sending data: {fingers_str}")

        # Send data to Arduino and handle disconnection
        try:
            ser.write(fingers_str.encode())
        except serial.SerialException as e:
            print(f"Serial write failed: {e}")
            print("Attempting to reconnect...")
            ser.close()
            arduino_port = find_arduino()
            if arduino_port:
                try:
                    ser = serial.Serial(arduino_port, 9600, timeout=1)
                    time.sleep(2)  # Allow time for Arduino to reset
                    print("Reconnected to Arduino.")
                except serial.SerialException as e:
                    print(f"Failed to reconnect: {e}")
                    break
            else:
                print("Arduino not found during reconnection attempt. Exiting.")
                break

    # Display the image with hand landmarks
    cv2.imshow("Image", img)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
