import cv2
import RPi.GPIO as GPIO
import time
import pigpio

# Initialize pigpio
pi = pigpio.pi()

# GPIO pin assignments
pan_pin = 27  # GPIO27 for pan (horizontal)
tilt_pin = 4  # GPIO4 for tilt (vertical)

# Set GPIO modes and frequencies
pi.set_mode(pan_pin, pigpio.OUTPUT)
pi.set_mode(tilt_pin, pigpio.OUTPUT)

pi.set_PWM_frequency(pan_pin, 50)
pi.set_PWM_frequency(tilt_pin, 50)

# Function to move the pan and tilt servos to a specified angle
def set_pan_angle(angle):
    pulse = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pan_pin, pulse)

def set_tilt_angle(angle):
    pulse = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(tilt_pin, pulse)

# Initialize pan and tilt angles to 90 degrees (center)
current_pan_angle = 90
current_tilt_angle = 90
set_pan_angle(current_pan_angle)
set_tilt_angle(current_tilt_angle)

# OpenCV's Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture (0 for USB Cam)
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Frame dimensions 
frame_width = 320
frame_height = 240
frame_center_x = frame_width // 2
frame_center_y = frame_height // 2

# Servo movement step size
servo_step = 2  # Adjust for smoother or faster movements

#video writer
record = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter('FaceTracking.avi',record,30.0,(320,240))

try:
    while True:
        # Capture a frame from the video feed
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        # Convert the frame to grayscale for face detection
        #Write frame to the video output
        video_out.write(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # If a face is detected
        if len(faces) > 0:
            (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])  # Track the largest face
            
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            print(face_center_y)
            # Pan (horizontal) control: move left or right
            if face_center_x < frame_center_x - 30:  # Face is to the left
                current_pan_angle = min(current_pan_angle + servo_step, 180)
                
            elif face_center_x > frame_center_x + 30:  # Face is to the right
                current_pan_angle = max(current_pan_angle - servo_step, 0)

            # Tilt (vertical) control: move up or down
            if face_center_y < frame_center_y - 30:  # Face is higher than center
                current_tilt_angle = max(current_tilt_angle +  servo_step, 60)
                
            elif face_center_y > frame_center_y + 30:  # Face is lower than center
                current_tilt_angle = min(current_tilt_angle - servo_step, 120)

            # Set the pan and tilt angles
            set_pan_angle(current_pan_angle)
            set_tilt_angle(current_tilt_angle)

        # Display the video frame with a rectangle around the detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            break  # Only track the first detected face
        
#         cv2.rectangle(frame,(30,30),(frame_width-30,frame_height-30),(0,0,255),2)
        # Show the video stream
        cv2.imshow('Face Tracking', frame)
        
        

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Face tracking interrupted")

finally:
    # Cleanup: stop PWM, clean up GPIO, release camera, and close windows
    GPIO.cleanup()
    video_capture.release()
    cv2.destroyAllWindows()
    pi.set_servo_pulsewidth(pan_pin, 0)  # Turn off pan servo
    pi.set_servo_pulsewidth(tilt_pin, 0)  # Turn off tilt servo
    pi.stop()