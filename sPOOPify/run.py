from app import make_app, db
import os
app = make_app()
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)