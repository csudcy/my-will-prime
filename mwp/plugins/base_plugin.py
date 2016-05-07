import inspect


class BasePlugin(object):
    @classmethod
    def expose(self, regex):
        def register_inner(func):
            func.plugin_regex = regex
            return func
        return register_inner

    @property
    def exposed_methods(self):
        """
        Returns a generator that iterates over all exposed methods of this class
        """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in methods:
            if hasattr(method, 'plugin_regex'):
                yield method.plugin_regex, method
