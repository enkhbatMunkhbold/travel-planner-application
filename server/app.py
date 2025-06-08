from flask import request, session
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from config import app, db, api, ma
from models import Traveler, Itinerary, Tour, Booking, TravelerSchema, ItinerarySchema, TourSchema, BookingSchema

traveler_schema = TravelerSchema()
travelers_schema = TravelerSchema(many=True)
tour_schema = TourSchema()
tours_schema = TourSchema(many=True)
itinerary_schema = ItinerarySchema()
itineraries_schema = ItinerarySchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Tours(Resource):
    def get(self):
        all_tours = Tour.query.all()
        return tours_schema.dump(all_tours), 200
    
    def post(self):
        try:
            data = request.get_json()
            new_tour = tour_schema.load(data)
            db.session.add(new_tour)
            db.session.commit()
            return tour_schema.dump(new_tour), 201
        except ValidationError as e:
            return {'error': str(e)}, 400
    
api.add_resource(Tours, '/tours')

class Itineraries(Resource):
    def get(self):
        all_itineraries = Itinerary.query.all()
        return itineraries_schema.dump(all_itineraries), 200
    
    def post(self):
        data = request.get_json()
        new_itinerary = itineraries_schema.load(data)
        db.session.add(new_itinerary)
        db.session.commit()
        return itineraries_schema.dump(new_itinerary), 201
    
api.add_resource(Itineraries, '/itineraries')

class Bookings(Resource):
    def get(self):
        all_bookings = Booking.query.all()
        return bookings_schema.dump(all_bookings), 200
    
    def post(self):
        try:
            data = request.get_json()
            new_booking = bookings_schema.load(data)
            db.session.add(new_booking)
            db.session.commit()
            return bookings_schema.dump(new_booking), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Invalid foreign key'}, 400
    
api.add_resource(Bookings, '/bookings')


class Register(Resource):
    def post(self):
        data = request.get_json()
        new_traveler = traveler_schema.load(data)
        db.session.add(new_traveler)
        db.session.commit()
        session['traveler_id'] = new_traveler.id
        return travelers_schema.dump(new_traveler), 201
    
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

