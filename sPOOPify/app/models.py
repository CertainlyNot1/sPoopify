from .db import db  # Імпортуємо db з db.py
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    genre = db.Column(db.String(50), nullable=True)
    file_path = db.Column(db.String(150), nullable=False)
    play_count = db.Column(db.Integer, default=0)  # Нове поле для відстеження прослуховувань
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable = False)
    # Додаємо відношення до альбому

    artist = db.relationship('Artist', backref='songs', lazy=True)

    album = db.relationship('Album', backref='songs', lazy=True)
class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    release_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.now())  # Нове поле
class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    albums = db.relationship('Album', backref='artist', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='playlists', lazy=True)

    songs = db.relationship('Song', secondary='playlist_song', backref='playlists', lazy='dynamic')


playlist_song = db.Table(
    'playlist_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), primary_key=True)
)