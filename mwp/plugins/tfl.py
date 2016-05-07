from mwp.helpers.tfl_road import TFLRoad
from mwp.helpers.tfl_tube import TFLTube
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class TFLPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.tfl_tube = TFLTube()
        self.tfl_road = TFLRoad()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('tfl tube (?P<line>.*)')
    def tfl_tube_me(self, message_data, line):
        """
        tfl tube ___: Get the status of the given tube line
        """
        line_status = self.tfl_tube.get_line_status(line)
        mwp_room_client.send_notification(line_status)

    @BasePlugin.respond_to('tfl road (?P<road>.*)')
    def tfl_road_me(self, message_data, road):
        """
        tfl road ___: Get the status of the given road
        """
        road_status = self.tfl_road.get_road_status(road)
        mwp_room_client.send_notification(road_status)

