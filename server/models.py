from datetime import date
from config import db, bcrypt, ma
from marshmallow import post_load, validates, ValidationError

class Traveler(db.Model):
  __tablename__ = 'travelers'

  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(30), nullable=False)
  lname = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(60), unique=True, nullable=False)
  _password_hash = db.Column(db.String, nullable=False)

  bookings = db.relationship('Booking', backref='traveler', lazy=True)

  def set_password(self, password):
    if len(password) < 8:
      raise ValueError("Password must be at least 8 characters long")
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = password_hash.decode('utf-8')

  def authenticate(self, password):
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

  def __repr__(self):
    return f'<Traveler {self.fname} {self.lname}>'
  
class Tour(db.Model):
  __tablename__ = 'tours'

  id = db.Column(db.Integer, primary_key=True)
  tour_title = db.Column(db.String(100), unique=True, nullable=False)
  tour_description = db.Column(db.Text, nullable=False)

  bookings = db.relationship('Booking', backref='tour', lazy=True)

  def __repr__(self):
    return f'<Tour {self.tour_title}>'

class Itinerary(db.Model):
  __tablename__ = 'itineraries'

  id = db.Column(db.Integer, primary_key=True)
  trip_title = db.Column(db.String(100), nullable=False)
  trip_length = db.Column(db.Integer, nullable=False)
  trip_route = db.Column(db.Text, nullable=False)
  trip_price = db.Column(db.Float, nullable=False)

  bookings = db.relationship('Booking', backref='itinerary', lazy=True)

  def __repr__(self):
    return f'<Itinerary {self.trip_title}>'

class Booking(db.Model):
  __tablename__ = 'bookings'

  id = db.Column(db.Integer, primary_key=True)
  number_of_travelers = db.Column(db.Integer, nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  total_price = db.Column(db.Float, nullable=False)
  status = db.Column(db.String(20), nullable=False, default='pending')

  traveler_id = db.Column(db.Integer, db.ForeignKey('travelers.id'), nullable=False)
  tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
  itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)

  def __repr__(self):
    return f'<Booking {self.id}>'

  def validate_dates(self):
    if self.end_date <= self.start_date:
      raise ValueError("End date must be after start date")

class TravelerSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Traveler
    load_instance = True
    exclude = ('_password_hash', 'bookings')
  password = ma.String(load_only=True)

  @validates('email')
  def validate_email(self, value):
    if '@' not in value or '.' not in value:
      raise ValidationError('Invalid email format')
    if len(value) < 5:
      raise ValidationError('Email must be at least 5 characters long')

  @validates('fname')
  def validate_fname(self, value):
    if len(value) < 2:
      raise ValidationError('First name must be at least 2 characters long')
    if not value.replace(' ', '').isalpha():
      raise ValidationError('First name must contain only letters and spaces')

  @validates('lname')
  def validate_lname(self, value):
    if len(value) < 2:
      raise ValidationError('Last name must be at least 2 characters long')
    if not value.replace(' ', '').isalpha():
      raise ValidationError('Last name must contain only letters and spaces')

  @post_load
  def make_traveler(self, data, **kwargs):
    if 'password' in data:
      traveler = Traveler(
        fname=data['fname'],
        lname=data['lname'],
        email=data['email']
      )
      traveler.set_password(data['password'])
      return traveler
    return Traveler(**data)
  
class TourSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Tour
    load_instance = True
    exclude = ('bookings',)

  @validates('tour_title')
  def validate_tour_title(self, value):
    if len(value) < 5:
      raise ValidationError('Tour title must be at least 5 characters long')

  @validates('tour_description')
  def validate_tour_description(self, value):
    if len(value) < 20:
      raise ValidationError('Tour description must be at least 20 characters long')

class ItinerarySchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Itinerary
    load_instance = True
    exclude = ('bookings',)

  @validates('trip_title')
  def validate_trip_title(self, value):
    if len(value) < 5:
      raise ValidationError('Trip title must be at least 5 characters long')

  @validates('trip_length')
  def validate_trip_length(self, value):
    if value <= 0:
      raise ValidationError('Trip length must be greater than 0')

  @validates('trip_price')
  def validate_trip_price(self, value):
    if value <= 0:
      raise ValidationError('Trip price must be greater than 0')

  @validates('trip_route')
  def validate_trip_route(self, value):
    if len(value) < 20:
      raise ValidationError('Trip route must be at least 20 characters long')

class BookingSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Booking
    load_instance = True
    include_fk = True

  traveler = ma.Nested(TravelerSchema)
  tour = ma.Nested(TourSchema)
  itinerary = ma.Nested(ItinerarySchema)

  @validates('number_of_travelers')
  def validate_number_of_travelers(self, value):
    if value <= 0:
      raise ValidationError('Number of travelers must be greater than 0')

  @validates('start_date')
  def validate_start_date(self, value):
    if value < date.today():
      raise ValidationError('Start date must be in the future')

  @validates('end_date')
  def validate_end_date(self, value, **kwargs):
    if 'start_date' in kwargs['data'] and value <= kwargs['data']['start_date']:
      raise ValidationError('End date must be after start date')

  @validates('total_price')
  def validate_total_price(self, value):
    if value <= 0:
      raise ValidationError('Total price must be greater than 0')

  @validates('status')
  def validate_status(self, value):
    valid_statuses = ['pending', 'confirmed', 'cancelled']
    if value not in valid_statuses:
      raise ValidationError(f'Status must be one of: {", ".join(valid_statuses)}')
