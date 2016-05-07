from mwp.helpers.youtube import Youtube
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class YoutubePlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.youtube = Youtube()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('youtube me (?P<search_query>.*)$')
    def youtube_me(self, message, search_query):
        """youtube me ___ : Search youtube for ___, and post a random one."""

        result = self.youtube.find(search_query)
        if result:
            mwp_room_client.send_notification(result)
        else:
            mwp_room_client.send_notification('Why would anyone make a video about that?!')
