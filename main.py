from flask import Flask
# import /root/flask/whatsapp-bot/keys.py
from twilio.rest import Client

app = Flask(__name__)
# account_sid = keys.ssid
# auth_token = keys.token
# client = Client(account_sid, auth_token)
# templates = ['Hai, This is Onyx Onwords Smart Assistant. This is my whatsapp number reply hear to talk to me!', ]
#
# message = client.messages.create(
#     body=str(templates[0]),
#     from_='whatsapp:+18144812393',
#     to='whatsapp:+919095640275'
# )
#
# print(message.sid)


@app.route("/")
def hello():
    return "Hello, this is onwords WhatsApp API"


if __name__ == "__main__":
    app.run(host='139.144.4.238', port=80)
