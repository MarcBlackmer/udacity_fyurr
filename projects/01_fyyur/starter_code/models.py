from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'shows'

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
    start_time = db.Column(db.DateTime())

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venues', lazy=True)

    def __repr__(self):
        return f'<ID: { self.id }, Name: { self.name }, Genres: { self.genres } City: { self.city }, State: { self.state }>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artists', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<ID: { self.id }, Name: { self.name }, Genres { self.genres } City: { self.city }, State: { self.state }>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
