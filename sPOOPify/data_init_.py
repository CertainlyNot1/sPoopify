from app import make_app, db
from app.models import Artist, Album, Song
from datetime import date
app = make_app()
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Додаємо артистів
        artist1 = Artist(name="Ariana Grande", bio="American singer and actress.")
        artist2 = Artist(name="Drake", bio="Canadian rapper, singer, and songwriter.")
        artist3 = Artist(name="Billie Eilish", bio="American singer-songwriter.")
        
        # Додаємо альбоми
        album1 = Album(title="Thank U, Next", artist=artist1, release_date=date(2019, 2, 8))
        album2 = Album(title="Scorpion", artist=artist2, release_date=date(2018, 6, 29))
        album3 = Album(title="When We All Fall Asleep, Where Do We Go?", artist=artist3, release_date=date(2019, 3, 29))
        
        # Додаємо пісні
        song1 = Song(title="7 Rings", album=album1, genre="Pop", file_path="maMony.mp3", play_count=1000, artist_id=3)
        song2 = Song(title="In My Feelings", album=album2, genre="Hip Hop", file_path="Petah.mp3", play_count=500, artist_id=3)
        db.session.add_all([artist1, artist2, artist3, album1, album2, album3, song1, song2])

        db.session.commit()
        print("Database initialized with sample data!")
if __name__ == "__main__":
    init_db()