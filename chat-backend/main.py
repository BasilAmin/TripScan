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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o "*" si es para demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)