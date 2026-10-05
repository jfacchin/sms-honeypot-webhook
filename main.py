# this app receives incoming sms messages from twilio and saves them to firestore
from fastapi import FastAPI, Form
from fastapi.responses import Response
from google.cloud import firestore

app = FastAPI()


#connect to the firestore database
db = firestore.Client()

    # twilio sends a POST request here every time a text arrives at our number
@app.post("/sms")
def receive_sms(
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(""),
    MessageSid: str = Form(...)
):
    # save message to "messages" collection
    # MessageSid as id so if twilio retries it will not create a duplicate 
    db.collection("messages").document(MessageSid).set({
        "timestamp": firestore.SERVER_TIMESTAMP,
        "from": From,
        "to": To,
        "body": Body,
        "message_sid": MessageSid,
    })


  # empty twilio response = don't reply to the sender
    return Response(content="<Response></Response>", media_type="application/xml")

# simple route to confirm the app is alive, useful for testing the deployment
@app.get("/")
async def health_check():
    return {"status": "ok"}