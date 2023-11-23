# FaceRecognitionDoorbell/face_detection.py

import face_recognition
import face_rec

def detect_faces(image_path):
    """
    Detect faces in the given image.

    Parameters:
    - image_path (str): Path to the image file.

    Returns:
    - List of face locations [(top, right, bottom, left), ...]
    """
    
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    return face_locations
