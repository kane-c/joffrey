class PluginRegistry(object):
    plugins = []

    def register(self, plugin):
        self.plugins.append(plugin)
plugin_registry = PluginRegistry()


class BasePlugin(object):
    name = 'Unnamed plugin'
    commands = {}

    def process(self, message, sender):
        """
        Return a reply to use if the message should trigger the plugin. Return
        None to not reply
        """
        return None

    def post_process(self, reply, message, sender):
        """
        Optionally change the reply that was chosen. Return the reply to do
        nothing.
        """
        return reply
