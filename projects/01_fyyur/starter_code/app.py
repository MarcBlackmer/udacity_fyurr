#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from flask_migrate import Migrate
import psycopg2
import sys


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.order_by('name').all()
  areas = Venue.query.distinct('city').all()
  return render_template('pages/venues.html', venues=venues, areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  response=Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue=Venue.query.get(venue_id)

  old_shows = (
    Show.query.with_entities(Artist.id, Artist.name, Artist.image_link, Show.start_time)
    .join(Artist).join(Venue)
    .filter(Venue.id == venue_id, Show.start_time < datetime.today())
    .all()
  )

  past_shows = []
  p = 0

  for show in old_shows:
    past_gigs = {}
    p += 1
    past_gigs['artist_id'] = show[0]
    past_gigs['artist_name'] = show[1]
    past_gigs['artist_image_link'] = show[2]
    past_gigs['start_time'] = show[3].strftime('%A %d-%b-%Y %H:%M')
    past_shows.append(past_gigs)

  new_shows = (
    Show.query.with_entities(Artist.id, Artist.name, Artist.image_link, Show.start_time)
    .join(Artist).join(Venue)
    .filter(Venue.id == venue_id, Show.start_time >= datetime.today())
    .all()
  )

  upcoming_shows = []
  u = 0

  for show in new_shows:
    new_gigs = {}
    u += 1
    new_gigs['artist_id'] = show[0]
    new_gigs['artist_name'] = show[1]
    new_gigs['artist_image_link'] = show[2]
    new_gigs['start_time'] = show[3].strftime('%A %d-%b-%Y %H:%M')
    upcoming_shows.append(new_gigs)

  data = {
    'id': venue.id,
    'name': venue.name,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'genres': venue.genres,
    'website': venue.website_link,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'past_shows': past_shows,
    'past_shows_count': p,
    'upcoming_shows': upcoming_shows,
    'upcoming_shows_count': u
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  form=VenueForm(request.form)
  try:
    if form.validate_on_submit():
      venue_obj=Venue()
      form.populate_obj(venue_obj)
      db.session.add(venue_obj)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Venue creation failed for the following reason(s): ')
      flash(form.errors)
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE', 'GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error=False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue was successfully deleted!')
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    flash('There was an error. The venue was not deleted!')
  finally:
    db.session.close()

  return render_template('pages/venues.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.order_by('name').all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  response=Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist=Artist.query.get(artist_id)

  old_shows = (
    Show.query.with_entities(Venue.id, Venue.name, Venue.image_link, Show.start_time)
    .join(Artist).join(Venue)
    .filter(Artist.id == artist_id, Show.start_time < datetime.today())
    .all()
  )

  past_shows = []
  p = 0

  for show in old_shows:
    past_gigs = {}
    p += 1
    past_gigs['venue_id'] = show[0]
    past_gigs['venue_name'] = show[1]
    past_gigs['venue_image_link'] = show[2]
    past_gigs['start_time'] = show[3].strftime('%A %d-%b-%Y %H:%M')
    past_shows.append(past_gigs)

  new_shows = (
    Show.query.with_entities(Venue.id, Venue.name, Venue.image_link, Show.start_time)
    .join(Artist).join(Venue)
    .filter(Artist.id == artist_id, Show.start_time >= datetime.today())
    .all()
  )

  upcoming_shows = []
  u = 0

  for show in new_shows:
    new_gigs = {}
    u += 1
    new_gigs['venue_id'] = show[0]
    new_gigs['venue_name'] = show[1]
    new_gigs['venue_image_link'] = show[2]
    new_gigs['start_time'] = show[3].strftime('%A %d-%b-%Y %H:%M')
    upcoming_shows.append(new_gigs)

  data = {
    'id': artist.id,
    'name': artist.name,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'genres': artist.genres,
    'website': artist.website_link,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'past_shows_count': p,
    'upcoming_shows': upcoming_shows,
    'upcoming_shows_count': u
  }

  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<artist_id>/delete', methods=['DELETE', 'GET'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error=False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('Artist was successfully deleted!')
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    flash('There was an error. The artist was not deleted!')
  finally:
    db.session.close()

  return render_template('pages/artists.html')
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  artist=Artist.query.get(artist_id)
  form=ArtistForm(obj=artist)
  try:
    if form.validate_on_submit():
      artist.name=form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data
      artist.genres=form.genres.data
      artist.image_link=form.image_link.data
      artist.facebook_link=form.facebook_link.data
      artist.website_link=form.website_link.data
      artist.seeking_venue=form.seeking_venue.data
      artist.seeking_description=form.seeking_description.data
      db.session.commit()
      flash(request.form['name'] + ' was successfully updated!')
    else:
      flash('Artist edit failed for the following reason(s): ')
      flash(form.errors)
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  try:
    if form.validate_on_submit():
      venue.name=form.name.data
      venue.city=form.city.data
      venue.state=form.state.data
      venue.address=form.address.data
      venue.phone=form.phone.data
      venue.genres=form.genres.data
      venue.image_link=form.image_link.data
      venue.facebook_link=form.facebook_link.data
      venue.website_link=form.website_link.data
      venue.seeking_talent=form.seeking_talent.data
      venue.seeking_description=form.seeking_description.data
      flash(request.form['name'] + ' was successfully updated!')
      db.session.commit()
    else:
      flash('Venue edit failed for the following reason(s): ')
      flash(form.errors)
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  form=ArtistForm(request.form)
  try:
    if form.validate_on_submit():
      artist_obj=Artist()
      form.populate_obj(artist_obj)
      db.session.add(artist_obj)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Artist creation failed for the following reason(s): ')
      flash(form.errors)
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = (
    Show.query.with_entities(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Show.start_time)
    .join(Venue)
    .join(Artist)
    .filter(Show.start_time >= datetime.today())
    .all()
  )

  data = []
  for show in shows:
    gig = {}
    gig['venue_id'] = show[0]
    gig['venue_name'] = show[1]
    gig['artist_id'] = show[2]
    gig['artist_name'] = show[3]
    gig['artist_image_link'] = show[4]
    gig['start_time'] = show[5].strftime('%A %d-%b-%Y %H:%M')
    data.append(gig)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error=False
  form=ShowForm()
  try:
    if form.validate_on_submit():
      show=Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    else:
      flash('Show creation failed for the following reason(s): ')
      flash(form.errors)
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
