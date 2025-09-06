import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture and hand detector
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
        fingers_data = [0 if finger else 1 for finger in fingers]
        fingers_str = ''.join(str(i) for i in fingers_data)
        print("Detected fingers:", fingers_str)

    # Display the image with hand landmarks
    cv2.imshow("Image", img)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
