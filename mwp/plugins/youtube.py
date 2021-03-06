import random

from mwp.helpers.youtube import Youtube
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class YoutubePlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.youtube = Youtube()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to(r'youtube (?P<search_query>.*)$')
    def youtube_me(self, message_data, search_query):
        """
        %TRIGGER% youtube ___ : Search youtube for ___, and post a random one.
        """

        videos = self.youtube.find(search_query.strip())
        if videos:
            mwp_room_client.send_notification(random.choice(videos))
        else:
            mwp_room_client.send_notification('Why would anyone make a video about that?!')

    @BasePlugin.respond_to(r'youtube5 (?P<search_query>.*)$')
    def youtube5(self, message_data, search_query):
        """
        %TRIGGER% youtube5 ___ : Search youtube for ___, and post the top 5 results.
        """

        videos = self.youtube.find(search_query, count=5)
        if videos:
            # mwp_room_client.send_notification('\n'.join(videos))
            for video in videos:
                mwp_room_client.send_notification(video)
        else:
            mwp_room_client.send_notification('Why would anyone make a video about that?!')
