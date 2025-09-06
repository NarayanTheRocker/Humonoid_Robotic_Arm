# Robotic Arm Gesture Control with Computer Vision

This project demonstrates a **physical robotic arm controlled by human hand gestures** using advanced **computer vision techniques**, without the need for physical sensors or gloves.  
The system uses a **webcam** to capture hand movements and translates them into commands for an **Arduino Uno**, which in turn controls the robotic arm.

---

## 🚀 How It Works
The system operates in a **three-step process**:

1. **Hand Detection**  
   The Python script uses the `cvzone.HandTrackingModule` to detect a human hand in real-time from a webcam feed.  
   This module, built upon **OpenCV** and **MediaPipe**, accurately identifies the hand and its key landmarks.

2. **Gesture-to-Data Conversion**  
   The script analyzes which fingers are raised and converts this information into a simple, encoded string  
   (e.g., `$01100`).  
   - Each digit represents a finger (Thumb → Pinky).  
   - `1` = Raised, `0` = Down.  

3. **Serial Communication**  
   The generated string is sent from the computer to an **Arduino Uno board** via serial communication.  
   The `serial.tools` library is used to automatically find the correct serial port for the Arduino.  
   The Arduino then controls the **servo motors** on the robotic arm based on this data.

---

## 🛠️ Requirements

### Hardware
- A physical robotic arm with **servo motors**
- **Arduino Uno board**
- **Webcam** (or integrated laptop camera)
- **USB cable** for the Arduino

### Software
- Python **3.x**
- Arduino IDE

### Python Libraries
You can install the required Python libraries using pip:

```bash
pip install cvzone
pip install pyserial
