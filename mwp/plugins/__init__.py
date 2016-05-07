import re

from mwp.mwp_client import mwp_room_client


class PluginRegistry(object):
    plugin_funcs = []

    def load_plugins(self):
        # TODO: Load all plugins in the directory
        # TODO: Load other plugins
        # TODO: Blacklist
        from mwp.plugins import blarg
        plugin = blarg.BlargPlugin()
        for regex, func in plugin.exposed_methods:
            print regex, func
            self.plugin_funcs.append((regex, func))

    def process_message(self, message_data):
        # Process the message through my plugins
        for regex, func in self.plugin_funcs:
            if re.match(regex, message_data.message_text):
                func(message_data)

        # print self.plugin_funcs
        # mwp_room_client.send_notification(
        #     'TODO: Process room_message ({md.message_text})'.format(
        #         md=message_data
        #     )
        # )


plugin_registry = PluginRegistry()
