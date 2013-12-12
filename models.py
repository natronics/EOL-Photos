from app import db


class PhotoSet(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<set %r>' % self.id

