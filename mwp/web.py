import collections
import json
import os
import traceback

from ac_flask.hipchat import Addon, sender
from flask import Flask
from flask import request

from mwp.plugin_registry import plugin_registry
from mwp.mwp_client import mwp_room_client


# Ac-flask-hipchat is hardcoded to check for MongoHQ env var.
# To be able to use other addons (e.g. mLab), copy their env var to the MongoHQ var
if not os.environ.get('MONGOHQ_URL'):
    # Try mLab instead
    if os.environ.get('MONGODB_URI'):
        os.environ['MONGOHQ_URL'] = os.environ.get('MONGODB_URI')


app=Flask(__name__)
addon = Addon(
    app=app,
    allow_room=True,
    scopes=[
        'send_notification',
        'view_messages',
        'view_room'
    ],
    env_prefix='MWP_'
)


# Load all MWP plugins
plugin_registry.load_plugins(app)


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

    try:
        _process_message(message_data)
    except Exception as ex:
        tb = traceback.format_exc()
        mwp_room_client.send_notification(
            'Oh no, something went wrong!\n\n{tb}'.format(tb=tb),
            color='red'
        )

    # Always return something
    return '', 204


def _process_message(message_data):
    print '\n' * 5
    print message_data.message_text
    if message_data.message_text == '/mwp json':
        # Return all the JSON info sent from Hipchat
        # TODO: Does this contain sensitive info?
        pretty_json = json.dumps(request.json, sort_keys=True, indent=2)
        mwp_room_client.send_notification(pretty_json)
    elif message_data.message_text == '/mwp info':
        # Return the useful info sent from Hipchat
        mwp_room_client.send_notification(str(message_data))
    elif message_data.message_text == '/mwp exception':
        # Throw an exception to test error handling
        raise Exception('Here\'s your exception!')
    else:
        plugin_registry.process_message(message_data)


def main():
    port = os.environ.get('MWP_PORT', '8080')
    print os.environ
    if 'DYNO' in os.environ:
        # Running on Heroku; us $PORT
        print 'Looks like I\'m on Heroku!'
        port = os.environ.get('PORT')

    addon.run(
        host=os.environ.get('MWP_HOST', '0.0.0.0'),
        port=int(port),
    )


if __name__ == '__main__':
    main()
