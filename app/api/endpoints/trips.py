import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from app.models import Trip, User
from app.database import engine
from app.schemas import TripRequestSchema, TripResponseSchema
from app.utils.prompt import generate_trip_plan
from datetime import datetime
from typing import List

load_dotenv()

router = APIRouter(prefix="/trips")


# Create a new trip
@router.post("/create", response_model=TripResponseSchema, status_code=201)
async def create_trip(trip: TripRequestSchema):
    
    # check if user exists
    user = await engine.find_one(User, User.id == ObjectId(trip.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate trip plan
    try:
        generated_plan = await generate_trip_plan(
            trip.destination,
            trip.budget,
            trip.duration,
            trip.interests
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not '{' in str(generated_plan):
        raise HTTPException(status_code=400, detail=generated_plan) 

    # Create new trip object
    new_trip = Trip(
        user_id=trip.user_id,
        destination=trip.destination,
        budget=trip.budget,
        duration=trip.duration,
        interests=trip.interests,
        itineraries=generated_plan.get("trip"),
        start_date=trip.start_date,
        favorite=False
    )
    
    # Save new trip to the database
    await engine.save(new_trip)
    
    # Return the created trip response
    return TripResponseSchema(id=str(new_trip.id), user_id=new_trip.user_id, destination=new_trip.destination, 
                              budget=new_trip.budget, duration=new_trip.duration, start_date=new_trip.start_date,
                              interests=new_trip.interests, itineraries=new_trip.itineraries)


# View all trips for a user
@router.get("/view", response_model=List[TripResponseSchema], status_code=200)
async def view_all_trips(user_id: str):
    # Query all trips for the user
    trips = await engine.find(Trip, Trip.user_id == user_id)

    if not trips:
        raise HTTPException(status_code=404, detail="No trips found for the user")


    # Return the list of trips
    return [TripResponseSchema(id=str(trip.id), user_id=trip.user_id, destination=trip.destination, 
                               budget=trip.budget, duration=trip.duration, start_date=trip.start_date,
                               interests=trip.interests, itineraries=trip.itineraries, favorite=trip.favorite) 
            for trip in trips]


# View favorite trips for a user
@router.get("/favorite", response_model=List[TripResponseSchema], status_code=200)
async def favorite_trips(user_id: str):
    # Query favorite trips for the user
    trips = await engine.find(Trip, Trip.user_id == user_id, Trip.favorite == True)

    if not favorite_trips:
        raise HTTPException(status_code=404, detail="No favorite trips found for the user")

    # Return the list of favorite trips
    return [TripResponseSchema(id=str(trip.id), user_id=trip.user_id, destination=trip.destination, 
                               budget=trip.budget, duration=trip.duration, start_date=trip.start_date, 
                               interests=trip.interests, itineraries=trip.itineraries, favorite=trip.favorite) 
            for trip in trips]


# Mark a trip as favorite or remove from favorites
@router.patch("/update-favorite/{trip_id}", response_model=TripResponseSchema, status_code=200)
async def update_favorite_trip(trip_id: str, favorite_value: str):
    # Convert favorite value to boolean
    if favorite_value.lower() == "true":
        favorite = True
    elif favorite_value.lower() == "false":
        favorite = False
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite value. Use 'true' or 'false'")

    # Find the trip by ID
    trip = await engine.find_one(Trip, Trip.id == ObjectId(trip_id))
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Update favorite status
    trip.favorite = favorite
    await engine.save(trip)
    
    # Return the updated trip
    return TripResponseSchema(id=str(trip.id), user_id=trip.user_id, destination=trip.destination, 
                              budget=trip.budget, duration=trip.duration, 
                              start_date=trip.start_date,
                              interests=trip.interests, itineraries=trip.itineraries, favorite=trip.favorite)

# Get a trip by ID
@router.get("/{trip_id}", response_model=TripResponseSchema, status_code=200)
async def get_trip(trip_id: str) :

    print(trip_id)
    # Find the trip by ID
    trip = await engine.find_one(Trip, Trip.id == ObjectId(trip_id))

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Return the updated trip
    return TripResponseSchema(id=str(trip.id), user_id=trip.user_id, destination=trip.destination, 
                              budget=trip.budget, duration=trip.duration, 
                              start_date=trip.start_date,
                              interests=trip.interests, itineraries=trip.itineraries, favorite=trip.favorite)