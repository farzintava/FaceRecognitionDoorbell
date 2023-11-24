# FaceRecognitionDoorbell/models.py

from extensions import db
from datetime import datetime
import pickle
import numpy as np

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class KnownFace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    encoding = db.Column(db.PickleType, nullable=False)
    image_path = db.Column(db.String(200),nullable=False)

    def set_encoding(self, encoding):
        self.encoding = pickle.dumps(encoding)

    def get_encoding(self):
        return pickle.loads(self.encoding)

