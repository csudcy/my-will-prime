from mwp.helpers.giphy import Giphy
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class GiphyPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.giphy = Giphy()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('gif me(?P<search_query>.*)$')
    def gif_me(self, message, search_query):
        """gif me ___ : Search google imaghes for ___, and post a random gif."""

        result = self.giphy.find(search_query.strip())
        if result:
            mwp_room_client.send_notification(result)
        else:
            mwp_room_client.send_notification('Why would anyone want a gif about that?!')
