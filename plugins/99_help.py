from registry import BasePlugin, plugin_registry


class Help(BasePlugin):
    name = 'Help'
    commands = {
        '!help': 'This help command',
    }

    def process(self, message, sender, command=None, *args):
        if command != 'help':
            return

        reply = ['Available commands:']
        for plugin in plugin_registry.plugins:
            if plugin.commands:
                reply.append(plugin.name)
                reply.append('\n'.join(('{}: {}'.format(c, d) for c, d in plugin.commands.iteritems())))

        return '\n'.join(reply)

plugin_registry.register(Help())
