from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from app.models import Artist, Album, Song, Playlist

auth_bp = Blueprint('auth', __name__)

main_bp = Blueprint('main', __name__)

acc_bp = Blueprint('acc', __name__)

@auth_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            session['userId'] = user.id
            return redirect(url_for('main.main'))
        else:
            return 'Wrong password, please try again'
    return render_template("login.html")

@main_bp.route('/main')
def main():
    if 'userId' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['userId'])
    artists = Artist.query.limit(5).all()
    albums = Album.query.limit(5).all()
    songs = Song.query.limit(5).all()
    genres = db.session.query(Song.genre).distinct().all()
    genres = [g[0] for g in genres if g[0]]
    return render_template('main.html', username = user.username, artists = artists, albums = albums, songs = songs, genres = genres)

@main_bp.route('/songs')
def songs():
    songs = Song.query.all()
    return render_template('songs.html', songs = songs)

@main_bp.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('artists.html', artists = artists)

@main_bp.route('/album')
def albums():
    albums = Album.query.all()
    return render_template('albums.html', albums = albums)

@main_bp.route('/artist/<int:artist_id>')
def artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)  
    return render_template('artist.html', artist=artist)

@main_bp.route('/album/<int:album_id>')
def album(album_id):
    album = Album.query.get_or_404(album_id)  
    return render_template('album.html', album=album)

@main_bp.route('/song/<int:song_id>')
def song(song_id):
    song = Song.query.get_or_404(song_id)  
    user_playlists = Playlist.query.all()
    return render_template('song.html', song=song,user_playlists=user_playlists)

@acc_bp.route('/acc')
def acc():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template("acc.html",user = user)
@acc_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@main_bp.route('/filter_songs')
def filter_songs():
    genre = request.args.get('genre', None)

    if genre:
        filtered_songs = Song.query.filter_by(genre=genre).order_by(Song.id.desc()).all()
    else:
        filtered_songs = Song.query.order_by(Song.id.desc()).all()
    
    songs_data = [
        {'title': song.title, "genre": song.genre, "file_path": song.file_path}
        for song in filtered_songs
    ]
    return jsonify({"songs": songs_data})

@main_bp.route('/search', methods = ['GET'])
def search():
    query = request.args.get('query','').strip()
    if not query:
        return render_template('srch.html', results = [], query = query)
    
    albums= Album.query.filter(Album.title.ilike(f'%{query}%')).all()
    songs = Song.query.filter(Song.title.ilike(f'%{query}%')).all()
    artists = Artist.query.filter(Artist.name.ilike(f'%{query}%')).all()
    results = {
        'albums':albums,
        'songs':songs,
        'artists':artists
    }
    return render_template('srch.html', results = results, query = query)
    
@main_bp.route('/playlists', methods = ["POST","GET"])
def playlists():
    if 'userId' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['userId']
    if request.method == 'POST':
        playlist_name = request.form['name']
        new_playlist = Playlist(name = playlist_name, user_id = user_id)
        db.session.add(new_playlist)
        db.session.commit()
        return redirect(url_for('main.playlists'))
    user_playlists = Playlist.query.filter_by(user_id=user_id).all()
    return render_template('playlists.html',playlists = user_playlists)

@main_bp.route('/addTo_playlist', methods = ['POST'])
def addToPLA():
    data = request.get_json()
    song_id = data.get('song_id')
    playlist_id = data.get('playlist_id')
    if not song_id or not playlist_id:
        return jsonify({'success': False,'message': 'Handicap rq'}), 400
    try:
        playlist = Playlist.query.get(playlist_id)
        song = Song.query.get(song_id)
        if not song or not playlist:
            return jsonify({'success': False,'message': 'Handicap rq'}), 400
    
        playlist.songs.append(song)
        db.session.commit()
        return jsonify({'success': True, 'message': 'No more melanin, YAYYYY!!!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@main_bp.route('/playlist/<int:playlist_id>')
def playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template('playlist.html', playlist=playlist)