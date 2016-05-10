import inspect


class BasePlugin(object):

    def __init__(self, app):
        self.app = app
        self._data_store = {}

    def _get_key(self, key):
        return '{prefix}__{key}'.format(
            prefix=self.__class__.__name__,
            key=key
        )

    def load_data(self, default=None, key='default'):
        key = self._get_key(key)
        return self._data_store.get(key, default)

    def save_data(self, data, key='default'):
        key = self._get_key(key)
        self._data_store[key] = data

    @classmethod
    def expose(cls, regex):
        def register_inner(func):
            func.plugin_regex = regex
            return func
        return register_inner

    @classmethod
    def hear(cls, regex):
        return cls.expose(
            r'^.*{regex}.*$'.format(
                regex=regex,
            )
        )

    @classmethod
    def respond_to(cls, regex):
        return cls.expose(
            r'^%TRIGGER% {regex}$'.format(
                regex=regex,
            )
        )

    @property
    def exposed_methods(self):
        """
        Returns a generator that iterates over all exposed methods of this class
        """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in methods:
            if hasattr(method, 'plugin_regex'):
                plugin_regex = method.plugin_regex.replace(
                    '%TRIGGER%',
                    self.app.config.get('TRIGGER', '/mwp')
                )
                yield plugin_regex, method
