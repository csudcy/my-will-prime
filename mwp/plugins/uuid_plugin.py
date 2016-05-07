import uuid

from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class UUIDPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('uuid')
    def uuid_single(self, message_data):
        """
        uuid me: Generate a UUID v4
        """
        mwp_room_client.send_notification(str(uuid.uuid4()))

    @BasePlugin.respond_to('uuid (?P<count>\d+)')
    def uuid_many(self, message_data, count):
        """
        uuid me: Generate a UUID v4
        """
        uuids = [
            str(uuid.uuid4())
            for i in xrange(int(count))
        ]
        mwp_room_client.send_notification('\n'.join(uuids))
