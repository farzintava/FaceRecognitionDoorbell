# FaceRecognitionDoorbell/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, Response, g
import os
from datetime import datetime
import face_recognition
import face_detection
import face_rec
from camera import capture_image
import cv2
from database import add_new_face,add_new_log
from extensions import db
from models import KnownFace, Log
import numpy as np



app = Flask(__name__)
app.secret_key = 'some_secret_key'  # This should ideally be stored securely.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/FaceRecognitionDoorbell/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'static/data', 'known_faces')
LOGS = []  # This will simulate our visitor logs for now.

# FaceRecognitionDoorbell/app.py (additions)


@app.route('/')
def index():
    """Main dashboard showing recognized and unknown visitors."""
    # TODO: Recognize faces and update LOGS accordingly.
    
    logs=Log.query.all()
    return render_template('index.html', logs=logs)

# FaceRecognitionDoorbell/app.py

@app.route('/manage_faces')
def manage_faces():
    known_faces = KnownFace.query.all()
    return render_template('manage_faces.html', known_faces=known_faces)

@app.route('/delete_face/<int:face_id>')
def delete_face(face_id):
    face = KnownFace.query.get_or_404(face_id)
    db.session.delete(face)
    db.session.commit()
    os.remove(f"static/data/known_faces/{face.image_path}")
    return redirect(url_for('manage_faces'))
# FaceRecognitionDoorbell/app.py (modifications to the add_face route)

@app.route('/add_face', methods=['GET', 'POST'])
def add_face():
    """Interface to add new known faces to the system."""
    if request.method == 'POST':
        name = request.form.get('name')
        method = request.form.get('method')
        timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        if not name:
            flash('Name is required!')
            return redirect(url_for('add_face'))
        
        image_path = os.path.join(KNOWN_FACES_DIR,f"{name}-{timestamp}.jpg")

        if method == 'upload':
            image = request.files.get('image')
            if not image:
                flash('Image is required for the upload method!')
                return redirect(url_for('add_face'))
            image.save(image_path)
        elif method == 'webcam':
            capture_image(image_path)

        # Detect faces in the saved image.
        detected_faces = face_detection.detect_faces(image_path)
        if not detected_faces:
            flash('No faces detected in the image!')
            os.remove(image_path)
            return redirect(url_for('add_face'))

        img = cv2.imread(image_path)
        for (top, right, bottom, left) in detected_faces:
            face_img = img[top:bottom, left:right]
            cv2.imwrite(image_path, face_img)
        face_image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(face_image)
        if face_encodings:
            add_new_face(db,name,face_encodings[0],f"{name}-{timestamp}.jpg")
        
        
        flash(f'Added {name} to known faces!')
        return redirect(url_for('index'))

    return render_template('add_face.html')

@app.route('/live_feed')
def live_feed():
    return render_template('live_feed.html')

@app.route('/video_feed')
def video_feed():
    return Response(face_rec.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/logs')
def logs():
    """Show logs of all visitors (recognized and unrecognized)."""
    logs=Log.query.all()
    return render_template('logs.html', logs=logs)



@app.route('/capture')
def capture():
    """Capture an image using the local machine's webcam and recognize the face."""
    image_path = os.path.join(BASE_DIR, 'static/data', 'captured_image.jpg')
    capture_image(image_path)
    
    
    detected_faces = face_detection.detect_faces(image_path)
    if not detected_faces:
        return redirect(url_for('index'))
    
    img = cv2.imread(image_path)
    for (top, right, bottom, left) in detected_faces:
        face_img = img[top:bottom, left:right]
        cv2.imwrite(image_path, face_img)
    
    
    face_encoding = face_recognition.face_encodings(img)
    print(f"face encoding: {type(face_encoding)}")
    known_faces = KnownFace.query.all()
    # Recognize the face in the captured image
    recognized_name = face_rec.recognize_face(face_encoding,known_faces)
    
    # Create a log entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if recognized_name != "Unknown":
        
        flash(f'Visitor recognized as {recognized_name}!')
    else:
        # Save the unknown face image for review
        unknown_image_path = os.path.join(BASE_DIR, 'static/data', 'unknown_faces', f'unknown_{timestamp}.jpg')
        os.rename(image_path, unknown_image_path)
        flash('Visitor could not be recognized!')
    add_new_log(db,recognized_name)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
