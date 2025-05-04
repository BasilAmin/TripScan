from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from .messages import *
from .orchestrator import *
from datetime import datetime
from .image import get_city_image_link
import os

app = FastAPI()

FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
if not FOURSQUARE_API_KEY:
    raise RuntimeError("Set FOURSQUARE_API_KEY in your environment")

HEADERS = {
    "Accept": "application/json",
    "Authorization": FOURSQUARE_API_KEY
}

def fetch_hotels(city: str, limit: int = 5):
    resp = requests.get(
        "https://api.foursquare.com/v3/places/search",
        headers=HEADERS,
        params={
            "query": "hotel",
            "near": city,
            "limit": limit
        }
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

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
async def send_message(message: Message, background_tasks: BackgroundTasks):
    """Endpoint to send a message and save it to a CSV file."""
    messageID = save_message_to_csv(message.user_id, message.content)
    # Check if the message is "/start" to trigger LLM processing
    if(message.content == "Can we get some recommendations?"):
        messageID = save_message_to_csv("System", "We are processing your request. Please wait...")
        # Call the orchestrator function to process the messages and trip data
        background_tasks.add_task(main_process)  
        return {"status": "Message sent", "message_id": messageID}
    elif(message.content == "Can we discuss possible travel dates that work for everyone?"):
        messageID = save_message_to_csv("System", "We are processing your request. Please wait...")
        # Call the orchestrator function to process the messages and trip data
        background_tasks.add_task(negociation_process)  
        return {"status": "Message sent", "message_id": messageID}
    return {"status": "Message sent", "message_id": messageID}

@app.post("/sendOriginAndDates/")
async def send_origin_and_dates(trip_data: TripData):
    """Endpoint to send origin city and trip dates and save them to a CSV file."""
    save_trip_data_to_csv(trip_data.user_id,trip_data.origin_city, trip_data.start_date, trip_data.end_date)
    return {"status": "Trip data saved", "origin_city": trip_data.origin_city, "start_date": trip_data.start_date, "end_date": trip_data.end_date}

@app.get("/recommendations/")
async def send_origin_and_dates():
    try:
        with open("output.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="output.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in output.json")

@app.post("/negotiate/")
async def negotiate():
    messages = read_messages_from_csv()
    chat_data = "\n".join([f"{msg['user_id']}: {msg['content']}" for msg in messages])
    try:
        result = await chat_with_gemini(chat_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/city-image/{city_name}")
async def get_city_image(city_name: str):
    """
    Endpoint to get an image URL for a city
    """
    try:
        image_url = get_city_image_link(city_name)
        return {"image_url": image_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/clear_chat")
async def clear_chat():
    """
    Endpoint to clear all the chat information
    """
    try:
        files_to_delete = ["output.json", "trips.csv", "messages.csv"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
        return {"detail": "Chat data cleared."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/hotels/")
def get_hotels(city: str = Query(..., description="City name to search hotels in")):
    """
    Returns a list of hotels (name and formatted address) for the given city.
    """
    try:
        places = fetch_hotels(city)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    if not places:
        return {"hotels": []}

    hotels = []
    for p in places:
        name = p.get("name", "Unknown")
        address = ", ".join(p.get("location", {}).get("formatted_address", []))
        hotels.append({"name": name, "location": address})

    return {"hotels": hotels}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)