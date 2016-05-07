import os

from ac_flask.hipchat import Addon, room_client, sender
from flask import Flask


print os.environ.get('MWP_ADDON_KEY')
print os.environ.get('MWP_ADDON_NAME')
print os.environ.get('MWP_BASE_URL')

addon = Addon(
    app=Flask(__name__),
    allow_room=True,
    scopes=['send_notification'],
    env_prefix='MWP_'
)


@addon.webhook(event="room_enter")
def room_entered():
    room_client.send_notification('hi: %s' % sender.name)
    return '', 204


if __name__ == '__main__':
    addon.run(
        host=os.environ.get('MWP_HOST', '0.0.0.0'),
        port=os.environ.get('MWP_PORT', 8080),
    )
