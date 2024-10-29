
# Face Tracking with Raspberry Pi and Servo Motor

This project uses a Raspberry Pi and two servo motors to create a face-tracking system. The system detects a face in the camera feed and adjusts the servo motor's position to keep the face centered in the frame. This is achieved through computer vision using OpenCV, making it ideal for learning about object tracking, computer vision, and basic servo control.

## Features
- Detects faces in real-time using OpenCV
- Controls servo motors to track and center the detected face in the frame
- Can be adapted to track other objects with minor modifications

## Hardware Requirements
- Raspberry Pi 4 (or other compatible model)
- USB camera or Raspberry Pi camera module (for this project I have used a Logi tech USB Camera)
- 2 Servo motors (for this project I have used Hitec HS-645MG Ultra Torque Servo) for Pan Tilt

## Install Required Packages
```
# Install pigpio for servo control
sudo apt update
sudo apt install pigpio python3-pigpio

# Install OpenCV for face detection
pip install opencv-python opencv-python-headless
```
## Setup Pigpio Daemon
Start ```pigpiod ``` daemon for controlling GPIOs
```
sudo pigpiod
```
For runnning it on startup
```
sudo systemctl enable pigpiod
```
