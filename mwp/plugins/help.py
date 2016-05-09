import re

from mwp.mwp_client import mwp_room_client
from mwp.plugin_registry import plugin_registry
from mwp.plugins.base_plugin import BasePlugin


class HelpPlugin(BasePlugin):

    @BasePlugin.respond_to(r'help(?P<search>.*?)')
    def help(self, message_data, search):
        """%TRIGGER% help ___: Search help for ___"""
        responders = plugin_registry.get_responders(self.app, search)

        output = 'Here\'s what I know how to do:'
        responders.sort(key=lambda x: x[1])
        from pprint import pprint as pp
        pp(responders)
        for regex, description in responders:
            if description:
                if ':' in description:
                    index = description.find(':')
                    description = '<b>{command}</b>{comment}'.format(
                        command=description[:index],
                        comment=description[index:]
                    )
                output += '<br/> &nbsp; %s' % description

        mwp_room_client.send_notification(output, html=True)

    @BasePlugin.respond_to(r'debug(?P<search>.*?)')
    def programmer_help(self, message_data, search):
        responders = plugin_registry.get_responders(self.app, search)

        output = 'Here\'s what I know how to do:'
        for regex, description in responders:
            output += '<br/> &nbsp; <b>{regex}</b> - {description}'.format(
                regex=regex,
                description=description or ''
            )

        mwp_room_client.send_notification(output, html=True)
