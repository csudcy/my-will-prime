from mwp.mwp_client import mwp_room_client
from mwp.helpers.chuck_norris import ChuckNorris
from mwp.plugins.base_plugin import BasePlugin


class ChuckNorrisPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.cn = ChuckNorris()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('chuck norris me')
    def chuck_norris_me(self, message):
        """
        chuck norris me: Get the a joke about Chuck Norris (there is no gaurentee it will be good).
        """
        mwp_room_client.send_notification(self.cn.get_chuck_norris_joke())

    @BasePlugin.respond_to('joke me (?P<first_name>.*) (?P<last_name>.*)')
    def joke_me(self, message, first_name, last_name):
        """
        joke me ___ ___: Get the a joke about a person (first name and last name). There is no gaurentee it will be good.
        """
        if not first_name or not last_name:
            mwp_room_client.send_notification('I need both a first and last name to make a joke!', color='red')
        else:
            mwp_room_client.send_notification(self.cn.get_joke_with_name(first_name, last_name))
