# FaceRecognitionDoorbell/camera.py
import cv2
import time

# class VideoCamera:
#     def __init__(self):
#         # Capture video from the first USB camera device
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         success, image = self.video.read()
#         if success:
#             return cv2.imencode('.jpg', image)[1].tobytes()
#         else:
#             return None


def capture_image(filename):
    """
    Captures an image using the local machine's webcam and saves it with the provided filename.

    Parameters:
    - filename (str): Path where the captured image will be saved.
    """
    cap = cv2.VideoCapture(0)  # Open default camera (0)

    # Warm-up phase: Capture frames for a short duration without saving them
    warmup_time = time.time() + 2  # Warm-up for 2 seconds
    while time.time() < warmup_time:
        ret, _ = cap.read()
        time.sleep(0.05)  # Sleep for 50 milliseconds

    ret, frame = cap.read()  # Read a frame after warm-up

    if not ret:
        raise Exception("Could not capture image from webcam!")

    cv2.imwrite(filename, frame)  # Save the captured frame as an image
    cap.release()  # Release the camera resource
