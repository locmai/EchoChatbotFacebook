#3rd-party library
from flask import Flask, request
import requests
import os
#core chatbot
from Chatbot.demobot import chatbot

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('FB_PAGE_ACCESS_TOKEN', 'conf_this')
VERIFY_TOKEN = os.environ.get('FB_PAGE_VERIFY_TOKEN', 'conf_this')


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.10/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, unicode(chatbot.get_response(str(message))))

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
