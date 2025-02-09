from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
auth_token = os.getenv("TWILIO_AUTH")

account_sid = 'AC99f49bb5c07ab9b4ca06ba9b8e8071f5'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18669401334',
  body='Make sure to take your meds!',
  to='+12247707887'
)

print(message.sid)