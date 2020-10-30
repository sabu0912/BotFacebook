from app import app
from flask import request
from random import choice
from requests import get, post
from json import dumps
import os

@app.route('/')
@app.route('/index')
def index():
    return 'GRUPO1 THE BEST'

@app.route('/webhook', methods=['GET'])
def webhook():
    if request.args.get('hub.verify_token') == os.getenv('VERIFY_TOKEN'):
        return request.args.get('hub.challenge')
    else:
        return 'Token invalido'
    #print(os.getenv('VERIFY_TOKEN'))
    #return 'webhook'

@app.route('/webhook', methods=['POST'])
def webhook_handle_message():
    data = request.get_json()
    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = message_random()
                    sender_graph({
                        'sender_id': recipient_id,
                        'message': response_sent_text
                    })

        #print(event)
    #print(request.get_json())
    return 'listo'

def sender_graph(object_message):
    response = post('https://graph.facebook.com/v8.0/me/messages', 
        params = {
            'access_token': os.getenv('PAGE_ACCESS_TOKEN')
        },
        headers = {
            'Content-Type': 'application/json'
        },
        data = dumps({
            'messaging_type': 'RESPONSE',
            'recipient': {
                'id': object_message['sender_id']
            },
            'message': {
                "text": '¿Qué deseas hacer?', #object_message['message']
                "quick_replies": [
                    {
                        "content_type":"text",
                        "title":"Escuchar Musica",
                        "payload":"1",
                        "image_url":'https://upload.wikimedia.org/wikipedia/commons/b/b9/Solid_red.png'
                    },{
                        "content_type":"text",
                        "title":"Chat",
                        "payload":"2",
                        "image_url":"https://upload.wikimedia.org/wikipedia/commons/f/f3/Green.PNG"
                    }
                ]
            }
        })
    )
    

def message_random():
    list_messages = ['Hola', 'Como estas?', 'Excelente', 'Que bien', 'Grupo1']
    return choice(list_messages)
    