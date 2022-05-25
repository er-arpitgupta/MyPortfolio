from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    mail = db.Column(db.String(100)) 
    msg = db.Column(db.String(500))

    def __init__(self, name, phone, mail, msg) -> None:
        self.name = name
        self.phone = phone
        self.mail = mail
        self.msg = msg