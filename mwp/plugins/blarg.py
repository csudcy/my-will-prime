from mwp_client import mwp_room_client
from mwp.plugins import plugin_registry
from mwp.plugins.base_plugin import BasePlugin

class BlargPlugin(BasePlugin):

    @BasePlugin.expose(r'.*blarg.*')
    def blarg(self, message_data):
        mwp_room_client.send_notification('Hi Danny!', color='random')
