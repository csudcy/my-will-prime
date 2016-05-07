from mwp.helpers.connect4 import Connect4
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class Connect4Plugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.connect4 = Connect4()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('c4 me')
    def hangman_me(self, message_data):
        """
        connect4 me: Start a new game of connect4
        """
        mwp_room_client.send_notification(self.connect4.new_game(), html=True)

    @BasePlugin.respond_to('c4 status')
    def hangman_status(self, message_data):
        """
        connect4 status: Check the progress of the current game
        """
        mwp_room_client.send_notification(self.connect4.get_status(), html=True)

    @BasePlugin.respond_to('c4 (?P<move>[OX][1-7])')
    def hangman_guess(self, message_data, move):
        """
        connect4 move ___: Make a move in the current connect4 game
        """
        mwp_room_client.send_notification(self.connect4.play(move), html=True)
