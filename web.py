import collections
import json
import os

from ac_flask.hipchat import Addon, room_client, sender
from flask import Flask
from flask import request


addon = Addon(
    app=Flask(__name__),
    allow_room=True,
    scopes=[
        'send_notification',
        'view_messages',
        'view_room'
    ],
    env_prefix='MWP_'
)


@addon.webhook(event='room_enter')
def room_entered():
    room_client.send_notification('hi: %s' % sender.name)
    return '', 204


MessageInfo = collections.namedtuple(
    'MessageInfo',
    (
        'date',
        'user_id',
        'user_name',
        'user_mention_name',
        'message_mentions',
        'message_text',
        'room_id',
        'room_name',
        'room_members_link',
        'room_participants_link',
    )
)

@addon.webhook(event='room_message')
def room_message():
    message_data = MessageInfo(
        date=request.json['item']['message']['date'],
        user_id=request.json['item']['message']['from']['id'],
        user_name=request.json['item']['message']['from']['name'],
        user_mention_name=request.json['item']['message']['from']['mention_name'],
        message_mentions=request.json['item']['message']['mentions'],
        message_text=request.json['item']['message']['message'],
        room_id=request.json['item']['room']['id'],
        room_name=request.json['item']['room']['name'],
        room_members_link=request.json['item']['room']['links']['members'],
        room_participants_link=request.json['item']['room']['links']['participants'],
    )
    if message_data.message_text == '/mwp json':
        # Return all the JSON info sent from Hipchat
        # TODO: Does this contain sensitive info?
        pretty_json = json.dumps(request.json, sort_keys=True, indent=2)
        pretty_json = pretty_json.replace('\n', '<br/>')
        print pretty_json
        room_client.send_notification(pretty_json)
    elif message_data.message_text == '/mwp info':
        # Return the useful info sent from Hipchat
        room_client.send_notification(str(message_data))
    else:
        # Process the message through my plugins
        room_client.send_notification(
            'TODO: Process room_message ({md.message_text})'.format(
                md=message_data
            )
        )
    return '', 204


@addon.webhook(event='room_notification')
def room_notification():
    print 'room_notification'
    room_client.send_notification('room_notification')
    return '', 204


if __name__ == '__main__':
    addon.run(
        host=os.environ.get('MWP_HOST', '0.0.0.0'),
        port=os.environ.get('MWP_PORT', 8080),
    )
