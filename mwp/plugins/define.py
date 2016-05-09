from mwp.helpers.dictionary import Dictionary
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class DefinePlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.dictionary = Dictionary()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to(r'define')
    def define_random(self, message_data):
        """
        %TRIGGER% define: Get the definition of a random word
        """
        return mwp_room_client.send_notification(self.dictionary.get_random_definition())

    @BasePlugin.respond_to(r'define (?P<word>[a-zA-Z]+)')
    def define(self, message_data, word):
        """
        %TRIGGER% define ___: Get the definition of ___
        """
        return mwp_room_client.send_notification(self.dictionary.get_definition(word))
