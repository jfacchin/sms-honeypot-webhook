# this app receives incoming sms messages from twilio and saves them to a csv file
from fastapi import FastAPI, Form
from datetime import datetime
import csv
import os

app = FastAPI()

# name of the file where every incoming message gets logged
LOG_FILE = "messages.csv"

# twilio sends a POST request here every time a text arrives at our number
@app.post("/sms")
async def receive_sms(
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...)
):
    # record the exact time the message was received
    timestamp = datetime.utcnow().isoformat()

    # check if the csv file already exists so we know whether to add column headers
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # write the header row only once, the first time the file is created
            writer.writerow(["timestamp", "from", "to", "body", "message_sid"])
        # write the actual message data as a new row
        writer.writerow([timestamp, From, To, Body, MessageSid])

    # twilio expects a response confirming we got the message
    return {"status": "received"}

# simple route to confirm the app is alive, useful for testing the deployment
@app.get("/")
async def health_check():
    return {"status": "ok"}