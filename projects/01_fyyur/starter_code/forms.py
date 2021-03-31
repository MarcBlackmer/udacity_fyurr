from datetime import datetime
from flask_wtf import Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    AnyOf,
    URL,
    Email,
    Optional
)

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AK', 'AK'),
            ('AL', 'AL'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WI', 'WI'),
            ('WV', 'WV'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[Optional(),URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Cabaret', 'Cabaret'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(),URL()]
    )
    website_link = StringField(
        'website_link', validators=[Optional(),URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AK', 'AK'),
            ('AL', 'AL'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WI', 'WI'),
            ('WV', 'WV'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[Optional(),URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[Optional(),URL()]
     )

    website_link = StringField(
        'website_link', validators=[Optional(),URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )
