from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
import torch
import asyncio

app = FastAPI()
class Negotiate_request(BaseModel):
    messeges: list[dict]

negotiator = pipeline("text-generation", model="./traveltime_negotiator",
device_map = "auto", torch_dtype = torch.bfloat16)

@app.post("/negotiate")
async def negotiate(request: Negotiate_request):
    convo = "/n".join([f"{msg['role']}]): {msg['content']}"
    for msg in request.messeges])

    prompt = f"""### Input:
    {convo}

    Comprimise options: """


    response = negotiator(
        prompt,
        maz_new_tokens=200,
        temperature=0.7,
        do_sample=True
    )

    return{"suggestions" : response[0]["generated_text"].split("### Output:")[1].strip()}
