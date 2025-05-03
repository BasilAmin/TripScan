from fastapi import FastAPI
from messages import *

app = FastAPI()

class Message(BaseModel):
    message_id: str
    user_id: str
    content: str
    timestamp: str

@app.get("/getMessages/")
async def get_messages():
    messages = read_messages_from_csv()
    return messages

@app.post("/sendMessage/")
async def send_message(message: Message):
    """Endpoint to send a message and save it to a CSV file."""
    save_message_to_csv(message.message_id, message.user_id, message.content, message.timestamp)
    return {"status": "Message sent", "message_id": message.message_id}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o "*" si es para demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)