from mwp.helpers.hot_deals import Dealer
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class HUKDPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.dealer = Dealer()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('deal me')
    def deal_random(self, message_data):
        """deal me: Get a random hot UK deal!"""
        return mwp_room_client.send_notification(self.dealer.get_deal('random'))

    @BasePlugin.respond_to('deal hot')
    def deal_hot(self, message_data):
        """deal hot: Get me the hottest hot UK deal!"""
        return mwp_room_client.send_notification(self.dealer.get_deal('hot'))

    @BasePlugin.respond_to('deal new')
    def deal_new(self, message_data):
        """deal new: Get me the latest hot UK deal!"""
        return mwp_room_client.send_notification(self.dealer.get_deal('new'))
