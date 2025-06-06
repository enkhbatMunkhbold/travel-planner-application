from flask import request, session, jsonify
from flask_restful import Resource

from config import app, db, api, ma
from models import Traveler, Itinerary, Tour, Booking


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

