from mwp.helpers.business import Business
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class BusinessPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.business = Business()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.hear('business')
    def hear_business(self, message):
        """
        business: Get your favourite corporate strategems
        """
        return mwp_room_client.send_notification(self.business.acquire_business())
