# from extensions import db
from models import KnownFace, Log

def add_new_face(db,name,face_encoding,image_path):
    new_face = KnownFace(name=name,image_path=image_path)
    new_face.set_encoding(face_encoding)
    db.session.add(new_face)
    db.session.commit()
    
    
def add_new_log(db,name):
    new_log = Log(name=name)
    db.session.add(new_log)
    db.session.commit()
    