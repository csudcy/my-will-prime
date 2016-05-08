import random

from mwp.helpers.wikipedia import Wikipedia
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class WikipediaPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.wikipedia = Wikipedia()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('wiki (?P<search_query>.*)$')
    def wikipedia_me(self, message_data, search_query):
        """
        wiki ___ : Search wikipedia for ___, and post the first result.
        """

        result = self.wikipedia.find(search_query.strip())
        if result:
            mwp_room_client.send_notification(result)
        else:
            mwp_room_client.send_notification('Why would anyone make an article about that?!')
