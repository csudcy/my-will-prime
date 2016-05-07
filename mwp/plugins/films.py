from mwp.helpers.films import Films
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class FilmsPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.films = Films()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('film me (?P<search_query>.*)')
    def film_me(self, message_data, search_query):
        """
        film me ___: Find info about ___ from rotten tomatoes
        """
        mwp_room_client.send_notification(self.films.search(search_query))
