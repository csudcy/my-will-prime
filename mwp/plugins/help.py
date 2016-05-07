import re

from mwp.mwp_client import mwp_room_client
from mwp.plugin_registry import plugin_registry
from mwp.plugins.base_plugin import BasePlugin


class HelpPlugin(BasePlugin):

    @BasePlugin.respond_to('help(?P<search>.*?)')
    def help(self, message_data, search):
        """help ___: Search help for ___"""
        search = search.strip()
        if search:
            search_re = r'.*%s.*' % search
        else:
            search_re = r'.+'
        responders = plugin_registry.get_responders(search_re)

        output = 'Here\'s what I know how to do:'
        for regex, description in responders:
            if ':' in description:
                index = description.find(':')
                description = '<b>%s</b>%s' % (description[:index], description[index:])
            output += '<br/> &nbsp; %s' % description

        mwp_room_client.send_notification(output, html=True)

    # @BasePlugin.respond_to('debug(?P<search>.*?)')
    # def programmer_help(self, message_data, search):

    #     # Prepare our search
    #     search = search.strip()
    #     if search:
    #         search_re = '.*%s.*' % search
    #     else:
    #         search_re = '.+'

    #     # Get the list of all regexes Will listens for
    #     all_regexes = self.load('all_listener_regexes')

    #     # Output everything that matches our search
    #     output = 'Here\'s everything I know how to listen to:'
    #     for r in all_regexes:
    #         if re.match(search_re, r, flags=re.DOTALL):
    #             output += '\n%s' % r

    #     mwp_room_client.send_notification(output)
