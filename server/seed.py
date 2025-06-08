#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, uniform
from datetime import date, timedelta

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Traveler, Tour, Itinerary, Booking

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data
        Booking.query.delete()
        Tour.query.delete()
        Itinerary.query.delete()
        Traveler.query.delete()
        
        print("Creating travelers...")
        travelers = []
        for _ in range(10):
            traveler = Traveler(
                fname=fake.first_name(),
                lname=fake.last_name(),
                email=fake.email()
            )
            traveler.set_password('password123')
            travelers.append(traveler)
        db.session.add_all(travelers)
        db.session.commit()
        
        print("Creating tours...")
        tours = []
        tour_titles = [
            "Mongolian Gobi Desert Adventure",
            "Ancient Silk Road Expedition",
            "Nomadic Culture Experience",
            "Eagle Hunting Tour",
            "Mongolian Steppe Safari"
        ]
        for title in tour_titles:
            tour = Tour(
                tour_title=title,
                tour_description=fake.paragraph(nb_sentences=5)
            )
            tours.append(tour)
        db.session.add_all(tours)
        db.session.commit()
        
        print("Creating itineraries...")
        itineraries = []
        for _ in range(8):
            itinerary = Itinerary(
                trip_title=f"{fake.word().capitalize()} Explorer Package",
                trip_length=randint(3, 14),
                trip_route=fake.paragraph(nb_sentences=3),
                trip_price=round(uniform(500, 3000), 2)
            )
            itineraries.append(itinerary)
        db.session.add_all(itineraries)
        db.session.commit()
        
        print("Creating bookings...")
        bookings = []
        for _ in range(20):
            start_date = fake.date_between(start_date='+30d', end_date='+60d')  # Start date at least 30 days in future
            trip_length = randint(3, 14)
            end_date = start_date + timedelta(days=trip_length)
            selected_itinerary = rc(itineraries)
            total_price = round(selected_itinerary.trip_price * randint(1, 6), 2)  # Price based on itinerary price and number of travelers
            
            booking = Booking(
                number_of_travelers=randint(1, 6),
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=fake.random_element(elements=('pending', 'confirmed', 'cancelled')),
                traveler_id=rc(travelers).id,
                tour_id=rc(tours).id,
                itinerary_id=selected_itinerary.id
            )
            bookings.append(booking)
        db.session.add_all(bookings)
        db.session.commit()
        
        print("Seeding completed!")
