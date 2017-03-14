from . import db

class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    biography = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_on = db.Column(db.String(80))

    def __init__(self, userid, firstname, lastname, username, age, gender, biography, image, created_on):
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.age = age
        self.gender = gender
        self.biography = biography
        self.image = image
        self.created_on = created_on

    def get_userid(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
