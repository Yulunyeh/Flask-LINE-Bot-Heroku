import os
import openai
import requests
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
openai.api_key = "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"

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=get_message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    completed_text = requests.post(
        CHATGPT_URL,
        headers={
            'Content-Type': 'application/json',
            'Authorization': " ".join(["Bearer", OPENAI_KEY])
        },
        json=data)

    res_json = response.json()
    reply_text = res_json.get("choices")[0].get(
        "text").replace("\n", "").replace("?", "")
        
    # Reply the text to client
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))


    # Send To Line
    #reply = TextSendMessage(text=f"{get_message}")
    #reply = TextSendMessage(text=f"{completed_text}")
    #line_bot_api.reply_message(event.reply_token, reply)
if __name__ == "__main__":
    app.run()
