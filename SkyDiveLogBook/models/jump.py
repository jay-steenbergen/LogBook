from db import db

class jumpModel(db.Model):
    __tablename__ = 'jumps'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.INT)
    dropZone = db.Column(db.String(80))

    logs_id = db.Column(db.Integer, db.ForeignKey('logs.id'))

    logs = db.relationship('logsModel')

    def __init__(self, number, dropZone, logs_id):

        self.number = number
        self.dropZone = dropZone
        self.logs_id = logs_id

    def json(self):
        return {'number': self.number, 'dropZone': self.dropZone}

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()   #select * from jumps where number=number

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()