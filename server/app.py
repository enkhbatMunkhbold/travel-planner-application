from flask import request, session, jsonify
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
# import re

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

# def is_valid_email(email):
#     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(email_pattern, email) is not None

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
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['fname', 'lname', 'email', 'password']):
                return jsonify({'error': 'Missing required fields'}), 400

            if Traveler.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Email already exists"}), 400

            traveler = Traveler(fname=data['fname'], lname=data['lname'], email=data['email'])
            traveler.password_hash(data['password'])
            db.session.add(traveler)
            db.session.commit()
            session['traveler_id'] = traveler.id
            return travelers_schema.dump(traveler), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'An error occurred during registration'}), 500
    
api.add_resource(Register, '/register')

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['email', 'password']):
                return jsonify({"error": "Missing required fields"}), 400
            
            traveler = Traveler.query.filter_by(email=data['email']).first()
            if traveler and traveler.authenticate(data['password']):
                session['traveler_id'] = traveler.id
                return travelers_schema.dump(traveler), 200
            return jsonify({'message': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error': 'An error occurred during login'}), 500

api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        traveler_id = session.get('traveler_id')
        if traveler_id:
            traveler = db.session.get(Traveler, traveler_id)
            if traveler:
                return travelers_schema.dump(traveler), 200
        return jsonify({'error': 'Not authenticated'}), 401

class Logout(Resource):
    def delete(self):
        session.pop('traveler_id', None)
        return {}, 204
    
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

