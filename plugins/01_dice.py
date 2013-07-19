from random import randrange
from registry import BasePlugin, plugin_registry


class Dice(BasePlugin):
    name = 'Dice'
    commands = {
        '!dice': 'Roll a die'
    }

    def process(self, message, sender, command=None, *args):
        if command == 'dice':
            return 'It\'s a {}'.format(randrange(1, 6))
plugin_registry.register(Dice())
