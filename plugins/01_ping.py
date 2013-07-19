from registry import BasePlugin, plugin_registry


class Ping(BasePlugin):
    def process(self, message, sender):
        if message.lower() == '!ping':
            return 'Pong!'
plugin_registry.register(Ping())