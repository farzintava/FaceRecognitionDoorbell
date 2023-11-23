# FaceRecognitionDoorbell/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, Response
import os
from datetime import datetime
import face_detection
import face_rec
from camera import capture_image
from camera import VideoCamera
import cv2



app = Flask(__name__)
app.secret_key = 'some_secret_key'  # This should ideally be stored securely.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'data', 'known_faces')
LOGS = []  # This will simulate our visitor logs for now.

face_rec.load_known_faces()

# FaceRecognitionDoorbell/app.py (additions)




@app.route('/')
def index():
    """Main dashboard showing recognized and unknown visitors."""
    # TODO: Recognize faces and update LOGS accordingly.
    return render_template('index.html', logs=LOGS)

# FaceRecognitionDoorbell/app.py (modifications to the add_face route)

@app.route('/add_face', methods=['GET', 'POST'])
def add_face():
    """Interface to add new known faces to the system."""
    if request.method == 'POST':
        name = request.form.get('name')
        method = request.form.get('method')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not name:
            flash('Name is required!')
            return redirect(url_for('add_face'))
        
        image_path = os.path.join(KNOWN_FACES_DIR,f"{name}-{timestamp}.jpg")

        if method == 'upload':
            image = request.files.get('image')
            if not image:
                flash('Image is required for the upload method!')
                return redirect(url_for('add_face'))
            # image_path = os.path.join(KNOWN_FACES_DIR,f"{name}-{timestamp}.jpg")
            image.save(image_path)
        elif method == 'webcam':
            # image_path = os.path.join(KNOWN_FACES_DIR, f'{name}-{timestamp}.jpg')
            capture_image(image_path)

        # Detect faces in the saved image.
        detected_faces = face_detection.detect_faces(image_path)
        if not detected_faces:
            flash('No faces detected in the image!')
            return redirect(url_for('add_face'))

        img = cv2.imread(image_path)
        for (top, right, bottom, left) in detected_faces:
            face_img = img[top:bottom, left:right]
            cv2.imwrite(image_path, face_img)

        flash(f'Added {name} to known faces!')
        return redirect(url_for('index'))

    return render_template('add_face.html')

@app.route('/live_feed')
def live_feed():
    return Response(face_rec.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logs')
def logs():
    """Show logs of all visitors (recognized and unrecognized)."""
    return render_template('logs.html', logs=LOGS)



@app.route('/capture')
def capture():
    """Capture an image using the local machine's webcam and recognize the face."""
    image_path = os.path.join(BASE_DIR, 'data', 'captured_image.jpg')
    capture_image(image_path)
    
    detected_faces = face_detection.detect_faces(image_path)
    img = cv2.imread(image_path)
    for (top, right, bottom, left) in detected_faces:
        face_img = img[top:bottom, left:right]
        cv2.imwrite(image_path, face_img)
    
    # Recognize the face in the captured image
    recognized_name = face_rec.recognize_face(image_path)
    
    # Create a log entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if recognized_name != "Unknown":
        LOGS.append({"name": recognized_name, "timestamp": timestamp})
        flash(f'Visitor recognized as {recognized_name}!')
    else:
        # Save the unknown face image for review
        unknown_image_path = os.path.join(BASE_DIR, 'data', 'unknown_faces', f'unknown_{timestamp}.jpg')
        os.rename(image_path, unknown_image_path)
        LOGS.append({"name": "Unknown", "timestamp": timestamp})
        flash('Visitor could not be recognized!')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
