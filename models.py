from app import db


class PhotoSet(db.Model):

    __tablename__ = 'photoset'

    id = db.Column(db.String(8), primary_key=True)
    date = db.Column(db.Date)
    photos = db.relationship('Photo', backref='photoset')

    def __repr__(self):
        return '<set %r>' % self.id


class Photo(db.Model):

    __tablename__ = 'photo'

    mission = db.Column(db.String(8), primary_key=True, autoincrement=False)
    roll = db.Column(db.String(8), primary_key=True, autoincrement=False)
    frame = db.Column(db.Integer, primary_key=True, autoincrement=False)
    set_id = db.Column(db.String(8), db.ForeignKey('photoset.id'))
