from datetime import date
from config import db, bcrypt, ma
from marshmallow import post_load

class Traveler(db.Model):
  __tablename__ = 'travelers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(60), unique=True, nullable=False)
  _password_hash = db.Column(db.String, nullable=False)

  bookings = db.relationship('Booking', backref='traveler', lazy=True)

  def set_password(self, password):
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = password_hash.decode('utf-8')

  def authenticate(self, password):
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

  def __repr__(self):
    return f'<Traveler {self.name}>'
  
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

  traveler_id = db.Column(db.Integer, db.ForeignKey('travelers.id'), nullable=False)
  tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
  itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)

  def __repr__(self):
    return f'<Booking {self.id}>'
