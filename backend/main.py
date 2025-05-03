from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from messages import *
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the TripScan API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app = FastAPI()

messageID = 0

@app.get("/getMessages/")
async def get_messages():
    messages = read_messages_from_csv()
    return messages

@app.post("/sendMessage/")
async def send_message(message: Message):
    global messageID
    """Endpoint to send a message and save it to a CSV file."""
    messageID = save_message_to_csv(message.user_id, message.content)
    return {"status": "Message sent", "message_id": messageID}

@app.post("/sendOriginAndDates/")
async def send_origin_and_dates(trip_data: TripData):
    """Endpoint to send origin city and trip dates and save them to a CSV file."""
    save_trip_data_to_csv(trip_data.origin_city, trip_data.start_date, trip_data.end_date)
    return {"status": "Trip data saved", "origin_city": trip_data.origin_city, "start_date": trip_data.start_date, "end_date": trip_data.end_date}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)