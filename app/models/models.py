from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    year = db.Column(db.String(20), nullable=False, unique=True)
    director = db.Column(db.String(100), nullable=False, unique=True)
    repart = db.Column(db.String(350), nullable=False, unique=True)
    genre = db.Column(db.String(150), nullable=False, unique=True)
    trailer = db.Column(db.String(150), nullable=False, unique=True)

    def __init__(self, name, year, director, repart, genre, trailer):
        self.name = name
        self.year = year
        self.director = director
        self.repart = repart
        self.genre = genre
        self.trailer = trailer
