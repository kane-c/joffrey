import logging
import ssl
import sys
import sleekxmpp
import plugins
from registry import plugin_registry
import settings


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')


class Bot(sleekxmpp.ClientXMPP):
    nick = settings.NICKNAME
    replies = 0

    def __init__(self):
        sleekxmpp.ClientXMPP.__init__(self, settings.JID, settings.PASSWORD)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler('session_start', self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler('message', self.receive_message)
        self.add_event_handler('groupchat_message', self.receive_message_muc)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence(pnick=self.nick)

        for room in settings.MUC_ROOMS:
            self.plugin['xep_0045'].joinMUC(room, self.nick)

    def receive_message(self, msg):
        if msg['type'] not in ('chat', 'normal'):
            return

        reply = self.process_message(msg['body'], msg['from'])

        if reply:
            msg.reply(reply).send()

    def receive_message_muc(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """

        # Ignore own messages
        if msg['mucnick'] == self.nick:
            return

        reply = self.process_message(msg['body'], msg['from'])

        if reply:
            self.say(reply, msg)

    def process_message(self, message, sender):
        message = message.strip()
        args = [message, sender]

        # Command support with messages starting with !
        # Provides the whole message, command (lowercase) and any arguments
        if message[0] == '!':
            parts = message[1:].partition(' ')
            args.append(parts[0].lower())
            for a in parts[2].split(' '):
                args.append(a)

        sender = self.get_display_name(sender)

        reply = None

        for plugin in plugin_registry.plugins:
            reply = plugin.process(*args)

            if reply:
                break

        if reply:
            for plugin in plugin_registry.plugins:
                reply = plugin.post_process(reply, message, sender)

            if reply:
                self.replies += 1
                reply = '{}: {}'.format(sender, reply)

        return reply

    def get_display_name(self, name):
        name = str(name)

        if '/' in name:
            return name.split('/')[1]
        else:
            return name

    def say(self, message, msg):
        return self.send_message(mto=msg['from'].bare,
                                 mbody=message,
                                 mtype='groupchat')

if __name__ == '__main__':
    bot = Bot()
    bot.register_plugin('xep_0030')  # Service Discovery
    bot.register_plugin('xep_0004')  # Data Forms
    bot.register_plugin('xep_0045')  # MUC
    bot.register_plugin('xep_0060')  # PubSub
    bot.register_plugin('xep_0172')  # Nicknames
    bot.register_plugin('xep_0199')  # XMPP Ping

    # Setup logging.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    bot.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # bot.ca_certs = 'path/to/ca/cert'

    # Connect to the XMPP server and start processing XMPP stanzas.
    if bot.connect((settings.XMPP_HOST, settings.XMPP_PORT)):
        bot.process(block=True)
    else:
        print('Unable to connect')
