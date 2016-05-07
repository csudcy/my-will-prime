from mwp.helpers.urban_dictionary import UrbanDictionary
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class UrbanDefinePlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.dictionary = UrbanDictionary()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('slang (?P<word>[a-zA-Z\s]+)')
    def slang(self, message, word):
        """
        slang ___: Get the definition of a slang
        """
        return mwp_room_client.send_notification(self.dictionary.get_definition(word))
