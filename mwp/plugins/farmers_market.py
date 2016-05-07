from datetime import datetime

from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class FarmersMarketPlugin(BasePlugin):

    @BasePlugin.hear('market')
    def is_it_farmers_market_day(self, message_data):
        now = datetime.now()
        if now.weekday() in [3, 4]:
            return mwp_room_client.send_notification('YES IT\'S FARMERS\' MARKET DAY!')
        else:
            return mwp_room_client.send_notification('No, it\'s not farmers\' market day :(')
