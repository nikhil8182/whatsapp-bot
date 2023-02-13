from fastapi import FastAPI, Request, Header
from fastapi.templating import Jinja2Templates
import requests, keys
from twilio.rest import Client
# config = {
#   'apiKey': "AIzaSyCcr9qTflrsOGcZhcU1h4tr6Kcp92ywmM8",
#   'authDomain': "whatsapp-bot-82679.firebaseapp.com",
#   'projectId': "whatsapp-bot-82679",
#   'storageBucket': "whatsapp-bot-82679.appspot.com",
#   'messagingSenderId': "941558673189",
#   'appId': "1:941558673189:web:066117b4aabcbe30fc74cc"
# }
app = FastAPI()
templates = Jinja2Templates(directory="templates")

account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

# firebase = pyrebase(config)
# db = firebase.database()


def whatsapp(reply):
    global from_
    message = client.messages.create(
        body=reply,
        to=from_,
        from_="whatsapp:+18144812393"
    )


url = "http://117.247.181.113:8000/"


def device(room, sts):
    device_data = requests.get(url).json()
    for ids in device_data:
        if room == ids['Room'].lower():
            _url = url + str(ids['id']) + "/"
            if sts == "on":
                requests.put(_url, json={"Device_Status": True})
            elif sts == "off":
                requests.put(_url, json={"Device_Status": False})
        # else:
        #     print(f'{room} is not equal to {ids["Room"]}')


def queryContains(a):
    global body
    for x in a:
        if x in body:
            # print(f'{x} is in {body}')
            return True

    return False


@app.get("/")
async def home(request: Request):
    base_url = "https://api.twilio.com/2010-04-01/Accounts/"
    messages_url = f"{base_url}{account_sid}/Messages.json"
    response = requests.get(messages_url, auth=(account_sid, auth_token))
    if response.status_code == 200:
        messages = response.json()["messages"]
        return templates.TemplateResponse("messages.html", {"request": request, "messages": messages})
    else:
        return {"error": response.text}


global body, from_

# def storeInDb():
#     db.child("+919095640275").push({"name": "Nikhil"})

def reply(body, _from):
    # if queryContains(['hai', 'hello', 'hi', 'hey']):
    # reply = "hai, this is onyx!, from fast api"
    # whatsapp(reply)
    # storeInDb()
    if queryContains(['off', 'turn', 'on']):
        if queryContains(['light', 'tubelight', 'lights']):
            if queryContains(['room', 'garage']):
                if queryContains(['admin', 'green', 'garage']):
                    if queryContains(['admin']):
                        if queryContains(['on']):
                            device('admin room', 'on')
                            whatsapp(f'turrnig on admin room lights and query = {body}')
                        elif queryContains(['off']):
                            device('admin room', 'off')

                            whatsapp('turning off admin room light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in admin room')

                    elif queryContains(['green']):
                        if queryContains(['on']):
                            device('green room', 'on')
                            whatsapp('turrnig on green room lights')
                        elif queryContains(['off']):
                            device('green room', 'off')
                            whatsapp('turning off green room light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in green room')

                    elif queryContains(['garage']):
                        if queryContains(['on']):
                            device('garage', 'on')
                            whatsapp('turrnig on garage lights')
                        elif queryContains(['off']):
                            device('garage', 'off')
                            whatsapp('turning off garage light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in garage')
        else:
            a = requests.post("http://onwordsapi.com/", json={"command": body, "name": "", "gender": "str"}).json()
            whatsapp(a["reply"])
            # whatsapp('sorry, I don't recognise device')
    elif queryContains(['kamalika','kamali']):
        if _from == "whatsapp:+919600612340":
            whatsapp('Kamalika, A golden hearted girl with flattering eyes and moles🥰')
        elif _from == "whatsapp:+918078850374":
            whatsapp('kamalika, is an enemy of my boss maha')

    else:
        a = requests.post("http://onwordsapi.com/", json={"command": body, "name": "", "gender": "str"}).json()
        whatsapp(a["reply"])



@app.post("/webhook")
async def webhook(request: Request):
    # Handle the webhook request
    data = await request.form()
    message_body = data.get("Body")
    message_from = data.get("From")
    global body, from_
    body = message_body.lower()
    from_ = message_from.lower()
    # message_sid = request.form.get("MessageSid")
    # message_body = request.form.get("Body")
    reply(message_body.lower(), message_from)
