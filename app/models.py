from app import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    versions = db.relationship('Version', backref='application', lazy=True)

    def __repr__(self):
        return '<application {}>'.format(self.name)


class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.String(), primary_key=True)
    file = db.Column(db.String(80), nullable=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))

    def serialize(self):
        return {"id": self.id,
                "file": self.file,
                "application_id": self.application_id.name}

    def __repr__(self):
        return '<version {}>'.format(self.id)
