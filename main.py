from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests, keys

app = FastAPI()
templates = Jinja2Templates(directory="templates")

account_sid = keys.account_sid
auth_token = keys.auth_token


@app.get("/")
async def home(request: Request):
    base_url = "https://api.twilio.com/2010-04-01/Accounts/"
    messages_url = f"{base_url}{account_sid}/Messages.json"
    response = requests.get(messages_url, auth=(account_sid, auth_token))
    if response.status_code == 200:
        messages = response.json()["messages"]
        return templates.TemplateResponse("messages.html", {"request":request, "messages":messages})
    else:
        return {"error": response.text}


@app.post("/webhook")
async def webhook(request: Request):
    message = request.form.get('Body', '')
    sender = request.form.get('From', '')
    print(sender, " sent ", message)
    return "Succeess"

