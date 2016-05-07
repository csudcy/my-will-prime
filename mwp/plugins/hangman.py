from mwp.helpers.hangman import Hangman
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin


class HangmanPlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.hangman = Hangman()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.respond_to('hangman me')
    def hangman_me(self, message_data):
        """
        hangman me: Start a new game of hangman
        """
        mwp_room_client.send_notification(self.hangman.new_game(), html=True)

    @BasePlugin.respond_to('hangman status')
    def hangman_status(self, message_data):
        """
        hangman status: Check the progress of the current game
        """
        mwp_room_client.send_notification(self.hangman.get_status(), html=True)

    @BasePlugin.respond_to('hangman reveal')
    def hangman_reveal(self, message_data):
        # Reveal hangmans inner secrets
        mwp_room_client.send_notification('Here are all my secrets:')
        mwp_room_client.send_notification(self.hangman.get_secrets())

    @BasePlugin.respond_to('hangman guess (?P<guess>.*)')
    def hangman_guess(self, message_data, guess):
        """
        hangman guess ___: Make a guess in the current hangman game
        """
        mwp_room_client.send_notification(self.hangman.guess(guess), html=True)

    @BasePlugin.respond_to('hangman cheat (?P<guess>.*)')
    def hangman_cheat(self, message_data, guess):
        for letter in guess:
            output = self.hangman.guess(letter)
            if self.hangman.state != 'PLAYING':
                break
        mwp_room_client.send_notification(output, html=True)
