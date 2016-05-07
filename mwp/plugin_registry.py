import inspect
import os
import re

from mwp.plugins import base_plugin
from mwp.mwp_client import mwp_room_client


class PluginRegistry(object):
    _responders = []

    def load_plugins(self):
        # TODO: Load other plugins
        # TODO: Blacklist
        plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
        module_names = self._get_module_names(plugin_path)
        modules = self._get_modules(module_names)
        classes = self._get_classes(modules)
        plugins = self._get_plugins(classes)
        self._add_responders(plugins)

    def _get_module_names(self, path):
        # Iterate over all files in path looking for python files
        # Have to make sure these are unique or it will import twice (once for py, once for pyc)
        module_names = set()
        for file_path in os.listdir(path):
            # Check this is a file
            full_path = os.path.join(path, file_path)
            if not os.path.isfile(full_path):
                continue

            # Check it is a non-private python file
            file_name, file_ext = os.path.splitext(file_path)
            if file_ext not in ('.py', '.pyc') or file_name[:2] == '__':
                continue

            module_names.add(file_name)
        return list(module_names)

    def _get_modules(self, module_names):
        for module_name in module_names:
            # Import that file
            try:
                module = __import__('mwp.plugins', locals(), globals(), [module_name])
                yield getattr(module, module_name)
            except Exception as ex:
                print 'Error importing "{module_name}": {ex}'.format(
                    module_name=module_name,
                    ex=ex
                )

    def _get_classes(self, modules):
        # Iterate over the modules and find all plugin classes
        for module in modules:
            classes = inspect.getmembers(module, predicate=inspect.isclass)
            for name, klass in classes:
                if issubclass(klass, base_plugin.BasePlugin) and klass != base_plugin.BasePlugin:
                    yield klass

    def _get_plugins(self, classes):
        # Create instances of all the given plugin classes
        for klass in classes:
            yield klass()

    def _add_responders(self, plugins):
        # Iterate over the plugins and add all responders to my registry
        for plugin in plugins:
            for regex, func in plugin.exposed_methods:
                self._responders.append((regex, func))

    def process_message(self, message_data):
        # Process the message through my plugins
        for regex, func in self._responders:
            match = re.match(regex, message_data.message_text)
            if match:
                func(message_data, **match.groupdict())


plugin_registry = PluginRegistry()
