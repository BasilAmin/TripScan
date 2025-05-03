from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from .messages import *
from .orchestrator import *
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the TripScan API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/getMessages/")
async def get_messages():
    messages = read_messages_from_csv()
    return messages

@app.post("/sendMessage/")
async def send_message(message: Message):
    """Endpoint to send a message and save it to a CSV file."""
    messageID = save_message_to_csv(message.user_id, message.content)
    # Check if the message is "/start" to trigger LLM processing
    if(message.content == "/start"):
        messageID = save_message_to_csv("System", "We are processing your request. Please wait...")
        # Call the orchestrator function to process the messages and trip data
        BackgroundTasks.add_task(main_process)  
        return {"status": "Message sent", "message_id": messageID}
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