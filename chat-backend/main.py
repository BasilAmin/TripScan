from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from messages import *
from datetime import datetime

app = FastAPI()

messageID = 0

class Message(BaseModel):
    user_id: str
    content: str

@app.get("/getMessages/")
async def get_messages():
    messages = read_messages_from_csv()
    return messages

@app.post("/sendMessage/")
async def send_message(message: Message):
    global messageID
    """Endpoint to send a message and save it to a CSV file."""
    save_message_to_csv(messageID, message.user_id, message.content)
    messageID += 1
    return {"status": "Message sent", "message_id": messageID}

class TripData(BaseModel):
    origin_city: str  # Three-letter city code
    start_date: str   # Start date in ISO format (YYYY-MM-DD)
    end_date: str     # End date in ISO format (YYYY-MM-DD)

def save_trip_data_to_csv(origin_city: str, start_date: str, end_date: str, file_path: str = "trips.csv"):
    """Saves trip data to a CSV file."""
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the header if the file is empty
        if f.tell() == 0:
            writer.writerow(["origin_city", "start_date", "end_date"])  # Write header
        
        # Write the trip data as a new row
        writer.writerow([origin_city, start_date, end_date])  # Write trip data

@app.post("/sendOriginAndDates/")
async def send_origin_and_dates(trip_data: TripData):
    """Endpoint to send origin city and trip dates and save them to a CSV file."""
    save_trip_data_to_csv(trip_data.origin_city, trip_data.start_date, trip_data.end_date)
    return {"status": "Trip data saved", "origin_city": trip_data.origin_city, "start_date": trip_data.start_date, "end_date": trip_data.end_date}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o "*" si es para demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)