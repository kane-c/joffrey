from random import choice
import re
from registry import BasePlugin, plugin_registry


class Joffrey(BasePlugin):
    swears = ('shit', 'fuck', 'suck', 'screw', 'ass', 'cunt')
    insults = (
        'Fuck you',
        'How dare you talk to your King like that',
        'I\'ll tear your intestines out and feed them to the dire wolves',
    )

    def process(self, message, sender):
        if 'joffrey' in message.lower():
            for s in Joffrey.swears:
                if re.search(r'\b%s' % s, message, re.IGNORECASE):
                    return choice(Joffrey.insults)

            if not re.search(r'\bking\b', message, re.IGNORECASE):
                return '*King* Joffrey'

    def post_process(self, reply, message, sender):
        return '{}, peasant'.format(reply)

plugin_registry.register(Joffrey())
