# FaceRecognitionDoorbell/face_recognition.py

import face_recognition
import os
import cv2
import numpy as np


KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'known_faces')
KNOWN_FACE_ENCODINGS = []
KNOWN_FACE_NAMES = []

def load_known_faces():
    """
    Load known faces from the data directory and encode them.
    """
    global KNOWN_FACE_ENCODINGS, KNOWN_FACE_NAMES

    for file in os.listdir(KNOWN_FACES_DIR):
        image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, file))
        face_encoding = face_recognition.face_encodings(image)[0]
        KNOWN_FACE_ENCODINGS.append(face_encoding)
        KNOWN_FACE_NAMES.append(file.split('-')[0])

def recognize_face(image_path):
    """
    Recognize a face in the given image.

    Parameters:
    - image_path (str): Path to the image file.

    Returns:
    - Name of the recognized person or "Unknown".
    """
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    for face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(KNOWN_FACE_ENCODINGS, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = KNOWN_FACE_NAMES[first_match_index]

        return name

def gen_frames():
    """
    Captures video from the camera and processes each frame for face recognition.
    """
    video_capture = cv2.VideoCapture(0)  # 0 for the default camera
    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(KNOWN_FACE_ENCODINGS, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = KNOWN_FACE_NAMES[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                # face_distances = face_recognition.face_distance(KNOWN_FACE_ENCODINGS, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #     name = KNOWN_FACE_NAMES[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    video_capture.release()