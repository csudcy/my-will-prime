from mwp.mwp_client import mwp_room_client
from mwp.helpers.ascii_art import ASCIIArt
from mwp.plugins.base_plugin import BasePlugin


class ASCIIPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.ascii_art = ASCIIArt()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to(r'ascii me (?P<text>.*?)')
    def ascii_me(self, message_data, text=None):
        "ascii me ___: Say ___ using a random ascii font"
        art = self.ascii_art.render(text)
        mwp_room_client.send_notification('<pre>%s</pre>' % art, html=True)
